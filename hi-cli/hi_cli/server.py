import logging
from os import name

import typer
from seedir import FakeDir

from .utils import SFTPHosts, get_connection, list_files, delete_files

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = typer.Typer()


@app.command("delete")
def cmd_delete(
    ctx: typer.Context,
    remote_dir: str = typer.Option(..., help="Remote directory."),
):
    """
    Delete all files in remote dir.
    """
    delete_files(ctx.obj["sftp"], remote_dir)


@app.command("list")
def cmd_list(
    ctx: typer.Context,
    remote_dir: str = typer.Option(..., help="Remote directory."),
):
    """
    Delete all files in remote dir.
    """
    tree: FakeDir = list_files(ctx.obj["sftp"], remote_dir, FakeDir(remote_dir))
    print(tree.seedir(style="emoji"))


@app.command("copy")
def cmd_copy(
    ctx: typer.Context,
    local_dir: str = typer.Option("../_build", help="Local directory."),
    remote_dir: str = typer.Option(..., help="Remote root directory."),
):
    """
    TODO: Add remote cleanup option
    Copy files from local dir to remote dir.
    """
    sftp = ctx.obj["sftp"]
    sftp.mkdir(remote_dir, ignore_existing=True)
    sftp.put_dir(local_dir, remote_dir)
    sftp.close()


@app.callback()
def main(
    ctx: typer.Context,
    username: str = typer.Option(
        ...,
        prompt=True,
        envvar="HI_USERNAME",
        help='Username without "@hi.is". If the environment variable does not exist you will be prompted.',
    ),
    password: str = typer.Option(
        ...,
        prompt=True,
        hide_input=True,
        envvar="HI_PASSWORD",
        help="If the environment variable does not exist you will be prompted.",
    ),
    host: SFTPHosts = SFTPHosts.katla,
):
    """
    Create sftp connection
    """
    sftp, _ = get_connection(host, username, password)
    ctx.ensure_object(dict)
    ctx.obj["sftp"] = sftp


if __name__ == "__main__":
    app()
