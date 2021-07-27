from argparse import ArgumentParser
from xml.etree.ElementTree import XML
import pandas as pd
from io import StringIO

p = ArgumentParser()
p.add_argument("xml", nargs="+")
p.add_argument("-w", "--what", choices=["pi_stack", "hydrophobic"], default="pi_stack")

a = p.parse_args()

is_first = True
for path in a.xml:
    output = StringIO()
    data = []
    with open(path) as f:
        root = XML(f.read())
        bs = root.get("bindingsite")
        for i in root.iter("bindingsite"):
            interactions = next(i.iter("interactions"))
            if a.what == "pi_stack":
                for pis in next(interactions.iter("pi_stacks")).iter("pi_stack"):
                    keys = ["restype_lig", "resnr_lig", "reschain_lig", "restype", "resnr", "reschain", "centdist", "angle", "offset", "type"]
                    record = dict((k, next(pis.iter(k)).text) for k in keys)
                    record.update(id=pis.attrib["id"])
                    data.append(record)
            if a.what == "hydrophobic":
                for pis in next(interactions.iter("hydrophobic_interactions")).iter("hydrophobic_interaction"):
                    keys = ["restype_lig", "resnr_lig", "reschain_lig", "restype", "resnr", "reschain", "dist", "ligcarbonidx", "protcarbonidx"]
                    record = dict((k, next(pis.iter(k)).text) for k in keys)
                    record.update(id=pis.attrib["id"])
                    data.append(record)
    df = pd.DataFrame(data)
    if len(a.xml) > 1:
        if len(df) < 1:
            continue
        df = df.assign(path=path)
    df.to_csv(output, index=False, header=is_first)
    output.seek(0)
    print(output.read())
    is_first=False
