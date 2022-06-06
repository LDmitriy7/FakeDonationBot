from . import commands
from . import handlers
from . import middlewares
from . import tasks


def init():
    handlers.setup()
    middlewares.setup()
    tasks.setup()
    commands.setup()
