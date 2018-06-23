import time

from rosso import __version__
from rosso.vendor import click
from rosso.vendor import feedparser
from rosso.vendor.tabulate import tabulate

APP_NAME = 'rosso'
VERSION_OPT_MSG = APP_NAME + ' %(version)s'


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
        feed = feedparser.parse(uri)
        for entry in feed.entries:
            value = entry.title
            if title == 'short' and len(value) > 10:
                value = value[:10] + '...'
            click.echo(u'title: {}'.format(value))

            value = entry.summary.replace('\r', '').replace('\n', '')
            if summary == 'short' and len(value) > 30:
                value = value[:30] + '...'
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
