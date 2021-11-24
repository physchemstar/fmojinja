from ...mixin import SubCommands

import pandas as pd
from argparse import ArgumentParser
from ...mixin import ReaderMixin

class XvgReaderMixin(ReaderMixin):

    @staticmethod
    def pandas_read(path, **kwargs) -> pd.DataFrame:
        data = []
        with open(path, "r") as f:
            for line in f:
                if line.startswith("@    title"):
                    title = line[11:].strip().strip("\" ")
                if line.startswith("@    xaxis  label"):
                    xaxis_label = line[18:].strip().strip("\" ")
                if line.startswith("@    yaxis  label"):
                    yaxis_label = line[18:].strip().strip("\" ")
                    break
            for line in f:
                if line.startswith("@"):
                    continue
                record = line.split()
                record.append(title)
                record.append(xaxis_label)
                record.append(yaxis_label)
                data.append(record)
        data = pd.DataFrame(data, columns=["x", "y", "title", "xaxis_label", "yaxis_label"])
        return data

    @classmethod
    def set_arguments(cls, p: ArgumentParser) -> ArgumentParser:
        p.add_argument("files", nargs="+")
        return super(XvgReaderMixin, cls).set_arguments(p)