import pandas as pd
from .hbond_reader import HbondReader

pd.read_hbond = HbondReader.pandas_read
