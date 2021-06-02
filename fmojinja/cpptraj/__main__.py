from ..mixin import SubCommands
from .snapshot import Snapshot
from .hbond import Hbond
from .rmsd import Rmsd

SubCommands.main_proc({
    "snapshot": Snapshot,
    "hbond": Hbond,
    "rmsd": Rmsd
})