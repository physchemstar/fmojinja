from ..mixin import SubCommands
from .vpi import Vpi
from .input import Input

SubCommands.main_proc({
    "vpi": Vpi,
    "input": Input,
})

