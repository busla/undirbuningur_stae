import logging
import os
from subprocess import call
import typer
from . import server
from .utils import msg_info, msg_success, msg_warning

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = typer.Typer()
app.add_typer(server.app, name="server")


@app.command("build")
def cmd_build(
    source_dir: str = typer.Argument(
        "../",
        help="Source files relative dir",
    ),
    build_dir: str = typer.Argument(
        "../_build",
        help="Build output relative dir",
    ),
    clean: bool = typer.Option(True, help="Delete output dir before building"),
):
    """
    Build edbook from source directory and optionally delete the output dir first.
    """
    os.chdir(source_dir)
    if clean:
        msg_info(f"Trashing {build_dir}")
        call(["rm", "-rf", build_dir])
    msg_info(f"Building edbook from {source_dir}")
    call(["make", "html"])
    msg_success(f"Done!")


if __name__ == "__main__":
    app()