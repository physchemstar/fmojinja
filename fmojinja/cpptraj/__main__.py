from ..mixin import SubCommands
from .snapshot import Snapshot
from .hbond import Hbond

SubCommands.main_proc({
    "snapshot": Snapshot,
    "hbond": Hbond,
})