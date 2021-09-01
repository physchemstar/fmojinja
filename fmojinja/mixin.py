from jinja2 import Environment
from textwrap import dedent
from pathlib import Path
import sys
from argparse import ArgumentParser
import pandas as pd
from typing import Dict, List, Type
from abc import abstractmethod


class SubCommand:
    """Abstract subcommand class for CLI.
    """

    @classmethod
    def main_proc(cls, **kwargs) -> None:
        pass

    @classmethod
    def set_arguments(cls, p: ArgumentParser) -> ArgumentParser:
        """ processes the given argparse.ArgumentParser for additional commandline arguments.
        This static method should be overrode for additional commandline arguments.

        :param p: parser instance
        :type p: argparse.ArgumentParser
        :return: The processed parser
        :rtype: argparse.ArgumentParser
        """

        return p


class SubCommands:
    """Methods for collections of SubCommandMixin subclasses.
    """

    @staticmethod
    def main_proc(sub_commands: Dict[str, Type[SubCommand]]) -> None:
        """Handle SubCommand children.

        :param sub_commands: {str: SumCommandMixin}:
        :return None:a rendered template (TemplateRendererMixin) or csv (ReaderMixin) is going to be printed.
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

    @classmethod
    @abstractmethod
    def template(cls) -> str:
        return ""

    @classmethod
    def main_proc(cls, **kwargs) -> None:
        sys.stdout.write(cls.render(**kwargs))

    @classmethod
    def render(cls, **kwargs) -> str:
        return Environment().from_string(dedent(cls.template())).render(**kwargs)


class ReaderMixin(SubCommand):

    @classmethod
    @abstractmethod
    def pandas_read(cls, path, **kwargs) -> pd.DataFrame:
        return pd.DataFrame(None)

    @classmethod
    def main_proc(cls, files: List[Path], **kwargs) -> None:
        is_first = True
        for path in files:
            df = cls.pandas_read(path=path, **kwargs)
            if len(files) > 1:
                df = df.assign(path=path)
            df.to_csv(sys.stdout, index=False, header=is_first)
            is_first = False


class CpptrajMixin(TemplateRendererMixin):

    @classmethod
    def set_arguments(cls, p: ArgumentParser) -> ArgumentParser:
        p = super(CpptrajMixin, cls).set_arguments(p)
        p.add_argument("-a", "--anchor", default="@CA,C,O,N", help="anchor info.")
        p.add_argument("-m", "--mask", help="mask info. e.g. '@CA,C,O,N' ':1-100<:6.0|:NA'")
        p.add_argument("-p", "--parm", type=Path, required=True, help="topology file")
        p.add_argument("-y", "--trajin", type=Path, nargs="*", required=True, help="trajectory files")
        p.add_argument("-c", "--ref", type=Path, help="reference file")
        p.add_argument("-am", "--align-mask", default="@CA,C,N", help="align mask e.g. '@CA,C,N' @O3',C3',C4',C5',O5',P")
        return p


class SanderMixin(TemplateRendererMixin):

    @classmethod
    def write_general_jinja(cls) -> str:
        return """{% set sampling_time = sampling_time if sampling_time else ((nsteps_limit / frames_per_file) | int) %}
  ntpr={{ sampling_time }}, 
  ntwr={{ sampling_time }}, 
  iwrap={{ iwrap }},
  ntwx={{ sampling_time }}, 
  ntwv={{ sampling_time }}, 
  ntwe={{ sampling_time }},
{%- if restraint_mask == None or restraint_mask == "" %}
  ntr=0,
{%- else %}
  ntr=1,
  restraintmask="{{ restraint_mask }}",
  restraint_wt={{ restraint_wt }},
{%- endif %}
  nstlim={{ nsteps_limit }},
  dt={{ delta_time }},
  ntt={{ temperature_regulation }},
  temp0={{ temperature }},
  gamma_ln={{ gamma_ln }},
  vlimit={{ vlimits }},
  pres0={{ pressure }},
  taup={{ pressure_relaxation_time }},
  cut={{ cut_off }},
  ig={{ seed }},
"""

    @classmethod
    def set_arguments(cls, p: ArgumentParser) -> ArgumentParser:
        p = super(SanderMixin, cls).set_arguments(p)
        p.add_argument("-t", "--title", help="title")
        p.add_argument("-nt", "--sampling-time", type=int)
        p.add_argument("-iwrap", default=1)
        p.add_argument("-nstlim", "--nsteps-limit", type=int, default=200000)
        p.add_argument("-dt", "--delta-time", type=float, default=0.0005)
        p.add_argument("-vl", "--vlimits", default=-1)
        p.add_argument("-cut", "--cut-off",default=12.0)
        p.add_argument("-ig", "--seed", default=-1)

        p.add_argument("-pres0", "--pressure", default=1.01)
        p.add_argument("-taup", "--pressure-relaxation-time", default=2.0)
        p.add_argument("-temp0", "--temperature", default=300)
        p.add_argument("-ntt", "--temperature-regulation", default=3)
        p.add_argument("-gl", "--gamma-ln", default=1.0)
        p.add_argument("-rm", "--restraint-mask", help="restraint mask. e.g. '!@H=' ")
        p.add_argument("-rw", "--restraint-wt", default=10, help="the weight (kcal/mol angstrom)"
                                                                 " for the positional restraints")

        p.add_argument("-fpf", "--frames-per-file", type=int, default=10)
        return p