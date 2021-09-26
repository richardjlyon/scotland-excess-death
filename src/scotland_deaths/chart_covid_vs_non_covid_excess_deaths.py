"""
    chart_covid_vs_non_covid_excess_deaths.py
    Richard Lyon, 25/9/21

    Generate a chart that shows Covid vs. non Covid excess death.
"""

import matplotlib.pyplot as plt

from scotland_deaths import OUT_DIR
from scotland_deaths.covid_deaths import CovidDeaths
from scotland_deaths.utils import new_chart

if __name__ == "__main__":

    covid_deaths = CovidDeaths(week_no=37)

    fig, ax = new_chart("Covid vs. non Covid death, Scotland 2021 vs. (2015-2019)")

    df = covid_deaths.get_covid_non_covid_excess_deaths()

    ax.plot(
        df.index,
        df["non-Covid"],
        color="tab:blue",
        # marker="o",
        linewidth=3,
        label="Cancer, Heart Disease, Stroke, Dementia, Altheimers, Respiratory, Other",
    )
    ax.plot(df.index, df["Covid"], color="grey", label="Covid")
    ax.fill_between(
        df.index,
        df["Covid"],
        df["non-Covid"],
        color="tab:blue",
        alpha=0.1,
    )

    ax.legend(loc=(0.52, 0.8))
    ax.axhspan(0, -400, facecolor="g", alpha=0.1)
    ax.axhspan(0, 400, facecolor="r", alpha=0.1)

    plt.savefig(OUT_DIR / "Excess Covid vs non Covid deaths 2021.png")
    plt.show()