from enum import Enum
from chinstrap.languages import ligo
from chinstrap.languages import smartpy
from chinstrap.helpers import startSpinner
from chinstrap.helpers import IsChinstrapProject


class Compiler:
    @IsChinstrapProject()
    def __init__(self, args, config, chinstrapPath) -> None:
        if config.compiler.lang == "smartpy":
            self.compile = smartpy.SmartPy(args, config, chinstrapPath)

        elif "ligo" in config.compiler.lang:
            self.compile = ligo.Ligo(args, config, chinstrapPath)

    def compileSources(self):
        return self.compile.compileSources()

    def compileOne(self, contract):
        return self.compile.compileOne(contract)


class Compilers(Enum):
    all = "all"
    smartpy = "smartpy"
    ligo = "ligo"

    def __str__(self):
        return self.value


def installSmartPyCompiler(local: bool, force: bool):
    smartpy.SmartPy.installCompiler(local, force)

def installLigoCompiler(local: bool, force: bool):
    # Currently ligo is compiled only for Linux
    # and is available as docker for mac.
    ligo.Ligo.installCompiler(local, force)


def installCompiler(compiler: Compilers, local: bool, force: bool):

    if compiler == Compilers.all:
        installLigoCompiler(local, force)
        installSmartPyCompiler(local, force)

    elif compiler == Compilers.smartpy:
        installSmartPyCompiler(local, force)

    elif compiler == Compilers.ligo:
        installLigoCompiler(local, force)
