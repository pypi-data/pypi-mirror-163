import os
import halo
import glob
import errno
import gitlab
import pathlib
import subprocess
from chinstrap import helpers
from prompt_toolkit import HTML
from chinstrap.helpers import hexit, startSpinner
from chinstrap.helpers import checkToCreateDir
from chinstrap.core.templates import contracts
from chinstrap.helpers import ensurePathExists
from chinstrap.helpers import fatal, runCommand
from prompt_toolkit import print_formatted_text
from chinstrap.helpers.container import pullImage, runSmartPyContainer

repo = "SmartPy/smartpy"
image = "ant4g0nist/smartpy"


class SmartPy:
    def __init__(self, args, config, chinstrapPath) -> None:
        self.config = config
        self.args = args

    def getCompiler(self):
        home = os.path.expanduser("~/chinstrap/bin")

        smartpyHome = pathlib.Path(
            os.getenv(
                "SMARTPY_HOME",
                home,
            )
        )
        
        fullPath = pathlib.Path(f"{smartpyHome}/smartpy-cli/SmartPy.sh")

        if not fullPath.is_file():
            fatal(
                f"Failed to find Smartpy compiler in {fullPath}. \
                    Please set SMARTPY_HOME env or run \
                    'chinstrap install -c smartpy' to install SmartPy"
            )

        return fullPath

    def compileSources(self):
        contracts = glob.iglob("contracts/*.py")
        self.initBuildFolder()
        status = 0
        for contract in contracts:
            if self.compileOne(contract):
                status = 1

        return status

    def compileOne(self, contract):
        name = pathlib.Path(contract).name
        spinner = halo.Halo(text=f"Compiling {name}", spinner="dots")
        spinner.start()
        success, msg = self.runCompiler(contract)
        if not success:
            self.status = 1
            spinner.fail(text=f"Compilation of {str(name)} Failed!")
            print("\nReason:")
            print(msg)
            return 1
        else:
            spinner.succeed(text=f"{name} compilation successful!")

        return 0

    def runCompiler(self, contract):
        if self.args.local:
            return self.runCompilerInHost(contract)
        else:
            name = pathlib.Path(contract).name
            command = f"compile /contracts/{name} /build/"
            return self.runCommandInContainer(
                contract,
                command,
                name,
                volumes={
                    f"{os.getcwd()}/contracts/": {"bind": "/contracts/", "mode": "ro"},
                    f"{os.getcwd()}/tests/": {"bind": "/tests/", "mode": "ro"},
                    f"{os.getcwd()}/build/contracts/": {
                        "bind": "/build/",
                        "mode": "rw",
                    },
                    f"{os.getcwd()}": {"bind": "/home/", "mode": "ro"},
                },
            )

    def runCompilerInHost(self, contract):
        """
        Compile with local SmartPy-cli
        """
        self.compiler = self.getCompiler()

        command = [self.compiler, "compile", str(contract), "./build/contracts/"]
        proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = proc.communicate()
        exit_code = proc.wait()

        if exit_code:
            if stderr:
                return False, stderr.decode()
            if stdout:
                return False, stdout.decode()

        return True, ""

    def runCommandInContainer(
        self,
        contract,
        command,
        name,
        volumes={os.getcwd(): {"bind": "/home/", "mode": "ro"}},
    ):
        container = runSmartPyContainer(command, [contract], volumes=volumes)
        output = ""

        for line in container.logs(stream=True):
            output += line.decode("utf-8")

        if output:
            return False, output

        return True, ""

    def runAllTests(self):
        tests = glob.iglob("./tests/*_smartpy.py")
        status = 0
        for test in tests:
            if self.runSingleTest(test):
                status = 1

        return status

    def runSingleTest(self, test):
        if self.args.local:
            self.runSingleTestOnHost(test)
        else:
            self.runSingleTestInContainer(test)

    def runSingleTestOnHost(self, test):
        self.compiler = self.getCompiler()

        name = pathlib.Path(test).name
        command = [self.compiler, "test", str(test), "./build/tests/"]

        spinner = halo.Halo(text=f"Running {name} test", spinner="dots")
        spinner.start()

        proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = proc.communicate()
        exit_code = proc.wait()

        if exit_code:
            spinner.fail(text=f"Test {str(name)} Failed!\n")
            if stderr:
                print(stderr.decode())
            if stdout:
                print(stdout.decode())

            return 1

        spinner.succeed(text=f"Tests passed on {name}")
        return 0

    def runSingleTestInContainer(self, test):
        name = pathlib.Path(test).name
        spinner = halo.Halo(text=f"Running {name} test", spinner="dots")
        spinner.start()

        if self.config.compiler.test == "smartpy":
            command = f"test {test} /build/tests/"

            suc, msg = self.runCommandInContainer(
                test,
                command,
                name,
                volumes={
                    f"{os.getcwd()}/contracts/": {"bind": "/contracts/", "mode": "ro"},
                    f"{os.getcwd()}/tests/": {"bind": "/tests/", "mode": "ro"},
                    f"{os.getcwd()}/build/": {"bind": "/build/", "mode": "rw"},
                    f"{os.getcwd()}": {"bind": "/home/", "mode": "ro"},
                },
            )
            if not suc:
                spinner.fail(text=f"Test {str(name)} Failed!\n{msg}")
                return 1

            spinner.succeed(text=f"Tests passed on {name}")

        else:
            spinner.fail(
                f"{self.config.compiler.test} tests not supported for Contracts made in SmartPy"
            )
            return 1

        return 0

    def initBuildFolder(self):
        helpers.mkdir("./build")
        helpers.mkdir("./build/contracts/")

    @staticmethod
    def installCompiler(local=False, force=False):
        spin = startSpinner("Installing SmartPy")

        if local:
            fullPath = os.path.expanduser("~/chinstrap/bin")
            
            os.makedirs(fullPath, exist_ok=True)

            ensurePathExists(fullPath)

            cmds = [
                f"curl -o {fullPath}/smartpy-install.sh -L https://smartpy.io/cli/install.sh",
                f"chmod +x {fullPath}/smartpy-install.sh",
                f"{fullPath}/smartpy-install.sh --yes --prefix \
                        {fullPath}/smartpy-cli",
                f'/bin/bash -c "chmod +x {fullPath}/smartpy-cli/SmartPy.sh"',
            ]

            for cmd in cmds:
                proc = runCommand(cmd, shell=True)
                proc.wait()

            os.remove(f"{fullPath}/smartpy-install.sh")
    
        else:
            suc, msg = pullImage(image, "latest")
            if not suc:
                spin.fail(f"Failed to install compiler. {msg}")
                hexit(1)
            
        spin.stop_and_persist("🎉", "SmartPy installed")

    @staticmethod
    def templates():
        downloader = SmartPyDownloader()
        downloader.displayTemplateCategories()

    @staticmethod
    def FA1_2_SmartPy(chinstrapPath):
        spinner = halo.Halo(text="Creating FA.1.2 Template")
        spinner.start()

        targetPath = pathlib.Path(f"{os.getcwd()}")

        helpers.copyFile(
            f"{chinstrapPath}/core/sources/contracts/FA1.2.py",
            f"{targetPath}/contracts/FA1.2.py",
        )

        helpers.copyFile(
            f"{chinstrapPath}/core/sources/originations/1_FA12_origination.py",
            f"{targetPath}/originations/1_FA12_origination.py",
        )

        helpers.copyFile(
            f"{chinstrapPath}/core/sources/tests/FA1.2.smartpy.py",
            f"{targetPath}/tests/FA1.2_smartpy.py",
        )

        spinner.succeed(text="Creatied FA.1.2 templates!")


class SmartPyDownloader:
    def __init__(self):
        self.gl = gitlab.Gitlab("https://gitlab.com")
        self.project = self.gl.projects.get(repo)

    def displayTemplateCategories(self):
        prom = helpers.SelectionPrompt()
        templateType = prom.prompt(
            HTML("<ansired>Available categories:</ansired>"), options=contracts.keys()
        )

        if templateType == "State Channels":
            for i in contracts[templateType]:
                if "contract" in i.keys():
                    self.downloadContractTemplate(
                        f"python/templates/{i['fileName']}", True
                    )
                else:
                    self.downloadContractTemplate(f"python/templates/{i['fileName']}")

            return

        options = []
        for i in contracts[templateType]:
            options.append(i["name"])

        print()

        prom = helpers.SelectionPrompt(sideBySide=False)
        contractChoice = prom.prompt(
            HTML("<ansigreen>Available contracts:</ansigreen>"), options=options
        )

        for i in contracts[templateType]:
            if i["name"] == contractChoice:
                self.downloadContractTemplate(f"python/templates/{i['fileName']}")

    def getListOfTemplates(self):
        templates = self.project.repository_tree(path="python/templates", per_page=200)
        for template in templates:
            if template["type"] == "blob":
                yield template["id"], template["name"], template["path"]

    def showAvailableFiles(self):
        msg = HTML(f"<u>name {'':<16}|{'':<16} path</u>")
        print_formatted_text(msg)

        for i in self.getListOfTemplates():
            msg = HTML(f"<b><ansigreen>{i[1]:32}</ansigreen></b> {i[2]}")
            print_formatted_text(msg)

    def mkdir_p(self, path):
        try:
            os.makedirs(path)
        except OSError as exc:  # Python >2.5
            if exc.errno == errno.EEXIST and os.path.isdir(path):
                pass
            else:
                raise

    def downloadContractTemplate(self, path, contract=False):
        basename = os.path.basename(path)
        spinner = halo.Halo(text="Fetching file!", spinner="dots")
        spinner.start()

        localFilePath = "contracts/"

        if contract:
            localFilePath += basename
        else:
            localFilePath += path.replace("python/templates/", "")

        self.mkdir_p(os.path.dirname(localFilePath))

        with open(localFilePath, "wb") as f:
            self.project.files.raw(
                file_path=path, ref="master", streamed=True, action=f.write
            )

        spinner.succeed(text=f"File saved to {localFilePath}!\n")
