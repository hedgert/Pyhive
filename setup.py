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
                    dual_name_rules={
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
                ),
            ]
        )
    },
)
