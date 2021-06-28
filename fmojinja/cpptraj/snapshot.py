from ..mixin import CpptrajMixin
from ..__version__ import get_version


class Snapshot(CpptrajMixin):

    @classmethod
    def template(cls) -> str:
        return f"# Generated by fmojinja version {get_version()}" + """
parm {{ parm }}
{%- for path in trajin %}
trajin {{ path }} lastframe
{%- endfor %}
autoimage anchor {{ anchor }} origin
{%- set ref = "ref {}".format(ref) if ref else "first" %}
{%- set move = "move {}".format(mask) if mask else "" %}
align {{ align_mask }} {{ move }} {{ ref }}
{% for path in trajin %}
{%- set fname = prefix ~ path.stem %}
{% if mask != None -%}
reference {{ path }} lastframe
strip !({{ mask }})
parmwrite out {{ fname }}.parm
{%- endif %}
outtraj {{ fname }}.pdb trajout onlyframes {{ loop.index }} nobox pdbter topresnum
trajout {{ fname }}.rst onlyframes {{ loop.index }}
{% if mask != None -%}
unstrip
{%- endif -%}
{% endfor %}

run
"""

    @classmethod
    def set_arguments(cls, p):
        p.add_argument("--prefix", default="snapshots/")
        return super(cls, cls).set_arguments(p)
