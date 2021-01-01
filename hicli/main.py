import logging
from subprocess import call
import typer
from typer.params import Argument
from .server import app as server_app
from .utils import msg_debug, msg_info, msg_success, ROOT_DIR, msg_warning

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = typer.Typer()
app.add_typer(server_app, name="server")


@app.command("run")
def cmd_build():
    """
    Run a simple webserver that loads the build dir
    """
    call(
        [
            "python",
            "-m",
            "http.server",
            "8000",
            "--directory",
            ROOT_DIR.joinpath("_build", "html"),
        ]
    )


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
    builder: str = typer.Option("html", "--builder", "-b", help="Builder type"),
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


@app.command(
    "autobuild",
    context_settings={"allow_extra_args": True, "ignore_unknown_options": True},
)
def cmd_autobuild(
    ctx: typer.Context,
    source_dir: str = typer.Argument(
        ROOT_DIR.joinpath("docs"),
        help="Source files relative dir",
    ),
    build_dir: str = typer.Argument(
        ROOT_DIR.joinpath("_build"),
        help="Build output relative dir",
    ),
):
    """
    TODO: Needs work. Write a simple wrapper for sphinx-autobuild.
    """
    # help_args = ["--help", "-h"]
    # for item in ctx.args:
    #     print(item)
    # if any(item in help_args for item in ctx.args):
    #     print("W00b")
    #     call(["sphinx-autobuild", *ctx.args])
    #     raise typer.Exit()
    call(["sphinx-autobuild", source_dir, build_dir, *ctx.args])


if __name__ == "__main__":
    app()