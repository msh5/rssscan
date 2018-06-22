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
@click.argument('urls', nargs=-1)
def list(urls):
    for url in urls:
        feed = feedparser.parse(url)
        for entry in feed.entries:
            title = entry.title
            summary = entry.summary.replace('\r', '').replace('\n', '')
            pubdate = entry.published
            click.echo(u'title: {}'.format(title[:10]))
            click.echo(u'summary: {}'.format(summary[:30]))
            click.echo(u'pubDate: {}'.format(pubdate))
            click.echo()


cli.add_command(list)


def main():
    cli(obj={})
