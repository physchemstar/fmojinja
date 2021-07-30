from ...mixin import TemplateRendererMixin
from ...__version__ import get_version
from argparse import ArgumentParser


class PdbReformer(TemplateRendererMixin):

    @classmethod
    def template(cls) -> str:
        return f"# Generated by fmojinja version {get_version()}" + """
PREFIX := {{ prefix }}
PDB :={% for path in input_pdbs %} {{ path }}{% endfor %}
CHAIN_STARTS :={% for seq_id in chain_starts %} {{ seq_id }}{% endfor %}
FORMATTED_PDB := $(addsuffix .pdb, $(addprefix $(PREFIX), $(basename $(notdir $(PDB)))))

.PHONY: run
run: gen $(FORMATTED_PDB)

.PHONY: gen
gen: $(PREFIX) $(PREFIX)reformat.awk

$(PREFIX):
\tmkdir $(PREFIX)

$(PREFIX)reformat.awk:
\tpython -m fmojinja.awk reformat_pdb -c $(CHAIN_STARTS) > $@

define expr
$(PREFIX)$(basename $(notdir $(1))).pdb: $(1)
\tawk -f $(PREFIX)reformat.awk $(1) > $(PREFIX)$(basename $(notdir $(1))).pdb
endef
$(foreach i, $(PDB), $(eval $(call expr, $(i))))


.PHONY: clean
clean:
\trm $(PREFIX)*

"""

    @classmethod
    def set_arguments(cls, p: ArgumentParser) -> ArgumentParser:
        p = super(PdbReformer, cls).set_arguments(p)
        p.add_argument("-P", "--prefix", default="reformat_pdb/")
        p.add_argument("-c", "--chain-starts", nargs="*", default=[])
        p.add_argument("-i", "--input-pdbs", required=True, nargs="+")
        return p