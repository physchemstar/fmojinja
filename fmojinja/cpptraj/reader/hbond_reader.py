import pandas as pd
from ...mixin import ReaderMixin


class HbondReader(ReaderMixin):

    @staticmethod
    def pandas_read(path):
        return pd.read_fwf(
            path,
            widths=[15, 16, 16, 9, 13, 13, 13],
            names=["acceptor","donor_h","donor","frames","frac","avg_dist","avg_ang"],
            comment="#")

    @classmethod
    def set_arguments(cls, p):
        p.add_argument("files", nargs="+")
        return super(cls, cls).set_arguments(p)
