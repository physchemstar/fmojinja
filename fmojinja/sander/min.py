from ..mixin import TemplateRendererMixin
from ..__version__ import get_version
from argparse import ArgumentParser


class Min(TemplateRendererMixin):
    """
    e.g. python -m fmojinja.sander min > $*.in; sander -O -i $*.in -o $*.mdout -r $*.rst_opt -p $*.parm -c $< -ref $<
    """

    template = "{{ title }}" + f" !Generated by fmojinja version {get_version()}" + """ 
&cntrl
  imin=1, 
  maxcyc={{ maxcyc }}, 
  ncyc=3000,
  drms={{ drms }},
  ntr=1,
{%- if restraint_mask != None %}
  restraintmask='{{ restraint_mask }}',
  restraint_wt={{ restraint_wt }},
{%- endif %}
  ig={{ seed }},
/

"""

    @classmethod
    def set_arguments(cls, p: ArgumentParser) -> ArgumentParser:
        p = super(Min, cls).set_arguments(p)
        p.add_argument("-t", "--title", help="title for the input.")
        p.add_argument("-mc", "--maxcyc", default=10000)
        p.add_argument("--drms", default=1e-4)
        p.add_argument("-rm", "--restraint-mask", help="restraint mask. e.g. '!@H=' ")
        p.add_argument("-rw", "--restraint-wt", default=10, help="the weight (kcal/mol angstrom)"
                                                                 " for the positional restraints")
        p.add_argument("-ig", "--seed", default=-1)
        return p
