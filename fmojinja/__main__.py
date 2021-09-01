import os
from .__version__ import get_version

print(os.linesep.join([
    f"[fmojinja{get_version()} modules]",
    "python -m fmojinja.bare_renderer",
    "python -m fmojinja.bare_makefile",
    "python -m fmojinja.abinitmp",
    "python -m fmojinja.abinitmp.reader",
    "python -m fmojinja.awk",
    "python -m fmojinja.makefile",
    "python -m fmojinja.chpi",
    "python -m fmojinja.cpptraj",
    "python -m fmojinja.cpptraj.makefile",
    "python -m fmojinja.cpptraj.reader",
    "python -m fmojinja.moebatch",
    "python -m fmojinja.plip.makefile",
    "python -m fmojinja.plip.reader",
    "python -m fmojinja.sander",
    "python -m fmojinja.tleap",
    "python -m fmojinja.gmx",
    "python -m fmojinja.sander.makefile"
])
)