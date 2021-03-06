import argparse
from ..mixin import TemplateRendererMixin
from ..__version__ import get_version
from argparse import ArgumentParser

class Equil(TemplateRendererMixin):

	@classmethod
	def template(cls):
		return f"; Generated by fmojinja version {get_version()}" + """
; Run parameters
integrator              = {{ integrator }}
nsteps                  = {{ nsteps }}
dt                      = {{ dt }}
; Output control
nstxout                 = {{ nstxout }}
nstvout                 = {{ nstvout }}
nstenergy               = {{ nstenergy }}
nstlog                  = {{ nstlog }}
nstxout-compressed      = {{ nstxoutcompressed }}
; Bond parameters
continuation            = {{ continuation }}
constraint_algorithm    = {{ constraint_algorithm }}
constraints             = {{ constraints }}
lincs_iter              = {{ lincs_iter }}
lincs_order             = {{ lincs_order }}
; Neighborsearching
cutoff-scheme           = {{ cutoffscheme }}
ns_type                 = {{ ns_type }}
nstlist                 = {{ nstlist }}
rcoulomb                = {{ rcoulomb }}
rvdw                    = {{ rvdw }}
; Electrostatics
coulombtype             = {{ coulombtype }}
pme_order               = {{ pme_order}}
fourierspacing          = {{ fourierspacing }}
; Temperature coupling is on
tcoupl                  = {{ tcoupl }}
tc-grps                 = {{ tcgrps }}
tau_t                   = {{ tau_t }}
ref_t                   = {{ ref_t }}
; Pressure coupling is on
pcoupl                  = {{ pcoupl }}
pcoupltype              = {{ pcoupltype }}
tau_p                   = {{ tau_p }}
ref_p                   = {{ ref_p }}
compressibility         = {{ compressibility }}
; Periodic boundary conditions
pbc                     = {{ pbc }}
; Dispersion correction
DispCorr                = {{ DispCorr }}
; Velocity generation
gen_vel                 = {{ gen_vel }}
"""

	@classmethod
	def set_arguments(cls, p: ArgumentParser) -> ArgumentParser:
		p = super(Equil, cls).set_arguments(p)
		p.add_argument("-int", "--integrator", default="md", help="leap-frog integrator")
		p.add_argument("-nst", "--nsteps", default=500000,help="2 * 500000 = 1000 ps (1 ns)")
		p.add_argument("-dt", "--dt", default=0.002, help="2 fs")
		p.add_argument("-nx", "--nstxout", default=5000, help="save coordinates every 10.0 ps")
		p.add_argument("-nv", "--nstvout", default=5000, help="save velocities every 10.0 ps")
		p.add_argument("-ne", "--nstenergy", default=5000, help="save energies every 10.0 ps")
		p.add_argument("-nl", "--nstlog", default=5000, help="update log file every 10.0 ps")
		p.add_argument("-nc", "--nstxoutcompressed", default=5000, help="save compressed coordinates every 10.0 ps")
		p.add_argument("-cont", "--continuation", default="yes", help="Restarting after NPT")
		p.add_argument("-ca", "--constraint_algorithm", default="lincs", help="holonomic constraints")
		p.add_argument("-const", "--constraints", default="h-bonds", help="bonds involving H are constrained")
		p.add_argument("-li", "--lincs_iter", default=1, help="accuracy of LINCS")
		p.add_argument("-lo", "--lincs_order", default=4, help="also related to accuracy")
		p.add_argument("-cs", "--cutoffscheme", default="Verlet", help="Buffered neighbor searching")
		p.add_argument("-nt", "--ns_type", default="grid", help="search neighboring grid cells")
		p.add_argument("-nstl", "--nstlist", default=10, help="20 fs, largely irrelevant with Verlet scheme")
		p.add_argument("-rc", "--rcoulomb", default=1.2, help="short-range electrostatic cutoff (in nm)")
		p.add_argument("-rd", "--rvdw", default=1.2, help="short-range van der Waals cutoff (in nm)")
		p.add_argument("-ct", "--coulombtype", default="PME", help="Particle Mesh Ewald for long-range electrostatics")
		p.add_argument("-po", "--pme_order", default=4, help="cubic interpolation")
		p.add_argument("-fs", "--fourierspacing", default=0.16, help="grid spacing for FFT")
		p.add_argument("-tc", "--tcoupl", default="V-rescale", help="modified Berendsen thermostat")
		p.add_argument("-tg", "--tcgrps", default="Protein Non-Protein", help="two coupling groups - more accurate")
		p.add_argument("-tt", "--tau_t", default="0.1     0.1", help="time constant, in ps")
		p.add_argument("-rt", "--ref_t", default="310     310", help="reference temperature, one for each group, in K")
		p.add_argument("-pc", "--pcoupl", default="Parrinello-Rahman", help="Pressure coupling on in NPT")
		p.add_argument("-pt", "--pcoupltype", default="isotropic", help="uniform scaling of box vectors")
		p.add_argument("-tp", "--tau_p", default=2.0, help="time constant, in ps")
		p.add_argument("-rp", "--ref_p", default=1.0, help="reference pressure, in bar")
		p.add_argument("-cb", "--compressibility", default="4.5e-5", help="isothermal compressibility of water, bar^-1")
		p.add_argument("-pbc", "--pbc", default="xyz", help="3-D PBC")
		p.add_argument("-dc", "--DispCorr", default="EnerPres", help="account for cut-off vdW scheme")
		p.add_argument("-gv", "--gen_vel", default="no", help="Velocity generation is off")
		return p