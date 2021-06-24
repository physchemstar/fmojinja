import pandas as pd
from .hbond_reader import HbondReaderMixin

pd.read_hbond = HbondReaderMixin.pandas_read
