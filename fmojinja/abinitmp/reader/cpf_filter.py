from __future__ import annotations
import pandas as pd
import numpy as np
import re
from logging import getLogger

logger = getLogger(__name__)

class CpfFilter:

    def __init__(self, m, n) -> None:
        self.m = m
        self.n = n
        logger.debug(self.m)
        logger.debug(self.n)
        logger.info(
            f"CpfFilter is generated. "
            f"{len(self.m) if self.m is not None else 'None'} x {len(self.n) if self.m is not None else 'None'}")

    def complete_by_all_frag_id(self, n_frag: int) -> None:
        if self.m is None:
            self.m = [i + 1 for i in range(n_frag)]
            logger.info(f"CpfFilter is completed. m: {len(self.m)}.")
        if self.n is None:
            self.n = [i + 1 for i in range(n_frag)]
            logger.info(f"CpfFilter is completed. n: {len(self.n)}.")

    @classmethod
    def by_frag_id_repr(cls,
                        m_frag_id_repr: str,
                        n_frag_id_repr: str) -> "CpfFilter":
        m = None
        n = None
        if m_frag_id_repr:
            m = re.sub(r"([0-9]+)-([0-9]+)", r"i + \1 for i in range(\2 - \1 + 1)", m_frag_id_repr)
            m = "[" + m.replace(",", "]+[") + "]"
            m = eval(m)
        if n_frag_id_repr:
            n = re.sub(r"([0-9]+)-([0-9]+)", r"i + \1 for i in range(\2 - \1 + 1)", n_frag_id_repr)
            n = "[" + n.replace(",", "]+[") + "]"
            n = eval(n)
        return cls(m, n)

    @classmethod
    def by_res_name(cls,
                    frag_name: pd.DataFrame,
                    m_include: str = None,
                    m_exclude: str = None,
                    n_include: str = None,
                    n_exclude: str = None) -> "CpfFilter":
        m_condition = np.array([True for _ in frag_name["frag_name"]])
        n_condition = np.array([True for _ in frag_name["frag_name"]])
        if m_include:
            m_include = "['" + m_include.replace(",", "']+['") + "']"
            m_include = eval(m_include)
            m_condition &= frag_name["res_name"].isin(m_include)
        if m_exclude:
            m_exclude = "['" + m_exclude.replace(",", "']+['") + "']"
            m_exclude = eval(m_exclude)
            m_condition &= ~frag_name["res_name"].isin(m_exclude)
        if n_include:
            n_include = "['" + n_include.replace(",", "']+['") + "']"
            n_include = eval(n_include)
            n_condition &= frag_name["res_name"].isin(n_include)
        if n_exclude:
            n_exclude = "['" + n_exclude.replace(",", "']+['") + "']"
            n_exclude = eval(n_exclude)
            n_condition &= ~frag_name["res_name"].isin(n_exclude)
        m = frag_name[m_condition]["frag_id"].tolist()
        n = frag_name[n_condition]["frag_id"].tolist()

        return cls(m, n)

    def filter(self, df, *, i_name="i", j_name="j") -> pd.DataFrame:
        cond_1 = df[i_name].isin(self.m) & df[j_name].isin(self.n)
        cond_2 = df[i_name].isin(self.n) & df[j_name].isin(self.m)
        result = df[cond_1 | cond_2] \
            .assign(m=lambda d: [i if i in self.m else j for i, j in zip(d[i_name], d[j_name])]) \
            .assign(n=lambda d: [j if i in self.m else i for i, j in zip(d[i_name], d[j_name])]) \
            .assign(m=lambda d: d.m.astype(int), n=lambda d: d.n.astype(int))
        return result