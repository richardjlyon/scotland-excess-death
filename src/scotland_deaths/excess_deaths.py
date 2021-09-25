"""
    excess_deaths.py
    Richard Lyon, 24/09/21
"""

import matplotlib.pyplot as plt
import pandas as pd

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


def plot_covid_vs_noncovid_deaths(ax, df_deaths):
    # compute "all locations"
    df_n = df_deaths.groupby(level=[0, 1], axis=1).sum()

    causes = list(df_n["2021"].columns)
    non_covid_causes = [c for c in causes if c != "COVID-19"]

    df_data = pd.DataFrame(columns=["Covid", "non-Covid"])
    df_data["Covid"] = df_n["2021"]["COVID-19"] - df_n["(2015-2019)"]["COVID-19"]
    df_data["non-Covid"] = df_n["2021"][non_covid_causes].sum(axis=1) - df_n[
        "(2015-2019)"
    ][non_covid_causes].sum(axis=1)

    ax.plot(
        df_data.index,
        df_data["non-Covid"],
        color="tab:blue",
        # marker="o",
        linewidth=3,
        label="Cancer, Heart Disease, Stroke, Dementia, Altheimers, Respiratory, Other",
    )
    ax.plot(df_data.index, df_data["Covid"], color="grey", label="Covid")
    ax.fill_between(
        df_data.index,
        df_data["Covid"],
        df_data["non-Covid"],
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


# def plot_geriatric_vs_nongeriatric_deaths(ax, df_deaths):
#     # compute "all locations"
#     df_n = df_deaths.groupby(level=[0, 1], axis=1).sum()
#     causes = list(df_n["2021"].columns)
#     non_geriatric_causes = ["Cancer", "Other"]
#     geriatric_causes = [c for c in causes if c not in non_geriatric_causes]
#     print(geriatric_causes)
#
#     df_data = pd.DataFrame(columns=["Geriatric", "non Geriatric"])
#     df_data["Geriatric"] = df_n["2021"][geriatric_causes].sum(axis=1) - df_n[
#         "(2015-2019)"
#     ][geriatric_causes].sum(axis=1)
#     df_data["non Geriatric"] = df_n["2021"][non_geriatric_causes].sum(axis=1) - df_n[
#         "(2015-2019)"
#     ][non_geriatric_causes].sum(axis=1)
#
#     ax.plot(df_data.index, df_data["Geriatric"], color="tab:red", label="Geriatric")
#     ax.plot(
#         df_data.index,
#         df_data["non Geriatric"],
#         color="tab:green",
#         # marker="o",
#         label="non Geriatric",
#     )
#     ax.fill_between(
#         df_data.index,
#         df_data["Geriatric"],
#         df_data["non Geriatric"],
#         color="grey",
#         alpha=0.2,
#     )
#     ax.title.set_text("Geriatric vs non-Geriatric excess deaths, Scotland 2021")
#     ax.legend(loc="upper right")
# plt.axhline(y=0, color="grey")


if __name__ == "__main__":
    covid_deaths = CovidDeaths(week_no=37)

    fig, [ax1, ax2] = plt.subplots(2, 1)
    fig.set_size_inches(16, 10)
    fig.patch.set_facecolor("white")
    fig.suptitle("Why are Governments not talking about non-Covid excess deaths?")

    plot_total_vs_actual_deaths(ax1, covid_deaths)
    plot_covid_vs_noncovid_deaths(ax2, covid_deaths.get_excess_deaths())
    # plot_geriatric_vs_nongeriatric_deaths(ax3, c.excess_death_df)

    # non_geriatric_causes = ["Cancer", "Other"]
    # geriatric_causes = [c for c in causes if c not in non_geriatric_causes]

    # df_data.plot()
    # print(df_n["2021"].to_markdown())
    plt.savefig(OUT_DIR / "Excess Deaths Scotland 2021.png")
    plt.show()
