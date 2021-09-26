"""
    chart_covid_vs_non_covid_excess_deaths.py
    Richard Lyon, 25/9/21

    Generate a chart that shows Covid vs. non Covid excess death.
"""

import matplotlib.pyplot as plt

from scotland_deaths import OUT_DIR
from scotland_deaths.covid_deaths import CovidDeaths

if __name__ == "__main__":

    plt.rcParams["axes.facecolor"] = (0.95, 0.95, 0.95)

    covid_deaths = CovidDeaths(week_no=37)

    df = covid_deaths.covid_non_covid_excess_deaths(daily=True)

    # plt.rcParams["axes.facecolor"] = (0.95, 0.95, 0.95)

    # fig, ax = new_single_panel_chart(
    #     "Covid vs. non Covid death, Scotland 2021 vs. (2015-2019)"
    # )

    fig, ax = plt.subplots(1, 1)
    fig.set_size_inches(16, 6)
    fig.suptitle("Covid vs. non Covid death, Scotland 2021 vs. (2015-2019)")

    df["non-Covid"].plot(
        ax=ax,
        color="tab:red",
        linewidth=3,
        label="Cancer, Heart Disease, Stroke, Dementia, Altheimers, Respiratory, Other",
    )
    df["Covid"].plot(ax=ax, color="tab:blue", linewidth=3, label="Covid")
    ax.fill_between(
        df.index,
        df["Covid"],
        0,
        color="tab:blue",
        alpha=0.1,
    )
    ax.fill_between(
        df.index,
        df["non-Covid"],
        0,
        color="tab:red",
        alpha=0.1,
    )

    ax.annotate(
        "richardlyon.substack.com",
        (0, 0),
        (25, 25),
        xycoords="figure points",
        textcoords="offset pixels",
        va="top",
        color="grey",
    )
    ax.annotate(
        "SOURCE: National Records of Scotland",
        (0, 0),
        (1300, 25),
        xycoords="figure points",
        textcoords="offset pixels",
        va="top",
        color="grey",
    )

    ax.legend()
    ax.set_ylabel("Excess deaths")
    # plt.grid(axis="y")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.spines["bottom"].set_visible(False)

    plt.savefig(OUT_DIR / "Excess Covid vs non Covid deaths 2021.png")
    plt.show()
