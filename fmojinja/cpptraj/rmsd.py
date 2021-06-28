from ..mixin import CpptrajMixin
from ..__version__ import get_version


class Rmsd(CpptrajMixin):

    @classmethod
    def template(cls) -> str:
        return f"# Generated by fmojinja version {get_version()}" + """
parm {{ parm }}
{%- for path in trajin %}
trajin {{ path }} 1 last{{ " {}".format(offset) if offset else "" }}
{%- endfor %}
{{ "reference {}".format(ref) if reference else "" }}
autoimage anchor {{ anchor }} origin
align {{ align_mask }} {{ "move {}".format(mask) if mask else "" }} {{ "ref {}".format(ref) if ref else "first" }}
rmsd rmsd_align{{ align_mask }} {{ align_mask }} out {{ output }} nofit {{ "reference" if ref else "first" }}
{% if mask_list != None %}
{%- for m in mask_list %}rmsd rmsd_{{m}} {{ m }} out {{ output }} nofit {{ "reference" if ref else "first" }}
{% endfor %}
{%- else %}rmsd {{ mask if mask else "" }} out {{ output }} nofit {{ "reference" if ref else "first" }}
{%- endif %}
run
"""

    @classmethod
    def set_arguments(cls, p):
        p.add_argument("--offset", default=1)
        p.add_argument("-ml", "--mask-list", nargs="*")
        p.add_argument("-o", "--output", default="output.dat")
        return super(cls, cls).set_arguments(p)
