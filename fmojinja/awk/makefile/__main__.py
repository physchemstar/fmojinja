from ...mixin import SubCommands
from .reformat_pdb import ReformatPdb

SubCommands.main_proc({
    "reformat_pdb": ReformatPdb
})
