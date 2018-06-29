import os
import time
import traceback

import click

from rssscan import __version__
from rssscan import emit
from rssscan import filter_
from rssscan import format_
from rssscan import parse
from rssscan import pipeline

APP_NAME = 'rssscan'
VERSION_OPT_MSG = APP_NAME + ' %(version)s'
TITLE_SHORTEN_LENGTH = 10
DESC_SHORTEN_LENGTH = 30


@click.group()
@click.version_option(version=__version__, message=VERSION_OPT_MSG)
def cli():
    pass


@click.command()
@click.option('--title', default='short', type=click.Choice(['full', 'short']))
@click.option('--desc', default='short', type=click.Choice(['full', 'short']))
@click.option('--pubdate', default='jp', type=click.Choice(['raw', 'jp']))
@click.argument('url_or_filepaths', nargs=-1)
def pprint(title, desc, pubdate, url_or_filepaths):
    """List all metadatas of RSS feed items"""
    for url_or_filepath in url_or_filepaths:
        try:
            pline = pipeline.RossoPipeline()
            pline.add_parser(parse.FileParser(url_or_filepath))
            pline.add_parser(parse.HTTPParser(url_or_filepath))
            pline.add_filter(
                filter_.TruncateFilter('description', ['\r', '\n']))
            if title == "short":
                pline.add_filter(
                    filter_.ShortenFilter('title', TITLE_SHORTEN_LENGTH))
            if desc == "short":
                pline.add_filter(
                    filter_.ShortenFilter('description', DESC_SHORTEN_LENGTH))
            if pubdate == "jp":
                pline.add_filter(filter_.DateToJpStyleFilter())
            pline.set_formatter(format_.PPrintFormatter())
            pline.set_emitter(emit.StdoutEmitter())
            pline.run()
        except:
            click.echo(traceback.format_exc())


@click.command()
@click.option('--style', default='short', type=click.Choice(['full', 'short']))
@click.argument('url_or_filepaths', nargs=-1)
def titles(style, url_or_filepaths):
    """List only titles of RSS feed items"""
    for url_or_filepath in url_or_filepaths:
        try:
            pline = pipeline.RossoPipeline()
            pline.add_parser(parse.FileParser(url_or_filepath))
            pline.add_parser(parse.HTTPParser(url_or_filepath))
            if style == "short":
                pline.add_filter(
                    filter_.ShortenFilter('title', TITLE_SHORTEN_LENGTH))
            pline.add_filter(filter_.AttributeRemoveFilter('description'))
            pline.add_filter(filter_.AttributeRemoveFilter('pubDate'))
            pline.set_formatter(format_.ListFormatter())
            pline.set_emitter(emit.StdoutEmitter())
            pline.run()
        except:
            click.echo(traceback.format_exc())


cli.add_command(pprint)
cli.add_command(titles)


def main():
    cli(obj={})
