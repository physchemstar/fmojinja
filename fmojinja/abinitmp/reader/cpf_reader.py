from __future__ import annotations
import pandas as pd
import numpy as np
import math
import re
from logging import getLogger
from ...mixin import ReaderMixin
from typing import Type, Dict, Any, List, Optional
from argparse import ArgumentParser

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
            m_condition &= frag_name["frag_name"].str.rstrip("0123456789").isin(m_include)
        if m_exclude:
            m_exclude = "['" + m_exclude.replace(",", "']+['") + "']"
            m_exclude = eval(m_exclude)
            m_condition &= ~frag_name["frag_name"].str.rstrip("0123456789").isin(m_exclude)
        if n_include:
            n_include = "['" + n_include.replace(",", "']+['") + "']"
            n_include = eval(n_include)
            n_condition &= frag_name["frag_name"].str.rstrip("0123456789").isin(n_include)
        if n_exclude:
            n_exclude = "['" + n_exclude.replace(",", "']+['") + "']"
            n_exclude = eval(n_exclude)
            n_condition &= ~frag_name["frag_name"].str.rstrip("0123456789").isin(n_exclude)
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


class CpfReader(ReaderMixin):

    @staticmethod
    def get_opt_singleton() -> "Type[OptSingleton]":
        class OptSingleton:
            _i: int = 0
            _j: int = 0
            _dtype: Dict[str, str] = {
                "id": "int",
                "atom": "string",
                "atom_type": "string",
                "res_name": "string",
                "res_seq": "int",
                "frag_id": "int",
                "x": "float",
                "y": "float",
                "z": "float",
                "chain_name": "string",
                "chain_id": "string",
                "i": "int",
                "j": "int",
                "bda": "int",
                "baa": "int",
                "bond_type": "float",  # for NaN
                "dist": "float",
            }

            @classmethod
            def create(cls,
                       header: str = None,
                       nrows: int = 0,
                       widths: List[int] = None,
                       names: List[str] = None,
                       dtype_add: Dict[str, str] = None) -> Dict[str, Any]:
                if dtype_add is None:
                    dtype_add = {}
                cls._i += cls._j
                cls._j = nrows
                return {
                    "header": header,
                    "skiprows": cls._i,
                    "nrows": cls._j,
                    "widths": widths,
                    "names": names,
                    "dtype": dict(cls._dtype, **dtype_add),
                    "compression": "infer",
                }

            @classmethod
            def proceed_position(cls, n) -> None:
                cls._i += n
                cls._j += 0
        return OptSingleton

    @staticmethod
    def format_mem_limit(mem_limit: str) -> int:
        mem_limit = str(mem_limit).replace("M", "* (10**6)").replace("G", "* (10**9)")
        mem_limit = eval(mem_limit.replace("B", ""))
        return mem_limit

    @staticmethod
    def pandas_read(path,
                    what="frag_name",
                    m=None,
                    n=None,
                    label=True,
                    *,
                    m_include=None,
                    m_exclude=None,
                    n_include=None,
                    n_exclude=None,
                    parallel=False,
                    nproc=None,
                    mem_limit=10 ** 8,
                    chunk_ratio=0.05,
                    **kwargs) -> Optional[pd.DataFrame, pd.Series]:
        """
        Cpf file reader
        :param path:
        :param what:
        :param m:
        :param n:
        :param m_include:
        :param m_exclude:
        :param n_include:
        :param n_exclude:
        :param parallel:
        :param nproc:
        :param mem_limit:
        :param chunk_ratio:
        :param kwargs:
        :return pandas.DataFrame or numpy.Series: depended on what param
        """
        opt_singleton = CpfReader.get_opt_singleton()
        hartree2kcalmol = 627.51
        what_choice = ["atom_info", "frag_name", "dimer_energy"]
        if what not in what_choice:
            raise ValueError(f"set what from {what_choice}.")
        mem_limit = CpfReader.format_mem_limit(mem_limit)
        if m or n:
            cpf_filter = CpfFilter.by_frag_id_repr(m, n)
        elif m_include or m_exclude or n_include or n_exclude:
            frag_name = CpfReader.pandas_read(path, what="frag_name")
            cpf_filter = CpfFilter.by_res_name(frag_name, m_include, m_exclude, n_include, n_exclude)
        else:
            cpf_filter = CpfFilter(None, None)

        logger.info("Entering header section.")
        opt = opt_singleton.create(nrows=1, widths=[100])
        title = pd.read_fwf(path, **opt)
        title = title.iloc[0, 0]
        assert ("CPF" in title)
        assert ("Open1.0" in title)
        assert ("rev23" in title)
        opt = opt_singleton.create(nrows=1, widths=[100])
        n_atom, n_frag = [int(i) for i in pd.read_fwf(path, **opt).iloc[0, 0].split()]
        n_dimer = int(n_frag * (n_frag - 1) / 2)
        n_wrap = -(-n_frag // 10)
        opt = opt_singleton.create(nrows=1, widths=[100])
        header_atom = pd.read_fwf(path, **opt).iloc[0, 0].replace("-", "_").lower().split()
        opt = opt_singleton.create(nrows=1, widths=[100])
        header_monomer = pd.read_fwf(path, **opt).iloc[0, 0].replace("-", "_").lower().split()
        opt = opt_singleton.create(nrows=1, widths=[100])
        header_monomer_energy = pd.read_fwf(path, **opt).iloc[0, 0].replace("-", "_").lower().split()
        opt = opt_singleton.create(nrows=1, widths=[100])
        header_dimer_energy = pd.read_fwf(path, **opt).iloc[0, 0].replace("-", "_").lower().split()

        if cpf_filter is None:
            cpf_filter = CpfFilter(None, None)
        cpf_filter.complete_by_all_frag_id(n_frag)

        logger.info("Entering atom info.")
        opt = opt_singleton.create(
            widths=[10, 2, 6, 4, 11, 11, 21, 20, 20, 4, 2] + [20] * len(header_atom),
            names=["id", "atom", "atom_type",
                   "res_name", "res_seq", "frag_id",
                   "x", "y", "z",
                   "chain_name", "chain_id"] + header_atom,
            nrows=n_atom,
            dtype_add=dict((key, "float") for key in header_atom),
        )
        logger.debug(opt)
        atom_info = pd.read_fwf(path, **opt)
        if what == "atom_info":
            return atom_info

        if what == "frag_name":
            frag_name = atom_info \
                .assign(rep_type=lambda d: d.atom_type.isin(["CA"])) \
                .assign(rep_type=lambda d: d.atom_type.isin(["C1'"])) \
                .assign(frag_name=lambda d: [str(i) + str(j) for i, j in zip(d.res_name, d.res_seq)]) \
                .assign(frag_name=lambda d: d.frag_name.astype("string"))
            frag_name = frag_name.sort_values(by=["rep_type"], ascending=False)
            frag_name = frag_name.drop_duplicates(["frag_id"])[["frag_id", "frag_name"]]
            frag_name = frag_name.sort_values(by=["frag_id"]).reset_index(drop=True)
            return frag_name

        logger.info("Entering n_atoms.")
        opt = opt_singleton.create(
            widths=[8] * 10,
            nrows=n_wrap,
        )
        logger.debug(opt)
        if what == "n_atoms":
            n_atoms = pd.read_fwf(path, **opt).to_numpy().ravel()
            n_atoms = n_atoms[~np.isnan(n_atoms)].astype(int)
            return n_atoms

        logger.info("Entering n_bonds.")
        opt = opt_singleton.create(
            widths=[8] * 10,
            nrows=n_wrap,
        )
        logger.debug(opt)
        n_bonds = pd.read_fwf(path, **opt).to_numpy().ravel()
        n_bonds = n_bonds[~np.isnan(n_bonds)].astype(int)
        if what == "n_bonds":
            return n_bonds

        logger.info("Entering bda/baa.")
        opt = opt_singleton.create(
            widths=[12, 12, 24],
            names=["bda", "baa", "bond_type"],
            nrows=int(np.sum(n_bonds)),
        )
        logger.debug(opt)
        if what == "bda_baa":
            bda_baa = pd.read_fwf(path, **opt)
            bda_baa = bda_baa.assign(bond_type=lambda d: d.bond_type.fillna(3).astype("int"))
            return bda_baa

        logger.info("Entering distance.")
        opt = opt_singleton.create(
            widths=[12, 12, 24],
            names=["i", "j", "dist"],
            nrows=n_dimer,
        )
        logger.debug(opt)
        if what == "dist":
            dist = pd.read_fwf(path, **opt)
            return dist

        logger.info("Entering monomer info.")
        opt = opt_singleton.create(
            # widths=[10] + [24] * len(header_monomer),
            widths=[10] + [24] + [25] * (len(header_monomer) - 1),  # cpf bug?
            names=["frag_id"] + header_monomer,
            nrows=n_frag,
            dtype_add=dict((key, "float") for key in header_monomer),
        )
        logger.debug(opt)
        if what == "monomer_info":
            monomer_info = pd.read_fwf(path, **opt)
            return monomer_info

        logger.info("Entering method info.")
        opt_singleton.proceed_position(7)

        logger.info("Entering monomer energy.")
        opt_singleton.proceed_position(1)
        opt = opt_singleton.create(
            widths=[10] + [24] * len(header_monomer_energy),
            names=["frag_id"] + header_monomer_energy,
            nrows=n_frag,
            dtype_add=dict((key, "float") for key in header_monomer_energy),
        )
        logger.debug(opt)
        if what == "monomer_energy":
            monomer_energy = pd.read_fwf(path, **opt)
            return monomer_energy

        logger.info("Entering dimer energy.")
        opt_singleton.proceed_position(1)
        opt = opt_singleton.create(
            widths=[10, 10] + [24] * len(header_dimer_energy),
            names=["i", "j"] + header_dimer_energy,
            nrows=n_dimer,
            dtype_add=dict((key, "float") for key in header_dimer_energy),
        )
        logger.debug(opt)
        estimated_df_row_mem = len(opt["widths"]) * 8  # df.values[0].nbytes
        if estimated_df_row_mem * len(cpf_filter.m) * len(cpf_filter.n) > mem_limit:
            raise MemoryError(f"Memory usage will exceed to mem_limit:{mem_limit}. Consider to set cpf_filter narrower.")
        chunksize = math.floor((mem_limit / estimated_df_row_mem) * chunk_ratio)
        logger.debug(f"read lines with chunksize: {chunksize}.")
        reader = pd.read_fwf(path, chunksize=chunksize, **opt)
        dimer_energy = pd.concat((cpf_filter.filter(d) for d in reader), ignore_index=True)
        energy_columns = dimer_energy.columns.difference(["i", "j", "m", "n"])
        dimer_energy[energy_columns] = dimer_energy[energy_columns] * hartree2kcalmol
        if what == "dimer_energy":
            frag_name = CpfReader.pandas_read(path, what="frag_name")
            dimer_energy = dimer_energy.merge(frag_name, how="left", left_on="m", right_on="frag_id", suffixes=("_m", "_m")) \
                .merge(frag_name, how="left", left_on="n", right_on="frag_id", suffixes=("_m", "_n"))
            columns = dimer_energy.columns.difference(["frag_id_m", "frag_id_n"], sort=False)
            dimer_energy = dimer_energy[columns]
            return dimer_energy
        raise EOFError("Unexpected Error.")

    @classmethod
    def set_arguments(cls, p: ArgumentParser) -> ArgumentParser:
        p.add_argument("files", nargs="+",
                       help="cpf or cpf compressed (pandas readable format) file(s) (e.g. .cpf, .cpf.gz, .cpf.zip)")
        p.add_argument("-m", help="frag_id e.g. '1,2,3', '1-200'")
        p.add_argument("-mi", "--m-include")
        p.add_argument("-mx", "--m-exclude")
        p.add_argument("-n",
                       help="frag_id e.g. '1,2,3', '1-200'")
        p.add_argument("-ni", "--n-include")
        p.add_argument("-nx", "--n-exclude")
        p.add_argument("-wh", "--what", choices=["atom_info", "frag_name", "dimer_energy"], default="frag_name")
        p.add_argument("-v", "--verbose", action="store_true")
        p.add_argument("--mem-limit", default="1000MB")
        p.add_argument("--chunk-ratio", type=float, default=0.005)
        return p