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


@click.command()
@click.version_option(version=__version__, message=VERSION_OPT_MSG)
@click.option('--title', default='short', type=click.Choice(['full', 'short']))
@click.option('--desc', default='short', type=click.Choice(['full', 'short']))
@click.option('--pubdate', default='jp', type=click.Choice(['raw', 'jp']))
@click.option('--field', type=click.Choice(['title', 'desc', 'pubdate']))
@click.argument('url_or_filepaths', nargs=-1, required=True)
def scan(title, desc, pubdate, field, url_or_filepaths):
    """Scan RSS feeds and output metadata of the items"""
    for url_or_filepath in url_or_filepaths:
        try:
            pline = pipeline.ScanPipeline()

            # Support input from filename or URL
            pline.add_parser(parse.FileParser(url_or_filepath))
            pline.add_parser(parse.HTTPParser(url_or_filepath))

            # Apply cosmetic requirements to attribute values
            if title == "short":
                pline.add_filter(
                    filter_.ShortenFilter('title', TITLE_SHORTEN_LENGTH))
            if desc == "short":
                pline.add_filter(
                    filter_.ShortenFilter('description', DESC_SHORTEN_LENGTH))
            if pubdate == "jp":
                pline.add_filter(filter_.DateToJpStyleFilter())
            pline.add_filter(
                filter_.TruncateFilter('description', ['\r', '\n']))

            # Remove attributes and format as output
            if field == 'title':
                pline.add_filter(filter_.AttributeRemoveFilter('description'))
                pline.add_filter(filter_.AttributeRemoveFilter('pubDate'))
                pline.set_formatter(format_.ListFormatter())
            elif field == 'desc':
                pline.add_filter(filter_.AttributeRemoveFilter('title'))
                pline.add_filter(filter_.AttributeRemoveFilter('pubDate'))
                pline.set_formatter(format_.ListFormatter())
            elif field == 'pubdate':
                pline.add_filter(filter_.AttributeRemoveFilter('title'))
                pline.add_filter(filter_.AttributeRemoveFilter('description'))
                pline.set_formatter(format_.ListFormatter())
            else:
                assert field is None
                pline.set_formatter(format_.PPrintFormatter())

            # Emit the output to stdout
            pline.set_emitter(emit.StdoutEmitter())
            pline.run()
        except:
            click.echo(traceback.format_exc())


def main():
    scan()
