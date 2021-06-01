from argparse import ArgumentParser
import pandas as pd
from io import StringIO

p = ArgumentParser()
p.add_argument("dat", nargs="*")
a = p.parse_args()

is_first = True
for path in a.dat:
    output = StringIO()
    df = pd.read_fwf(path,
                     widths=[15, 16, 16, 9, 13, 13, 13],
                     names=["acceptor","donor_h","donor","frames","frac","avg_dist","avg_ang"],
                     comment="#")
    #df.columns.rename([i.replace("#", "") for i in df.columns.values])
    if len(a.dat) > 1:
        df = df.assign(path=path)
    df.to_csv(output, index=False, header=is_first)
    output.seek(0)
    print(output.read())
    is_first = False
