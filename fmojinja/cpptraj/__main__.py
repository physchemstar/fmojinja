import sys
from enum import Enum
from argparse import ArgumentParser
from .snapshot import Snapshot


class SubCommands(Enum):
    snapshot = Snapshot


p = ArgumentParser()
p_subs = p.add_subparsers(dest="sub_command")
for s in SubCommands:
    p_sub = p_subs.add_parser(s.name, help=repr(s.value))
    p_sub = s.value.set_arguments(p_sub)
    p_sub.set_defaults(render=s.value.render)

a = p.parse_args()

if a.sub_command is None:
    p.print_help()
    sys.exit(0)

print(a.render(**vars(a)))