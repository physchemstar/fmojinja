from ..mixin import SubCommands
from .snapshot import Snapshot
from .hbond import Hbond
from .rmsd import Rmsd
from .reduce_frames import ReduceFrames
from .split import Split

SubCommands.main_proc({
    "snapshot": Snapshot,
    "hbond": Hbond,
    "rmsd": Rmsd,
    "reduce_frames": ReduceFrames,
    "split": Split
})