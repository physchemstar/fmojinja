import pandas as pd


def pandas_read_hpi(path):
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


pd.read_hpi = pandas_read_hpi

if __name__ == '__main__':
    from argparse import ArgumentParser
    from io import StringIO
    p = ArgumentParser()
    p.add_argument("hpi", nargs="*")

    a = p.parse_args()
    if len(a.hpi) == 0:
        p.print_help()
        exit()

    is_first = True
    for path in a.hpi:
        output = StringIO()
        df = pandas_read_hpi(path)
        if len(a.hpi) > 1:
            df = df.assign(path=path)
        df.to_csv(output, index=False, header=is_first)
        output.seek(0)
        print(output.read())
        is_first = False

