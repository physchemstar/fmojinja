from fmojinja.mixin import SubCommands
from fmojinja.abinitmp.reader.cpf_reader import CpfReader
from fmojinja.plip.makefile.docker import DockerMakefile
from fmojinja.plip.reader.xml_reader import XmlReader
from fmojinja.chpi.vpi import Vpi
from fmojinja.chpi.input import Input
from fmojinja.chpi.reader.hpi_reader import HpiReader


SubCommands.main_proc({
    "abinitmp_reader_cpf": CpfReader,
    "plip_makefile_docker": DockerMakefile,
    "plip_reader_xml": XmlReader,
    "chpi_vpi": Vpi,
    "chpi_input": Input,
    "chpi_reader_hpi": HpiReader,
})
