import pandas as pd
from argparse import ArgumentParser
from ...mixin import ReaderMixin


class HpiReader(ReaderMixin):
    @classmethod
    def pandas_read(cls, path, **kwargs) -> pd.DataFrame:
        with open(path, "r") as f:
            skiprows = 0
            nrows = 0
            for line in f:
                skiprows += 1
                if "**Inter&Intramolecular H/pi interactions**" in line:
                    next(f)
                    next(f)
                    next(f)
                    skiprows += 3
                    break
            for line in f:
                if line.startswith("          "):
                    break
                nrows += 1
        widths = [4, 5, 3, 4, 4, 3, 5, 5, 3, 6, 4, 6, 6, 6, 7, 6, 3]
        header = ["id","pi_IDRD", "pi_RES", "pi_KL", "pi_VPI", "pi_VATM", "pi_N",
                  "hx_IDRD", "hx_RES", "hx_VATM", "hx_N",
                  "geom_DPLN", "geom_DLIN", "geom_DATM", "geom_OMEGA", "geom_Hangl", "geom_RG"]
        header = [i.lower() for i in header]
        df = pd.read_fwf(path, names=header, widths=widths, skiprows=skiprows, nrows=nrows)
        df = df.assign(
            is_hpi_dpln=df.geom_dpln.str.startswith("["),
            is_hpi_dlin=df.geom_dlin.str.startswith("["),
            is_hpi_datm=df.geom_datm.str.startswith("[")
        ).assign(
            geom_dpln=df.geom_dpln.str.strip("[]").replace("****", "NaN").astype(float),
            geom_dlin=df.geom_dlin.str.strip("[]").replace("****", "NaN").astype(float),
            geom_datm=df.geom_datm.str.strip("[]").replace("****", "NaN").astype(float)
        )
        return df

    @classmethod
    def set_arguments(cls, p: ArgumentParser) -> ArgumentParser:
        p.add_argument("files", nargs="+")
        return p


