from ...mixin import SubCommands
from .agr_reader import AgrReaderMixin

SubCommands.main_proc({
    "agr": AgrReaderMixin,
})