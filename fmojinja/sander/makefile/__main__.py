from ...mixin import SubCommands
from .step_min import StepMin
from .step_prep import StepPrep
from .step_prod import StepProd

SubCommands.main_proc({
    "step_min": StepMin,
    "step_prep": StepPrep,
    "step_prod": StepProd
})

