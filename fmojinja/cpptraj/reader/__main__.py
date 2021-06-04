from ...mixin import SubCommands
from .hbond_reader import HbondReader
from .rmsd_reader import RmsdReader

SubCommands.main_proc({
    "hbond": HbondReader,
    "rmsd": RmsdReader
})

