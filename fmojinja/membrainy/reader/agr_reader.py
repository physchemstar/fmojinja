from ...mixin import SubCommands

import pandas as pd
from argparse import ArgumentParser
from ...mixin import ReaderMixin


class AgrReaderMixin(ReaderMixin):

    @staticmethod
    def pandas_read(path, **kwargs) -> pd.DataFrame:
        data = []
        with open(path, "r") as f:
            for line in f:
                if line.startswith("@    title"):
                    title = line[11:].strip().strip("\" ")
                if line.startswith("@    subtitle"):
                    subtitle = line[13:].strip().strip("\" ")
                if line.startswith("@target"):
                    target = line.split()[1]
                    break
            for line in f:
                if line.startswith("@target"):
                    target = line.split()[1]
                if line.startswith("@type"):
                    continue
                record = line.split()
                record.append(title)
                record.append(subtitle)
                record.append(target)
                data.append(record)
        data = pd.DataFrame(data, columns=["x", "y", "title", "subtitle", "target"])
        return data

    @classmethod
    def set_arguments(cls, p: ArgumentParser) -> ArgumentParser:
        p.add_argument("files", nargs="+")
        return super(AgrReaderMixin, cls).set_arguments(p)