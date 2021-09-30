from ...mixin import SubCommands
from .snap_min import SnapMin

SubCommands.main_proc({
    "snap_min": SnapMin,
})