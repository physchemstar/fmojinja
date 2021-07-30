from ...mixin import SubCommands
from .pdb_reformer import PdbReformer

SubCommands.main_proc({
    "reformat_pdb": PdbReformer
})
