from ..mixin import SubCommands
from .snapshot import Snapshot

SubCommands.main_proc({
    "snapshot": Snapshot
})