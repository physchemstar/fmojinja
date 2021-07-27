import os
import sys
from .mixin import TemplateRendererMixin
from argparse import ArgumentParser
from jinja2 import Environment, meta


class BareRenderer(TemplateRendererMixin):
    temp = None

    @classmethod
    def template(cls) -> str:
        if cls.temp is None:
            cls.temp = []
            for line in sys.stdin:
                try:
                    cls.temp.append(line)
                except KeyboardInterrupt:
                    exit()
        return os.linesep.join(cls.temp)

    @classmethod
    def set_arguments(cls, p: ArgumentParser) -> ArgumentParser:
        p = super(BareRenderer, cls).set_arguments(p)
        ast = Environment().parse(cls.template())
        for i in meta.find_undeclared_variables(ast):
            p.add_argument("--" + i, required=True)
        return p


if __name__ == '__main__':
    p = ArgumentParser()
    p = BareRenderer.set_arguments(p)
    a = p.parse_args()
    BareRenderer.main_proc(**vars(a))
