from ..mixin import CpptrajMixin
from ..__version__ import get_version


class Rmsd(CpptrajMixin):

    template = f"# Generated by fmojinja version {get_version()}" + """ 
parm {{ parm }}
{%- for path in trajin %}
trajin {{ path }} 1 last {{ offset }}{% endfor %}
autoimage anchor {{ anchor }} origin
align {{ align_mask }} {{ "move {}".format(mask) if mask else "" }} {{ "ref {}".format(reference) if reference else "first" }}
rmsd {{ mask if mask else "" }} out {{ output }}
run
"""

    @classmethod
    def set_arguments(cls, p):
        p.add_argument("--offset", default=100)
        p.add_argument("-o", "--output", default="output.dat")
        return super(cls, cls).set_arguments(p)
