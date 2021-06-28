from ..mixin import TemplateRendererMixin
from argparse import ArgumentParser


class ResInfo(TemplateRendererMixin):

    @classmethod
    def template(cls) -> str:
        return """#!/usr/bin/env -S moebatch -run
#svl
// Output will be printed to stderr.  Use redirect (e.g. moebatch -run input.svl 2> output.csv ).
function main []
  ReadMOE '{{ moefile }}';
  local res = Residues [];
  local res_name = rName res;
  local res_seq = rUID res;
  local res_chain = cName rChain res;
  fwrite ['*cli*','{|,}\\n', ['id','res_name', 'res_seq', 'res_chain']];
  local i;
  for i = 1, length(res), 1 loop
    fwrite ['*cli*', '{|,}\\n', [i, res_name[i], res_seq[i], res_chain[i]]];
  endloop
endfunction
"""

    @classmethod
    def set_arguments(cls, p: ArgumentParser) -> ArgumentParser:
        p = super(ResInfo, cls).set_arguments(p)
        p.add_argument("moefile")
        return p
