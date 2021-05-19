from jinja2 import Environment
from pathlib import Path
from textwrap import dedent


class SubCommandMixin:
    template = ""

    @classmethod
    def render(cls, **kwargs):
        return Environment().from_string(dedent(cls.template)).render(**kwargs)

    @staticmethod
    def set_arguments(p):
        p.add_argument("-a", "--anchor", default="@CA,C,O,N")
        p.add_argument("-m", "--mask", help="e.g. '@CA,C,O,N' ':1-100<:6.0|:NA'")
        p.add_argument("-p", "--parm", type=Path, required=True)
        p.add_argument("-y", "--trajin", type=Path, nargs="*", required=True)
        p.add_argument("-ref", "--reference", type=Path)
        p.add_argument("-am", "--align-mask", default="@CA,C,N", help="e.g.  '@CA,C,N' '@O3',C3',C4',C5',O5',P'")
        return p
