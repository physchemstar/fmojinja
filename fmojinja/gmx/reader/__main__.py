from ...mixin import SubCommands
from .xvg_reader import XvgReaderMixin

SubCommands.main_proc({
    "xvg": XvgReaderMixin,
})