"""Setup pyhiveapi package."""

# pylint: skip-file
import unasync
from setuptools import setup

from pathlib import Path
import sys
project_root = Path.cwd()
sys.path.insert(0, str(project_root))

import unasync

print("=" * 80)
print("setup.py executing")
print("Python:", sys.executable)
print("unasync:", unasync.__file__)
print("unasync version:", getattr(unasync, "__version__", "<unknown>"))
print("=" * 80)

ATTRIBUTE_REPLACEMENTS = {
    ("asyncio", "current_task"): {
        "replacement": (None, "current_thread"),
        "import": ("threading", "current_thread"),
    },
    ("asyncio", "Task"): {
        "replacement": (None, "Thread"),
        "import": ("threading", "Thread"),
    },
    ("asyncio", "sleep"): {
        "replacement": ("time", "sleep"),
    },
    ("asyncio", "TimeoutError"): {
        "replacement": (None, "TimeoutError"),
    }
}

setup(
    cmdclass={
        "build_py": unasync.cmdclass_build_py(
            rules=[
                unasync.Rule(
                    "/apyhiveapi/",
                    "/pyhive/",
                    additional_replacements={
                        "apyhiveapi": "pyhive",
                    },
                    attribute_replacements=ATTRIBUTE_REPLACEMENTS,
                ),
                unasync.Rule(
                    "/apyhiveapi/api/",
                    "/pyhive/api/",
                    additional_replacements={"apyhiveapi": "pyhive"},
                    attribute_replacements=ATTRIBUTE_REPLACEMENTS,
                ),
                unasync.Rule(
                    "/apyhiveapi/devices/",
                    "/pyhive/devices/",
                    additional_replacements={
                        "apyhiveapi": "pyhive",
                    },
                    attribute_replacements=ATTRIBUTE_REPLACEMENTS,
                ),
                unasync.Rule(
                    "/apyhiveapi/session/",
                    "/pyhive/session/",
                    additional_replacements={
                        "apyhiveapi": "pyhive",
# remove as this creates at least 4 wrong code instances where replacement is not appropriate                       "asyncio": "threading",
                    },
                    attribute_replacements=ATTRIBUTE_REPLACEMENTS,
                ),
                unasync.Rule(
                    "/apyhiveapi/helper/",
                    "/pyhive/helper/",
                    additional_replacements={"apyhiveapi": "pyhive"},
                    attribute_replacements=ATTRIBUTE_REPLACEMENTS,
                ),
            ]
        )
    },
)
