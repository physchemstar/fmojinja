import os


print(os.linesep.join([
    "[fmojinja modules]",
    "python -m fmojinja.abinitmp",
    "python -m fmojinja.abinitmp.reader",
    "python -m fmojinja.chpi",
    "python -m fmojinja.cpptraj",
    "python -m fmojinja.cpptraj.reader",
    "python -m fmojinja.sander"
])
)