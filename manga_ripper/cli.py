#!/usr/bin/env python
import click
from . import Chapter, Series

# print(Series.__subclasses__())

@click.group()
def cli():
    pass


@cli.command()
@click.argument("text")
def echo(text):
    click.echo(f"You typed: {text}")


@cli.command(help="Download a full series")
@click.option(
    "--last",
    "-l",
    type=int,
    help="Download the latest x chapters",
    default=0,
)
@click.option("--site", default=None)
@click.option(
    "--select",
    "-s",
    type=int,
    help="Download select chapters",
    default=None
)
@click.argument("name")
def series(name, last, select, site):
    if site is not None:
        for site_class in Series.__subclasses__():
            if site in site_class.tags:
                Use_Series = site_class
    else:
        Use_Series = Series
    s = Use_Series(name)
    s.download(last)
    # s.download(select)


@cli.command(help="Website to dowload from")
@click.argument("websitename")
def website(websitename):
    w = websitename
    w.download()


@cli.command("list")
def websitelist():
    print("Sitename: Tags")
    print("==============")
    for site_class in Series.__subclasses__():
        print("{}: {}".format(*site_class.tags))

if __name__ == "__main__":
    cli()
