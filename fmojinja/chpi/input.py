from ..mixin import TemplateRendererMixin


class Input(TemplateRendererMixin):

    @classmethod
    def template(cls) -> str:
        return """{{ pdb }}
{{ vpi }}
{{ output }}
{{ out_mol }}
{%- for res_name in ( "{},END".format(exclude) if exclude else "END").split(",")  %}
{{ res_name }}
{%- endfor %} 
   2.00    8.00 
   2.00    3.05 
 127.50   63.00 
0
0
0
0
0
1

"""

    @classmethod
    def set_arguments(cls, p):
        p.add_argument("-p", "--pdb", required=True)
        p.add_argument("-v", "--vpi", required=True)
        p.add_argument("-o", "--output", required=True, help="e.g. output.hpi")
        p.add_argument("-m", "--out-mol", required=True)
        p.add_argument("-x", "--exclude", help="e.g. HOH,UNK")
        return super(cls, cls).set_arguments(p)

