from ..mixin import SubCommands
from .min import Min
from .heat import Heating
from .dens import Density
from .equil import Equilibration
from .prod import Production


SubCommands.main_proc({
    "min": Min,
    "heat": Heating,
    "dens": Density,
    "equil": Equilibration,
    "prod": Production
})

