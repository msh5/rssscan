import click


class RossoEmitter(object):
    def __init__(self):
        pass

    def emit(self, body):
        # To be overwritten by derived classes
        pass


class StdoutEmitter(RossoEmitter):
    def __init__(self):
        super(StdoutEmitter, self).__init__()

    def emit(self, body):
        click.echo(body)