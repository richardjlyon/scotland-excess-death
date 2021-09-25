"""
    excess_deaths.py
    Richard Lyon, 24/09/21
"""

import matplotlib.pyplot as plt

from scotland_deaths import OUT_DIR
from scotland_deaths.covid_deaths import CovidDeaths


def plot_total_vs_actual_deaths(ax, covid_deaths: CovidDeaths):

    df_deaths = covid_deaths.get_all_deaths(resample=True)

    ax.plot(
        df_deaths.index,
        df_deaths["Total deaths (2021)"],
        color="tab:blue",
        # marker="o",
        linewidth=3,
        label="Total deaths",
    )
    ax.plot(
        df_deaths.index,
        df_deaths["Average total deaths (2015-2019)"],
        color="grey",
        # marker="o",
        label="Average previous 5 years",
    )
    ax.fill_between(
        df_deaths.index,
        df_deaths["Total deaths (2021)"],
        df_deaths["Average total deaths (2015-2019)"],
        where=(
            df_deaths["Total deaths (2021)"]
            >= df_deaths["Average total deaths (2015-2019)"]
        ),
        color="tab:red",
        alpha=0.1,
    )
    ax.fill_between(
        df_deaths.index,
        df_deaths["Total deaths (2021)"],
        df_deaths["Average total deaths (2015-2019)"],
        where=(
            df_deaths["Total deaths (2021)"]
            < df_deaths["Average total deaths (2015-2019)"]
        ),
        color="tab:green",
        alpha=0.1,
    )
    ax.title.set_text("Fig. 1 Excess deaths, Scotland 2021")
    ax.legend(loc=(0.78, 0.8))

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.spines["bottom"].set_visible(False)


def plot_covid_vs_noncovid_deaths(ax, covid_deaths: CovidDeaths):

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
    ax.title.set_text("Fig 2. Covid vs non-Covid excess deaths, Scotland 2021")
    ax.legend(loc=(0.52, 0.8))
    ax.axhspan(0, -400, facecolor="g", alpha=0.1)
    ax.axhspan(0, 400, facecolor="r", alpha=0.1)

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.spines["bottom"].set_visible(False)


def plot_two_panel_excess_deaths():
    covid_deaths = CovidDeaths(week_no=37)

    fig, [ax1, ax2] = plt.subplots(2, 1)
    fig.set_size_inches(16, 10)
    fig.patch.set_facecolor("white")
    fig.suptitle("Why are Governments not talking about non-Covid excess deaths?")

    plot_total_vs_actual_deaths(ax1, covid_deaths)
    plot_covid_vs_noncovid_deaths(ax2, covid_deaths)

    plt.savefig(OUT_DIR / "Excess Deaths Scotland 2021.png")
    plt.show()


def plot_respiratory_illness_by_location():
    covid_deaths = CovidDeaths(week_no=37)
    df = covid_deaths.get_excess_deaths()
    df = df["2021"] - df["(2015-2019)"]

    fig, [(ax1, ax2), (ax3, ax4), (ax5, ax6)] = plt.subplots(3, 2)
    fig.suptitle(
        "Excess death by cause and location, Scotland 2021 (SOURCE: National Records of Scotland)"
    )
    fig.set_size_inches(16, 12)
    fig.patch.set_facecolor("white")

    ax1.annotate(
        "richardlyon.substack.com",
        (0, 0),
        (50, 50),
        xycoords="figure points",
        textcoords="offset pixels",
        va="top",
        color="grey",
    )

    causes = [
        (ax1, "COVID-19"),
        (ax2, "Cancer"),
        (ax3, "Respiratory"),
        (ax4, "Circulatory (heart disease and stroke)"),
        (ax5, "Other"),
        (ax6, "Dementia / Alzheimers"),
    ]
    for ax, cause in causes:
        ax.title.set_text(cause)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_visible(False)
        ax.spines["bottom"].set_visible(False)

        for location in df[cause].columns:
            ax.bar(df.index, df[cause][location], width=5, label=location)
            if ax == ax1:
                ax.legend(loc=("upper right"))

    plt.savefig(OUT_DIR / "Excess death by cause and location, Scotland 2021.png")
    plt.show()


if __name__ == "__main__":
    # plot_two_panel_excess_deaths()
    plot_respiratory_illness_by_location()
