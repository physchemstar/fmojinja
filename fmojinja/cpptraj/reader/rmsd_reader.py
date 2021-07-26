import os.path

import pandas as pd
from ...mixin import ReaderMixin
import re


class RmsdReaderMixin(ReaderMixin):

    @staticmethod
    def pandas_read(path, inpcrd_names=None, dt_per_frame=50, data_structure="long", **kwargs):
        with open(path, "r") as f:
            header = next(f)[8:]
        widths = [len(i) for i in re.findall(" *[^ ]+", header)]
        widths = [8] + widths
        df = pd.read_fwf(path, widths=widths)
        if inpcrd_names is None:
            df = df.rename({'#Frame': 'step'}, axis=1)
        else:
            frame2step = []
            for path in inpcrd_names:
                frame2step.append(int(re.findall("[0-9]+", os.path.basename(path))[0]))
            df = df.assign(step=lambda d: [frame2step[i - 1] for i in d.step])
        align_mask = [i for i in df.columns.values if i.startswith("rmsd_align")]
        df = df.rename({align_mask[0]: align_mask[0].replace("align", "")}, axis=1)
        df = df.assign(align_mask=align_mask[0].replace("rmsd_align", ""))
        df = df.assign(step=lambda d: d.step * dt_per_frame)
        if data_structure == "wide":
            return df
        df = pd.wide_to_long(df,
                             stubnames="rmsd",
                             i=["step", "align_mask"],
                             j="mask",
                             sep="_",
                             suffix=r".+").reset_index()
        return df

    @classmethod
    def set_arguments(cls, p):
        p.add_argument("files", nargs="+")
        p.add_argument("-in", "--inpcrd-names", nargs="*")
        p.add_argument("-ds", "--data-structure", default="long", choices=["long", "wide"])
        return super(cls, cls).set_arguments(p)
