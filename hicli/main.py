import logging
import os
from pathlib import Path
from subprocess import call
from unicodedata import name
import typer
from .server import app as server_app
from .utils import msg_info, msg_success, ROOT_DIR, msg_warning

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = typer.Typer()
app.add_typer(server_app, name="server")


@app.command("build")
def cmd_build(
    source_dir: str = typer.Argument(
        ROOT_DIR.joinpath("docs"),
        help="Source files relative dir",
    ),
    build_dir: str = typer.Argument(
        ROOT_DIR.joinpath("_build"),
        help="Build output relative dir",
    ),
    builder: str = typer.Option("html", help="Builder type"),
    clean: bool = typer.Option(
        False, help="Delete the build directory before building."
    ),
):
    """
    Build edbook from source directory and optionally delete the output dir first.
    """
    if clean:
        msg_warning(f"Deleting {build_dir} before building ...")
        call(["sphinx-build", "-M", "clean", source_dir, build_dir])
    msg_info(f"Building edbook from {source_dir}")
    call(["sphinx-build", "-M", builder, source_dir, build_dir])
    msg_success(f"Done!")


if __name__ == "__main__":
    app()