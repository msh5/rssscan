from distutils.core import setup

about = {}
with open('rssscan/__about__.py') as fp:
    exec(fp.read(), about)

setup(
    name='rssscan',
    version=about['__version__'],
    description='Everything goes well with RSS feeds.',
    author='Sho Minagawa',
    author_email='msh5.global@gmail.com',
    url=
    'https://msh5.kibe.la/shared/entries/10e81faa-fbe5-48fd-ad08-0db487a8e92e',
    packages=[
        'rssscan', 'rssscan/vendor', 'rssscan/vendor/click',
        'rssscan/vendor/dateutil', 'rssscan/vendor/dateutil/parser',
        'rssscan/vendor/dateutil/tz', 'rssscan/vendor/dateutil/zoneinfo'
    ],
    scripts=['bin/rssscan'])
