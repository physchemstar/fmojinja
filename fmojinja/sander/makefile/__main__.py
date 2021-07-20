from ...mixin import SubCommands
from .snap_min import SnapMin
from .step_prep import StepPrep
from .step_prod import StepProd

SubCommands.main_proc({
    "snap_min": SnapMin,
    "step_prep": StepPrep,
    "step_prod": StepProd
})

