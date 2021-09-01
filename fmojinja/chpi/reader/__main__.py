from ...mixin import SubCommands
from .hpi_reader import HpiReader

SubCommands.main_proc({
    "hpi": HpiReader
})
