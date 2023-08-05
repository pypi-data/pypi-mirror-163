#!/usr/bin/env python

import test
from tkinter import W

import rich_click as click
from click_shell import shell

import get

click.rich_click.OPTION_GROUPS = {
    "mytool": [
        {
            "name": "Simple options",
            "options": ["--name", "--description", "--version", "--help"],
        },
        {
            "name": "Advanced options",
            "options": ["--force", "--yes", "--delete"],
        },
    ]
}

def print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    version_file = open("version.txt", "r")
    version = version_file.read()
    version_file.close()
    click.echo(version)
    ctx.exit()


@shell(prompt="ff > ", intro="Starting ff...")
@click.option(
    "--version",
    is_flag=True,
    callback=print_version,
    expose_value=False,
    is_eager=True,
)
@click.pass_context
def cli(ctx):

    # TODO: Pass something if needed in near future
    ctx.obj = {}


cli.add_command(get.get)
cli.add_command(test.test)

if __name__ == "__main__":

    cli()
