from ..mixin import SubCommandMixin


class Vpi(SubCommandMixin):
    template = """
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
"""