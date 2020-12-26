import logging
import os
from subprocess import call
import typer
from . import server

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = typer.Typer()
app.add_typer(server.app, name="server")


@app.command("build")
def cmd_build(
    edbook_dir: str = typer.Argument(
        "../",
        help="Source files relative dir",
    ),
    output_dir: str = typer.Argument(
        "../_build",
        help="Build output relative dir",
    ),
    clean: bool = typer.Option(True, help="Delete output dir before building"),
):
    """
    Build edbook from source directory and optionally delete the output dir first.
    """
    os.chdir(edbook_dir)
    if clean:
        call(["rm", "-rf", output_dir])
    call(["make", "html"])


if __name__ == "__main__":
    app()