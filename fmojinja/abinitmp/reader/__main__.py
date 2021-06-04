from ...mixin import SubCommands
from .reader import CpfReader

SubCommands.main_proc({
    "cpf": CpfReader
})