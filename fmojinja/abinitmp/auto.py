from ..mixin import SubCommandMixin
from ..__version__ import get_version


class Auto(SubCommandMixin):

    template = f"! Generated by fmojinja version {get_version()}" + """ 
&CNTRL
  Method='{{ method }}'
  Memory={{ memory }}
  ReadGeom='{{ pdb }}'
  WriteGeom='{{ geom if geom else pdb.replace(".pdb", ".cpf") }}'
  Charge={{ charge if charge else 0 }} 
  {%- if cpf_version %}
  CpfVer={{ cpf_version }} {% endif %}
  {%- if auto_frag_only %}
  Nprint=0 {% endif %}
/
&FMOCNTRL
  FMO='ON'
  NBody=2
  AutoFrag='ON'
  FragSizeResidue=1
  FragSizeAminoacid='{{ frag_size_aminoacid }}'
  FragSizeNucleotide='{{ frag_size_nucleotide }}'
  LigandCharge='{{ ligand_charge }}'
  Rsolv='{{ rsolv }}'
  NP={{ nproc_per_frag }}
/
&BASIS
  BasisSet='{{ basis_set }}'
/

"""

    @classmethod
    def set_arguments(cls, p):
        p.add_argument("--method", default="MP2")
        p.add_argument("--memory", default="6000")
        p.add_argument("-p", "--pdb", required=True)
        p.add_argument("-g", "--geom", type=str)
        p.add_argument("-c", "--charge", type=int, default=0)
        p.add_argument("-lc", "--ligand-charge", type=int)
        p.add_argument("--cpf-version")
        p.add_argument("-amino", "--frag-size-aminoacid", default="+amino")
        p.add_argument("-base", "--frag-size-nucleotide", default="+base")
        p.add_argument("--rsolv", default="Na=0.0,Br=0.0,Cl=0.0,Mg=0.0")
        p.add_argument("-np", "--nproc-per-frag", type=int, default=1)
        p.add_argument("-b", "--basis-set", default="6-31G*")
        p.add_argument("--auto-frag-only", action="store_true")
        return super(cls, cls).set_arguments(p)