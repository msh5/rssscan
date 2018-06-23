import os
import time
import traceback

from rosso import __version__
from rosso.vendor import click
from rosso.vendor import feedparser
from rosso.vendor.tabulate import tabulate

APP_NAME = 'rosso'
VERSION_OPT_MSG = APP_NAME + ' %(version)s'
TITLE_SHORTEN_LENGTH = 10
SUMMARY_SHORTEN_LENGTH = 30


@click.group()
@click.version_option(version=__version__, message=VERSION_OPT_MSG)
def cli():
    pass


def pprint_entries(url_or_file, title_style, desc_style, pubdate_style):
    feed = feedparser.parse(url_or_file)
    for entry in feed.entries:
        value = entry.title
        if title_style == 'short' and len(value) > TITLE_SHORTEN_LENGTH:
            value = value[:TITLE_SHORTEN_LENGTH] + '...'
        click.echo(u'title: {}'.format(value))

        value = entry.summary
        # Sanitize the description which might include CRLFs
        value = value.replace('\r', '').replace('\n', '')
        if desc_style == 'short' and len(value) > SUMMARY_SHORTEN_LENGTH:
            value = value[:SUMMARY_SHORTEN_LENGTH] + '...'
        click.echo(u'description: {}'.format(value))

        value = entry.published
        if pubdate_style == 'ja':
            value = time.strftime('%Y-%m-%d(%a) %H:%M:%S',
                                  entry.published_parsed)
        click.echo(u'pubDate: {}'.format(value))

        # Insert a line padding between the entries
        click.echo()


def list_titles(url_or_file, style):
    feed = feedparser.parse(url_or_file)
    for entry in feed.entries:
        value = entry.title
        if style == 'short' and len(value) > TITLE_SHORTEN_LENGTH:
            value = value[:TITLE_SHORTEN_LENGTH] + '...'
        click.echo(value)


@click.command()
@click.option('--title', default='short', type=click.Choice(['full', 'short']))
@click.option('--desc', default='short', type=click.Choice(['full', 'short']))
@click.option('--pubdate', default='ja', type=click.Choice(['raw', 'ja']))
@click.argument('url_or_filepaths', nargs=-1)
def pprint(title, desc, pubdate, url_or_filepaths):
    for url_or_filepath in url_or_filepaths:
        try:
            if os.path.exists(url_or_filepath):
                with open(url_or_filepath) as fp:
                    pprint_entries(fp, title, desc, pubdate)
            else:
                pprint_entries(url_or_filepath, title, desc, pubdate)
        except:
            click.echo(traceback.format_exc())


@click.command()
@click.option('--style', default='short', type=click.Choice(['full', 'short']))
@click.argument('url_or_filepaths', nargs=-1)
def titles(style, url_or_filepaths):
    for url_or_filepath in url_or_filepaths:
        try:
            if os.path.exists(url_or_filepath):
                with open(url_or_filepath) as fp:
                    list_titles(fp, style)
            else:
                list_titles(url_or_filepath, style)
        except:
            click.echo(traceback.format_exc())


cli.add_command(pprint)
cli.add_command(titles)


def main():
    cli(obj={})
