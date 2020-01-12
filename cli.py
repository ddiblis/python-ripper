#!/usr/bin/env python
import click
from working import Chapter, Series


@click.group()
def cli():
    pass


@cli.command()
@click.argument("text")
def echo(text):
    click.echo(f"You typed: {text}")


@cli.command()
@click.argument("chapter")
def chapter_echo(chapter):
    chap = Chapter(chapter)
    for p in chap.page_list:
        page = chap.generate_page(p)
        click.echo(page.image)


@cli.command(help="Download a full series")
@click.option(
    "--last",
    "-l",
    type=int,
    help="Download the latest x chapters",
    default=None,
)
@click.argument("name")
def series(name, last):
    s = Series(name)
    s.download(last)


@cli.command(help="Website to dowload from")
@click.argument("websitename")
def website(websitename):
    w = websitename
    w.download()


if __name__ == "__main__":
    cli()
