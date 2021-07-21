from ..mixin import SubCommands
from .min import Min
from .equil import Equil


SubCommands.main_proc({"min": Min, "equil": Equil})