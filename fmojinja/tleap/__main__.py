from ..mixin import SubCommands
from .solvate import Solvate


SubCommands.main_proc({
    "solvate": Solvate
})