import os.path

import pandas as pd
from ...mixin import ReaderMixin
import re


class RmsdReaderMixin(ReaderMixin):

    @staticmethod
    def pandas_read(path, trajin=None, data_structure="long", **kwargs):
        with open(path, "r") as f:
            header = next(f)[8:]
        widths = [len(i) for i in re.findall(" *[^ ]+", header)]
        widths = [8] + widths
        df = pd.read_fwf(path, widths=widths)
        df = df.rename({'#Frame': 'frame'}, axis=1)
        if trajin is not None:
            frame2step = []
            for path in trajin:
                frame2step.append(int(re.findall("[0-9]+", os.path.basename(path))[0]))
            df = df.assign(step=lambda d: [frame2step[i - 1] for i in d.frame])
        align_mask = [i for i in df.columns.values if i.startswith("rmsd_align")]
        df = df.rename({align_mask[0]: align_mask[0].replace("align", "")}, axis=1)
        df = df.assign(align_mask=align_mask[0].replace("rmsd_align", ""))
        if data_structure == "wide":
            return df
        df = pd.wide_to_long(df,
                             stubnames="rmsd",
                             i=["frame", "align_mask"],
                             j="mask",
                             sep="_",
                             suffix=r".+").reset_index()
        return df

    @classmethod
    def set_arguments(cls, p):
        p.add_argument("files", nargs="+")
        p.add_argument("-y", "--trajin", nargs="*")
        p.add_argument("-ds", "--data-structure", default="long", choices=["long", "wide"])
        return super(cls, cls).set_arguments(p)
