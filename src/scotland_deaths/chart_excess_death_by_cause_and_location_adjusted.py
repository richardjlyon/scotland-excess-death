"""
    chart_excess_death_by_cause_and_location_adjusted.py
    Richard Lyon, 26/9/21

    Generate a chart that estimates Covid excess death after accounting for respiratory and dementia
    negative excess death.
"""

import matplotlib.pyplot as plt

from scotland_deaths import OUT_DIR
from scotland_deaths.covid_deaths import CovidDeaths
from scotland_deaths.utils import new_six_panel_chart


def chart_excess_death_by_cause_and_location_adjusted():

    fig, [(ax1, ax2), (ax3, ax4), (ax5, ax6)] = new_six_panel_chart(
        "Hypothetical excess death by cause and location assuming Covid accounts for Respiratory/Care Home negative excess, Scotland 2021 vs (2015-2019)"
    )

    covid_deaths = CovidDeaths(week_no=37)

    df = covid_deaths.deaths_by_cause_and_location(daily=True)
    df_excess = df["2021"] - df["(2015-2019)"]

    total_before = df_excess["2021"].sum(axis=1).sum()

    # starting Covid numbers
    # print(df_excess["COVID-19"].loc["2021-05-01"])

    # care home numbers
    # print(df_excess.swaplevel(axis=1)["Care Homes"].loc["2021-05-01"])

    causes = [
        (ax1, "COVID-19"),
        (ax2, "Cancer"),
        (ax3, "Respiratory"),
        (ax4, "Circulatory (heart disease and stroke)"),
        (ax5, "Dementia / Alzheimers"),
        (ax6, "Other"),
    ]

    # adjust Covid to deduct negative excess deaths for respiratory infection, dementia, add Alzheimers
    for cause in ["Respiratory", "Dementia / Alzheimers"]:
        df_neg, df_pos = df_excess[cause].clip(upper=0), df_excess[cause].clip(lower=0)
        df_excess["COVID-19"] = df_excess["COVID-19"] + df_neg
        df_excess[cause] = df_pos

    # adjust Covid to deduct negative excess care home death
    for cause in [
        "Cancer",
        "Respiratory",
        "Circulatory (heart disease and stroke)",
        "Dementia / Alzheimers",
        "Other",
    ]:

        df_neg, df_pos = df_excess[cause]["Care Homes"].clip(upper=0), df_excess[cause][
            "Care Homes"
        ].clip(lower=0)
        df_excess["COVID-19"]["Care Homes"] = (
            df_excess["COVID-19"]["Care Homes"] + df_neg
        )
        df_excess[cause]["Care Homes"] = df_pos

    # sanity check
    # print(df_excess["COVID-19"].loc["2021-05-01"])

    total_after = df_excess["2021"].sum(axis=1).sum()
    assert total_before == total_after

    # print(f"Total Covid deaths: {df_excess['COVID-19'].sum().sum()}")

    for ax, cause in causes:

        cause_df = df_excess[cause]
        total_df = cause_df.sum(axis=1)

        # split dataframe df into negative only and positive only values
        df_neg, df_pos = cause_df.clip(upper=0), cause_df.clip(lower=0)
        # stacked area plot of positive values
        df_pos.plot.area(ax=ax, stacked=True, linewidth=0.0, legend=False, alpha=0.8)
        # reset the color cycle
        ax.set_prop_cycle(None)
        # stacked area plot of negative values, prepend column names with '_' such that they don't appear in the legend
        df_neg.rename(columns=lambda x: "_" + x).plot.area(
            ax=ax, stacked=True, linewidth=0.0, legend=False, alpha=0.8
        )
        # rescale the y axis
        # ax.set_ylim([df_neg.sum(axis=1).min(), df_pos.sum(axis=1).max()])
        ax.set_ylim([-30, 60])

        total_df.plot(ax=ax, color="black", linewidth=2, label="Total")

        ax.title.set_text(cause)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_visible(False)
        ax.spines["bottom"].set_visible(False)
        if ax == ax1:
            ax.legend(loc=("upper right"))

    plt.savefig(
        OUT_DIR / "Hypothetical Excess death by cause and location, Scotland 2021.png"
    )
    # plt.show()


if __name__ == "__main__":
    chart_excess_death_by_cause_and_location_adjusted()
