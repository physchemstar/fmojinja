from ...mixin import SubCommands
from .cpf_reader import CpfReader

SubCommands.main_proc({
    "cpf": CpfReader
})