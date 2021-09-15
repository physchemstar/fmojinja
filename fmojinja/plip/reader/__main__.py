from ...mixin import SubCommands
from .plip_reader import XmlReader


SubCommands.main_proc({
    "xml": XmlReader,
})
