import argparse
from ..mixin import TemplateRendererMixin
from ..__version__ import get_version
from argparse import ArgumentParser

class Equil(TemplateRendererMixin):

	@classmethod
	def template(cls):
		return f"; Generated by fmojinja version {get_version()}" + """
{% if define %}define       = {{ define }}{% endif %}
integrator   = {{ integrator }}
emtol        = {{ emtol }}
emstep       = {{ emstep }}
nsteps       = {{ nsteps }}
nstlist      = {{ nstlist }}
ns_type      = {{ ns_type }}
coulombtype  = {{ coulombtype }}
rcoulomb     = {{ rcoulomb }}
rvdw         = {{ rvdw }}
pbc          = {{ pbc }}

"""

	@classmethod
	def set_arguments(cls, p: ArgumentParser) -> ArgumentParser:
		p = super(Equil, cls).set_arguments(p)
		p.add_argument("-def", "--define", default=" ", help="define")
		p.add_argument("-int", "--integrator", default="steep",help="Algorithm (steep = steepest descent minimization)")
		p.add_argument("-et", "--emtol", default=1000.0, help="Stop minimization when the maximum force < 1000.0 kJ/mol/nm")
		p.add_argument("-es", "--emstep", default=0.01, help="Energy step size")
		p.add_argument("-ns", "--nsteps", default=50000, help="Maximum number of (minimization) steps to perform")
		p.add_argument("-nl", "--nstlist", default=100, help="Frequency to update the neighbor list and long range forces")
		p.add_argument("-nt", "--ns-type", default="grid", help="Method to determine neighbor list (simple, grid)")
		p.add_argument("-ct", "--coulombtype", default="PME", help="Treatment of long range electrostatic interactions")
		p.add_argument("-rc", "--rcoulomb", default=1.2, help="Short-range electrostatic cut-off")
		p.add_argument("-rv", "--rvdw", default=1.2, help="Short-range Van der Waals cut-off")
		p.add_argument("-pbc", "--pbc", default="xyz", help="Periodic Boundary Conditions (yes/no)")
		return p