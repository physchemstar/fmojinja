from ...mixin import SubCommands
from .docker import DockerMakefile

SubCommands.main_proc({
    "docker": DockerMakefile
})