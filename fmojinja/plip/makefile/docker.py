from fmojinja.mixin import TemplateRendererMixin


class DockerMakefile(TemplateRendererMixin):
    """

    """

    @classmethod
    def template(cls):
        return """
XML := {% for i in pdb %}{{i.replace(".pdb", ".xml")}} \\
{% endfor %}
DOCKER := docker

.PHONY: run
run: ${XML}

.PHONY: clean
clean:
\trm -f ${XML}

%.xml: %.pdb
\tMSYS_NO_PATHCONV=1 \
\t$(DOCKER) run --rm \\
\t-v ${PWD}:/results \\
\t-w /results \\
\t-u $(id -u ${USER}):$(id -g ${USER}) \\
\tpharmai/plip:latest \
--nohydro \
{{ "-v " if verbose }}\
{{ "-nofixfile " if verbose }}\
{{ "--breakcomposite " if breakcomposite }}\
{{ "--peptides " + " ".join(peptides) + " " if peptides }}\
{{ "--intra {} ".format(intra) if intra }}\
{{ "--keepmod " if keepmod }}\
{{ "--dnareceptor " if dnareceptor }}\\
{{ "\t--hydroph_dist_max {} ".format(hydroph_dist_max) if hydroph_dist_max }}\\
{{ "\t--hbond_dist_max {} ".format(hbond_dist_max) if hbond_dist_max }}\\
{{ "\t--pistack_dist_max {} ".format(pistack_dist_max) if pistack_dist_max }}\\
{{ "\t--pistack_offset_max {} ".format(pistack_offset_max) if pistack_offset_max }}\\
{{ "\t--pication_dist_max {} ".format(pication_dist_max) if pication_dist_max }}\\
{{ "\t--saltbridge_dist_max {} ".format(saltbridge_dist_max) if saltbridge_dist_max }}\\
{{ "\t--halogen_dist_max {} ".format(halogen_dist_max) if halogen_dist_max }}\\
\t-x \\
\t-f $< \\
\t-O > $@
\tif [ ! -d 'plipfixed' ]; then mkdir plipfixed ||:; fi
\tmv plipfixed.*.pdb plipfixed ||:

"""

    @staticmethod
    def set_arguments(p):
        # https://github.com/pharmai/plip/blob/master/plip/basic/config.py
        p.add_argument("pdb", nargs="+", help="pdb files")
        p.add_argument("-v", "--verbose", dest="verbose", default=False, action="store_true")
        p.add_argument("--nofixfile", action="store_true", help="Turns off writing files for fixed PDB files.")
        p.add_argument("--breakcomposite", dest="breakcomposite", default=False, help="Don't combine ligand fragments with covalent bonds but treat them as single ligands for the analysis.", action="store_true")
        ligandtype = p.add_mutually_exclusive_group()  # Either peptide/inter or intra mode
        ligandtype.add_argument("--peptides", "--inter", dest="peptides", default=[], help="Allows to define one or multiple chains as peptide ligands or to detect inter-chain contacts", nargs="+")
        ligandtype.add_argument("--intra", dest="intra", default="A", help="Allows to define one chain to analyze intra-chain contacts.")
        p.add_argument("--keepmod", dest="keepmod", default=False, help="Keep modified residues as ligands", action="store_true")
        p.add_argument("--dnareceptor", dest="dnareceptor", default=True, help="Treat nucleic acids as part of the receptor structure (together with any present protein) instead of as a ligand.", action="store_true")
        p.add_argument("--hydroph_dist_max", default=4.0 + 5.9, help="Distance cutoff for detection of hydrophobic contacts")

        p.add_argument("--hbond_dist_max", default=4.1, help="Max. distance between hydrogen bond donor and acceptor (Hubbard & Haider, 2001) + 0.6 A")

        p.add_argument("--pistack_dist_max", default=5.5 + 4.4, help="Max. distance for parallel or offset pistacking (McGaughey, 1998)")
        p.add_argument("--pistack_offset_max", default=2.0, help="Maximum offset of the two rings (corresponds to the radius of benzene + 0.5 A)")

        p.add_argument("--pication_dist_max", default=6.0 + 3.9, help="Max. distance between charged atom and aromatic ring center (Gallivan and Dougherty, 1999)")

        p.add_argument("--saltbridge_dist_max", default=5.5 + 4.4, help="Max. distance between centers of charge for salt bridges (Barlow and Thornton, 1983) + 1.5")
        p.add_argument("--halogen_dist_max", default=4.0 + 5.9, help="Max. distance between oxy. and halogen (Halogen bonds in biological molecules., Auffinger)+0.5")
        return p