from dotenv import load_dotenv

load_dotenv("_env")

__version__ = "dev"

if "dev" in __version__:
    from pathlib import Path

    try:
        import subprocess

        basedir = Path(__file__).parent

        __version__ = (
            __version__
            + "-"
            + subprocess.check_output(
                ["git", "log", '--format="%h"', "-n 1"],
                stderr=subprocess.DEVNULL,
                cwd=basedir,
            )
            .decode("utf-8")
            .rstrip()
            .strip('"')
        )

    except Exception:  # pragma: no cover
        pass
