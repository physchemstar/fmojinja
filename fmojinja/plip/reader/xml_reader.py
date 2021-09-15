import pandas as pd
from xml.etree.ElementTree import XML
from argparse import ArgumentParser
from ...mixin import ReaderMixin


class XmlReader(ReaderMixin):
    @staticmethod
    def pandas_read(path, what="pi_stack", **kwargs) -> pd.DataFrame:
        data = []
        with open(path) as f:
            root = XML(f.read())
            for i in root.iter("bindingsite"):
                interactions = next(i.iter("interactions"))
                if what == "pi_stack":
                    for pis in next(interactions.iter("pi_stacks")).iter("pi_stack"):
                        keys = ["restype_lig", "resnr_lig", "reschain_lig", "restype", "resnr", "reschain", "centdist", "angle", "offset", "type"]
                        record = dict((k, next(pis.iter(k)).text) for k in keys)
                        record.update(id=pis.attrib["id"])
                        data.append(record)
                if what == "hydrophobic":
                    for pis in next(interactions.iter("hydrophobic_interactions")).iter("hydrophobic_interaction"):
                        keys = ["restype_lig", "resnr_lig", "reschain_lig", "restype", "resnr", "reschain", "dist", "ligcarbonidx", "protcarbonidx"]
                        record = dict((k, next(pis.iter(k)).text) for k in keys)
                        record.update(id=pis.attrib["id"])
                        data.append(record)
        return pd.DataFrame(data)

    @classmethod
    def set_arguments(cls, p: ArgumentParser) -> ArgumentParser:
        p.add_argument("files", nargs="+")
        p.add_argument("-w", "--what", choices=["pi_stack", "hydrophobic"], default="pi_stack")
        return p