"""
    chart_excess_death_by_cause_and_location.py
    Richard Lyon, 24/09/21

    Generate a 6-panel chart that shows excess death by cause and location.
"""

import matplotlib.pyplot as plt

from scotland_deaths import OUT_DIR
from scotland_deaths.covid_deaths import CovidDeaths
from scotland_deaths.utils import new_six_panel_chart


def chart_excess_death_by_cause_and_location():

    fig, [(ax1, ax2), (ax3, ax4), (ax5, ax6)] = new_six_panel_chart(
        "Excess death by cause and location, Scotland 2021 vs (2015-2019)"
    )

    covid_deaths = CovidDeaths(week_no=37)
    df = covid_deaths.deaths_by_cause_and_location(daily=True)
    df = df["2021"] - df["(2015-2019)"]

    print(f"Total Covid deaths: {df['COVID-19'].sum().sum()}")

    causes = [
        (ax1, "COVID-19"),
        (ax2, "Cancer"),
        (ax3, "Respiratory"),
        (ax4, "Circulatory (heart disease and stroke)"),
        (ax5, "Dementia / Alzheimers"),
        (ax6, "Other"),
    ]
    for ax, cause in causes:

        cause_df = df[cause]
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

    plt.savefig(OUT_DIR / "Excess death by cause and location, Scotland 2021.png")
    plt.show()


if __name__ == "__main__":
    chart_excess_death_by_cause_and_location()
