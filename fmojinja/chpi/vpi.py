from ..mixin import TemplateRendererMixin
import yaml


class Vpi(TemplateRendererMixin):

    @classmethod
    def template(cls) -> str:
        return """
PI-system  K  L  M  VPI   N   1    2    3    4    5    6
REG   HIS  1  1  1  FIV   5   CG   ND1  CE1  NE2  CD2
REG   PHE  1  1  1  SIX   6   CG   CD1  CE1  CZ   CE2  CD2
REG   TYR  1  1  1  SIX   6   CG   CD1  CE1  CZ   CE2  CD2
REG   TRP  1  1  2  FIV   5   CG   CD1  NE1  CE2  CD2
REG   TRP  1  2     SIX   6   CE2  CD2  CE3  CZ3  CH2  CZ2
DNA    DA  1  1  2  FIV   5   N9   C8   N7   C5   C4
DNA    DA  1  2     SIX   6   C5   C4   N3   C2   N1   C6
DNA    DC  1  1  1  SIX   6   N1   C2   N3   C4   C5   C6
DNA    DG  1  1  2  FIV   5   N9   C8   N7   C5   C4
DNA    DG  1  2     SIX   6   C5   C4   N3   C2   N1   C6
DNA    DT  1  1  1  SIX   6   N1   C2   N3   C4   C5   C6
RNA    DU  1  1  1  SIX   6   N1   C2   N3   C4   C5   C6
DNA   A    1  1  2  FIV   5   N9   C8   N7   C5   C4
DNA   A    1  2     SIX   6   C5   C4   N3   C2   N1   C6
DNA   C    1  1  1  SIX   6   N1   C2   N3   C4   C5   C6
DNA   G    1  1  2  FIV   5   N9   C8   N7   C5   C4
DNA   G    1  2     SIX   6   C5   C4   N3   C2   N1   C6
DNA   T    1  1  1  SIX   6   N1   C2   N3   C4   C5   C6
RNA   U    1  1  1  SIX   6   N1   C2   N3   C4   C5   C6
{% if add_yaml_expr %}{% for k in add_yaml_expr %}{% for l in k %}{{add_name}}   {{l}}
{% endfor %}{% endfor %}{% endif %}"""

    class Additive:
        vpi = {
            2: "OLE",
            3: "OLE",
            5: "FIV",
            6: "SIX"
        }
        k = {}

        def __init__(self, expr):
            data = yaml.safe_load(expr)
            for key, values in data.items():
                self.key = key
                self.values = values
            self.i = 0

        def __iter__(self):
            return self

        def __next__(self):
            try:
                m = ""
                self.i += 1
                if self.i == 1:
                    self.set_k(self.key)
                    m = str(len(self.values))
                value = self.values.pop(0)
                line = str(self.key)
                line += f"{self.get_k(self.key): >3}"
                line += f"{self.i: >3}"
                line += f"{m: >3}"
                line += f"{self.vpi[len(value)]: >5}"
                line += f"{len(value): >4}   "
                for at in value:
                    line += f"{at: <5}"
                return line
            except IndexError:
                raise StopIteration

        @classmethod
        def set_k(cls, key):
            if key not in cls.k:
                cls.k[key] = 0
            cls.k[key] += 1

        @classmethod
        def get_k(cls, key):
            return cls.k[key]


    @classmethod
    def set_arguments(cls, p):
        p.add_argument("--add-name", default="LIG")
        p.add_argument("--add-yaml-expr", nargs="*", type=cls.Additive, help="e.g. 'RCG: [[C9,C10,C11,C12,C13,C14], [C24,C25,C26,C27,C28,C29], [C17,C18,C19,C20,C21,C22]]'")
        return super(cls, cls).set_arguments(p)

