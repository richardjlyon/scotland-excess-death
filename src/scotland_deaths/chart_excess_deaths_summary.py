"""
    chart_excess_deaths_summary.py
    Richard Lyon, 25/9/21

    Generate a chart that shows 2021 and (2015-2010) excess deaths.
"""

import matplotlib.pyplot as plt

from scotland_deaths import OUT_DIR
from scotland_deaths.covid_deaths import CovidDeaths
from scotland_deaths.utils import new_chart

if __name__ == "__main__":

    covid_deaths = CovidDeaths(week_no=37)

    fig, ax = new_chart("Excess deaths, Scotland 2021 vs. (2015-2019)")

    df = covid_deaths.get_all_deaths(resample=True)

    ax.plot(
        df.index,
        df["Total deaths (2021)"],
        color="tab:blue",
        # marker="o",
        linewidth=3,
        label="Total deaths",
    )
    ax.plot(
        df.index,
        df["Average total deaths (2015-2019)"],
        color="grey",
        # marker="o",
        label="Average (2015-2019)",
    )
    ax.fill_between(
        df.index,
        df["Total deaths (2021)"],
        df["Average total deaths (2015-2019)"],
        where=(
                df["Total deaths (2021)"]
                >= df["Average total deaths (2015-2019)"]
        ),
        color="tab:red",
        alpha=0.1,
    )
    ax.fill_between(
        df.index,
        df["Total deaths (2021)"],
        df["Average total deaths (2015-2019)"],
        where=(
                df["Total deaths (2021)"]
                < df["Average total deaths (2015-2019)"]
        ),
        color="tab:green",
        alpha=0.1,
    )

    ax.legend(loc=(0.8, 0.85))

    plt.savefig(OUT_DIR / "Excess Deaths Scotland 2021.png")
    plt.show()


