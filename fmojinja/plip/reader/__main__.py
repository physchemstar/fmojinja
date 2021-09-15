from ...mixin import SubCommands
from .xml_reader import XmlReader


SubCommands.main_proc({
    "xml": XmlReader,
})
