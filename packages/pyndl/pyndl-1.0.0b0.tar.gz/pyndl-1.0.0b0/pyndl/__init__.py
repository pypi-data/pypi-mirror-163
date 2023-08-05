"""
Pyndl - Naive Discriminative Learning in Python
===============================================

*pyndl* is an implementation of Naive Discriminative Learning in Python. It was
created to analyse huge amounts of text file corpora. Especially, it allows to
efficiently apply the Rescorla-Wagner learning rule to these corpora.

"""

import os
import sys
import multiprocessing as mp
try:
    from importlib.metadata import requires
except ModuleNotFoundError:  # python 3.7 and before
    requires = None
try:
    from packaging.requirements import Requirement
except ModuleNotFoundError:  # this should only happend during setup phase
    Requirement = None

try:
    from importlib import metadata
    __version__ = metadata.version(__package__)
except metadata.PackageNotFoundError:
    import toml
    __version__ = toml.load("pyproject.toml")["tool"]["poetry"]["version"] + "dev"


def sysinfo():
    """
    Prints system the dependency information
    """
    if requires:
        dependencies = [Requirement(req).name for req in requires('pyndl')
                        if not Requirement(req).marker]

    header = ("Pyndl Information\n"
              "=================\n\n")

    general = ("General Information\n"
               "-------------------\n"
               "Python version: {}\n"
               "Pyndl version: {}\n\n").format(sys.version.split()[0], __version__)

    uname = os.uname()
    osinfo = ("Operating System\n"
              "----------------\n"
              "OS: {s.sysname} {s.machine}\n"
              "Kernel: {s.release}\n"
              "CPU: {cpu_count}\n").format(s=uname, cpu_count=mp.cpu_count())

    if uname.sysname == "Linux":
        _, *lines = os.popen("free -m").readlines()
        for identifier in ("Mem:", "Swap:"):
            memory = [line for line in lines if identifier in line]
            if len(memory) > 0:
                _, total, used, *_ = memory[0].split()
            else:
                total, used = '?', '?'
            osinfo += "{} {}MiB/{}MiB\n".format(identifier, used, total)

    osinfo += "\n"

    deps = ("Dependencies\n"
            "------------\n")

    if requires:
        deps += "\n".join("{pkg.__name__}: {pkg.__version__}".format(pkg=__import__(dep))
                          for dep in dependencies)
    else:
        deps = 'You need Python 3.8 or higher to show dependencies.'

    print(header + general + osinfo + deps)
