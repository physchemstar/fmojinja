import pandas as pd
from ...mixin import ReaderMixin
import re


class RmsdReaderMixin(ReaderMixin):

    @staticmethod
    def pandas_read(path, dt_per_frame=50, **kwargs):
        with open(path, "r") as f:
            header = next(f)[8:]
        widths = [len(i) for i in re.findall(" *[^ ]+", header)]
        widths = [8] + widths
        df = pd.read_fwf(path, widths=widths).rename({'#Frame': 'step'}, axis=1)
        align_mask = [i for i in df.columns.values if i.startswith("rmsd_align")]
        df = df.rename({align_mask[0]: align_mask[0].replace("align", "")}, axis=1)
        df = df.assign(align_mask=align_mask[0].replace("rmsd_align", ""))
        df = df.assign(step=lambda d: d.step * dt_per_frame)
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
        p.add_argument("-dt", "--dt-per-frame", default=50)
        return super(cls, cls).set_arguments(p)
