"""Setup pyhiveapi package."""

# pylint: skip-file
import unasync
from setuptools import setup

from pathlib import Path
import sys
project_root = Path.cwd()
sys.path.insert(0, str(project_root))
from _build import PyHiveUnasyncRule

import unasync

print("=" * 80)
print("setup.py executing")
print("Python:", sys.executable)
print("unasync:", unasync.__file__)
print("unasync version:", getattr(unasync, "__version__", "<unknown>"))
print("=" * 80)

setup(
    cmdclass={
        "build_py": unasync.cmdclass_build_py(
            rules=[
                PyHiveUnasyncRule(
                    "/apyhiveapi/",
                    "/pyhive/",
                    additional_replacements={
                        "apyhiveapi": "pyhive",
                    },
                ),
                PyHiveUnasyncRule(
                    "/apyhiveapi/api/",
                    "/pyhive/api/",
                    additional_replacements={"apyhiveapi": "pyhive"},
                ),
                PyHiveUnasyncRule(
                    "/apyhiveapi/devices/",
                    "/pyhive/devices/",
                    additional_replacements={
                        "apyhiveapi": "pyhive",
                    },
                ),
                PyHiveUnasyncRule(
                    "/apyhiveapi/session/",
                    "/pyhive/session/",
                    additional_replacements={
                        "apyhiveapi": "pyhive",
# remove as this creates at least 4 wrong code instances where replacement is not appropriate                       "asyncio": "threading",
                    },
                ),
                PyHiveUnasyncRule(
                    "/apyhiveapi/helper/",
                    "/pyhive/helper/",
                    additional_replacements={"apyhiveapi": "pyhive"},
                ),
            ]
        )
    },
)
