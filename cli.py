from enum import Enum
from pathlib import Path
import typer


class SFTPHosts(str, Enum):
    hekla = "hekla.rhi.hi.is"
    katla = "katla.rhi.hi.is"


app = typer.Typer()


@app.command("deploy")
def main(
    username: str = typer.Option(
        ...,
        prompt=True,
        envvar="HI_USERNAME",
        help="HÍ username. If the environment variable does not exist you will be prompted.",
    ),
    password: str = typer.Option(
        ...,
        prompt=True,
        hide_input=True,
        envvar="HI_PASSWORD",
        help="HÍ password. If the environment variable does not exist you will be prompted.",
    ),
    host: SFTPHosts = SFTPHosts.katla,
    remote_dir: Path = typer.Argument(..., help="default sftp host"),
):

    typer.secho(
        "Validate login ...",
        fg=typer.colors.BLUE,
        bold=True,
        bg=typer.colors.RESET,
    )


if __name__ == "__main__":
    typer.run(main)
