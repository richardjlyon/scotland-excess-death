"""
    chart_excess_deaths.py
    Richard Lyon, 25/9/21

    Generate a chart that shows 2021 and (2015-2010) excess deaths.
"""

import matplotlib.pyplot as plt

from scotland_deaths import OUT_DIR
from scotland_deaths.covid_deaths import CovidDeaths


def chart_excess_deaths():

    covid_deaths = CovidDeaths(week_no=37)

    df = covid_deaths.deaths_by_cause_and_location(daily=True)

    df_2021 = df["2021"].sum(axis=1)
    df_2015_2019 = df["(2015-2019)"].sum(axis=1)

    plt.rcParams["axes.facecolor"] = (0.95, 0.95, 0.95)

    fig, [ax1, ax2] = plt.subplots(2, 1)
    fig.set_size_inches(16, 8)
    fig.suptitle("Excess deaths, Scotland 2021 vs. (2015-2019)")

    # Upper plot : total vs. avg deaths

    df_2021.plot(
        ax=ax1,
        color="tab:blue",
        linewidth=3,
        label="Total deaths",
    )
    df_2015_2019.plot(
        ax=ax1,
        color="grey",
        label="Average (2015-2019)",
    )

    ax1.fill_between(
        df_2021.index,
        df_2021,
        df_2015_2019,
        where=(df_2021 >= df_2015_2019),
        color="tab:red",
        alpha=0.1,
    )
    ax1.fill_between(
        df_2021.index,
        df_2021,
        df_2015_2019,
        where=(df_2021 < df_2015_2019),
        color="tab:green",
        alpha=0.1,
    )
    ax1.legend(loc=(0.8, 0.8))
    ax1.set_ylabel("Daily deaths")
    ax1.set_ylim([0, 250])

    # lower plot : excess death

    excess_death_df = df_2021 - df_2015_2019

    excess_death_df.plot(ax=ax2, linewidth=3)
    ax2.fill_between(
        excess_death_df.index,
        excess_death_df,
        0,
        where=(excess_death_df >= 0),
        color="tab:red",
        alpha=0.1,
    )
    ax2.fill_between(
        excess_death_df.index,
        excess_death_df,
        0,
        where=(excess_death_df < 0),
        color="tab:green",
        alpha=0.1,
    )
    ax2.set_ylabel("Excess deaths")

    ax1.annotate(
        "richardlyon.substack.com",
        (0, 0),
        (25, 25),
        xycoords="figure points",
        textcoords="offset pixels",
        va="top",
        color="grey",
    )
    ax1.annotate(
        "SOURCE: National Records of Scotland",
        (0, 0),
        (1300, 25),
        xycoords="figure points",
        textcoords="offset pixels",
        va="top",
        color="grey",
    )

    for ax in [ax1, ax2]:
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_visible(False)
        ax.spines["bottom"].set_visible(False)

    plt.savefig(OUT_DIR / "Excess Deaths Scotland 2021.png")
    plt.show()


if __name__ == "__main__":
    chart_excess_deaths()
