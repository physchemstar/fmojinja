from ...__version__ import get_version
from ...mixin import TemplateRendererMixin
from jinja2 import Environment
from argparse import ArgumentParser
from ...jinja_filters import broadcast_n
from pathlib import Path


class StepProd(TemplateRendererMixin):

    @classmethod
    def template(cls) -> str:
        return f"# Generated by fmojinja version {get_version()}" + """
MD_ENGINE = sander # e.g. sander, pmemd, pmemd.cuda, mpi -n 8 pmemd.MPI
PREFIX := {{ prefix }}
PS_OFFSET := {{ (delta_time * nsteps_limit) | int }}
PS_END := {{ (delta_time * nsteps_limit * nsteps) | int }}
PS_PROD_START := {{ (delta_time * nsteps_limit * nsteps_offset) | int }}
PROD_SEQ := $(shell seq $(PS_END) -$(PS_OFFSET) $(shell expr $(PS_PROD_START) + 1))

define wrap_num_w_tag
$(shell awk 'BEGIN{\
d[1]="a";d[2]="b";d[3]="c";d[4]="d";d[5]="e";d[6]="f";d[7]="g";d[8]="h";d[9]="i";\
print d[length($(1))] "." int($(1))}')
endef


.PHONY: gen
gen: $(PREFIX).prmtop $(PREFIX).mdin
$(PREFIX).prmtop:
\tcp {{ prmtop }} $@
$(PREFIX).$(call wrap_num_w_tag, $(PS_PROD_START)).restrt:
\tcp {{ inpcrd }} $@
$(PREFIX).mdin:
\tpython -m fmojinja.sander prod\
{%- if title %} -t {{ title }} {%- else %} -t prod{% endif %}\
{%- if restraint_mask %} -rm "{{ restraint_mask }}" -rw {{ restraint_wt }}{% endif %}\
{{ " -gl {}".format(gamma_ln) if gamma_ln else "" }}\
{{ " -temp0 {}".format(temperature) if temperature else "" }}\
{{ " -pres0 {}".format(pressure) if pressure else "" }}\
{{ " -nt {}".format(sampling_time) if sampling_time else "" }}\
{{ " -nstlim {}".format(nsteps_limit) if nsteps_limit else "" }}\
{{ " -dt {}".format(delta_time) if delta_time else "" }}\
{{ " -cut {}".format(cut_off) if cut_off else "" }}\
{{ " -ig {}".format(seed) if seed else "" }} > $@


.PHONY: run
run: gen $(PREFIX).$(call wrap_num_w_tag, $(PS_END)).restrt

# sequential makefile rules expressions
# $<, $@ cannot be used in rules.
define sander_expr # e.g. (3000, 1000) -> $(prefix).d.3000.$(suffix): $(prefix).d.2000.$(suffix)
$(PREFIX).$(call wrap_num_w_tag, $(1)).restrt: $(PREFIX).$(call wrap_num_w_tag, $(shell expr $(1) - $(2))).restrt
\t$(MD_ENGINE) -O \\
\t-i $(PREFIX).mdin \\
\t-o $(PREFIX).$(call wrap_num_w_tag, $(1)).mdout \\
\t-p $(PREFIX).prmtop \\
\t-c $(PREFIX).$(call wrap_num_w_tag, $(shell expr $(1) - $(2))).restrt \\
\t-ref $(PREFIX).a.0.restrt \\
\t-r $(PREFIX).$(call wrap_num_w_tag, $(1)).restrt \\
\t-x $(PREFIX).$(call wrap_num_w_tag, $(1)).mdcrd \\
\t-inf $(PREFIX).$(call wrap_num_w_tag, $(1)).mdinfo 
endef
$(foreach i, $(PROD_SEQ), $(eval $(call sander_expr, $(i), $(PS_OFFSET))))


.PHONY: clean
clean:
\trm $(PREFIX)*.* 

"""

    @classmethod
    def render(cls, **kwargs) -> str:
        env = Environment()
        env.filters["broadcast"] = broadcast_n(kwargs.get("nsteps"))
        return env.from_string(cls.template()).render(**kwargs)

    @classmethod
    def set_arguments(cls, p: ArgumentParser) -> ArgumentParser:
        p = super(StepProd, cls).set_arguments(p)
        p.add_argument("-P", "--prefix", default="prod")
        p.add_argument("-ns", "--nsteps", required=True, type=int, help="number of steps")
        p.add_argument("-no", "--nsteps-offset", default=0, type=int, help="number of steps offset")

        p.add_argument("-p", "--prmtop", type=Path, required=True)
        p.add_argument("-c", "--inpcrd", type=Path, required=True)
        p.add_argument("-t", "--title", help="title for the input.")
        p.add_argument("-nt", "--sampling-time", type=int)
        p.add_argument("-nstlim", "--nsteps-limit", type=int, default=2000000)
        p.add_argument("-dt", "--delta-time", type=float, default=0.0005)

        p.add_argument("-cut", "--cut-off", default=12.0)
        p.add_argument("-rm", "--restraint-mask", help="restraint mask. e.g. '!@H=' ")
        p.add_argument("-rw", "--restraint-wt", help="the weight (kcal/mol angstrom) for the positional restraints")
        p.add_argument("-ig", "--seed", default=-1)
        return p
