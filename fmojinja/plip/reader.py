from argparse import ArgumentParser
from xml.etree.ElementTree import XML
import pandas as pd
from io import StringIO

p = ArgumentParser()
p.add_argument("xml", nargs="*")

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
            for pis in next(interactions.iter("pi_stacks")).iter("pi_stack"):
                keys = ["restype_lig", "resnr_lig", "reschain_lig", "restype", "resnr", "reschain", "centdist", "angle", "offset", "type"]
                record = dict((k, next(pis.iter(k)).text) for k in keys)
                data.append(record)
    df = pd.DataFrame(data)
    if len(a.xml) > 1:
        df = df.assign(path=path)
    if len(df) > 0:
        df.to_csv(output, index=False, header=is_first)
        output.seek(0)
        print(output.read())
        is_first=False
