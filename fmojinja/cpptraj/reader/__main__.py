from ...mixin import SubCommands
from .hbond_reader import HbondReaderMixin
from .rmsd_reader import RmsdReaderMixin

SubCommands.main_proc({
    "hbond": HbondReaderMixin,
    "rmsd": RmsdReaderMixin
})

