from ...mixin import SubCommands
from .hbond_reader import HbondReader

SubCommands.main_proc({
    "hbond": HbondReader
})

