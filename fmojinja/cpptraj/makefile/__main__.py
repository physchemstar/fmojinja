from ...mixin import SubCommands
from .maskpdb import MaskPdb

SubCommands.main_proc({
    "maskpdb": MaskPdb,
})