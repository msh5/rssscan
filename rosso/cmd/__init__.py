import time

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


@click.command()
@click.option('--title', default='short', type=click.Choice(['full', 'short']))
@click.option(
    '--summary', default='short', type=click.Choice(['full', 'short']))
@click.option('--pubdate', default='ja', type=click.Choice(['raw', 'ja']))
@click.argument('urls', nargs=-1)
def list(title, summary, pubdate, urls):
    for url in urls:
        feed = feedparser.parse(url)
        for entry in feed.entries:
            value = entry.title
            if title == 'short' and len(value) > TITLE_SHORTEN_LENGTH:
                value = value[:TITLE_SHORTEN_LENGTH] + '...'
            click.echo(u'title: {}'.format(value))

            value = entry.summary.replace('\r', '').replace('\n', '')
            if summary == 'short' and len(value) > SUMMARY_SHORTEN_LENGTH:
                value = value[:SUMMARY_SHORTEN_LENGTH] + '...'
            click.echo(u'summary: {}'.format(value))

            value = entry.published
            if pubdate:
                value = time.strftime('%Y-%m-%d(%a) %H:%M:%S',
                                      entry.published_parsed)
            click.echo(u'pubDate: {}'.format(value))

            # Insert a line padding between the entries
            click.echo()


cli.add_command(list)


def main():
    cli(obj={})
