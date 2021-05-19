from jinja2 import Environment
from textwrap import dedent
from pathlib import Path
import sys
from argparse import ArgumentParser


class SubCommandMixin:
    template = ""

    @classmethod
    def render(cls, **kwargs):
        return Environment().from_string(dedent(cls.template)).render(**kwargs)

    @staticmethod
    def set_arguments(p):
        return p


class SubCommands:
    @staticmethod
    def main_proc(subcommands):
        p = ArgumentParser()
        p_subs = p.add_subparsers(dest="sub_command")
        for command_name, command_class in subcommands.items():
            p_sub = p_subs.add_parser(command_name, help=repr(command_class))
            p_sub = command_class.set_arguments(p_sub)
            p_sub.set_defaults(render=command_class.render)

        a = p.parse_args()

        if a.sub_command is None:
            p.print_help()
            sys.exit(0)

        print(a.render(**vars(a)))


class CpptrajMixin(SubCommandMixin):
    @staticmethod
    def set_arguments(p):
        p.add_argument("-a", "--anchor", default="@CA,C,O,N")
        p.add_argument("-m", "--mask", help="e.g. '@CA,C,O,N' ':1-100<:6.0|:NA'")
        p.add_argument("-p", "--parm", type=Path, required=True)
        p.add_argument("-y", "--trajin", type=Path, nargs="*", required=True)
        p.add_argument("-ref", "--reference", type=Path)
        p.add_argument("-am", "--align-mask", default="@CA,C,N", help="e.g.  '@CA,C,N' '@O3',C3',C4',C5',O5',P'")
        return p

