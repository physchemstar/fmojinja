from jinja2 import Environment
from textwrap import dedent
from pathlib import Path
import sys
from argparse import ArgumentParser
import pandas as pd


class SubCommand:
    """Abstract subcommand class for CLI.
    """
    @classmethod
    def main_proc(cls, **kwargs):
        """ main process

        :param kwargs:
        :return None:
        """
        pass

    @staticmethod
    def set_arguments(p):
        """ processes the given argparse.ArgumentParser for additional commandline arguments.
        This static method should be overrode for additional commandline arguments.

        :param p argparse.ArgumentParser:
        :return argparse.ArgumentParser: Processed argparse.ArgumentParser
        """

        return p


class SubCommands:
    """Methods for collections of SubCommandMixin subclasses.
    """
    @staticmethod
    def main_proc(sub_commands):
        """Handle SubCommand children.

        :param subcommands {str: SumCommandMixin}:
        :return None: rendered template (TemplateRendererMixin) or csv (ReaderMixin) is going to be printed.
        """
        import logging

        p = ArgumentParser()
        p.add_argument("-v", "--verbose", action="store_true")
        p_subs = p.add_subparsers(dest="sub_command")
        for command_name, command_class in sub_commands.items():
            p_sub = p_subs.add_parser(command_name, help=repr(command_class))
            p_sub = command_class.set_arguments(p_sub)
            p_sub.set_defaults(main_proc=command_class.main_proc)

        a = p.parse_args()
        if a.verbose:
            logging.basicConfig(level=logging.DEBUG)

        if a.sub_command is None:
            p.print_help()
            sys.exit(0)

        a.main_proc(**vars(a))


class TemplateRendererMixin(SubCommand):
    template = ""

    @classmethod
    def main_proc(cls, **kwargs):
        print(cls.render(**kwargs))

    @classmethod
    def render(cls, **kwargs):
        return Environment().from_string(dedent(cls.template)).render(**kwargs)


class ReaderMixin(SubCommand):

    @staticmethod
    def pandas_read(**kwargs):
        return pd.DataFrame(None)

    @classmethod
    def main_proc(cls, files, **kwargs):
        is_first = True
        for path in files:
            df = cls.pandas_read(path=path, **kwargs)
            if len(files) > 1:
                df = df.assign(path=path)
            df.to_csv(sys.stdout, index=False, header=is_first)
            is_first = False


class CpptrajMixin(TemplateRendererMixin):
    @staticmethod
    def set_arguments(p):
        p.add_argument("-a", "--anchor", default="@CA,C,O,N")
        p.add_argument("-m", "--mask", help="e.g. '@CA,C,O,N' ':1-100<:6.0|:NA'")
        p.add_argument("-p", "--parm", type=Path, required=True)
        p.add_argument("-y", "--trajin", type=Path, nargs="*", required=True)
        p.add_argument("-c", "--ref", type=Path)
        p.add_argument("-am", "--align-mask", default="@CA,C,N", help="e.g.  '@CA,C,N' '@O3',C3',C4',C5',O5',P'")
        return p

