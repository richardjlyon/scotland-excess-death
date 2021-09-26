"""
    new_six_panel_chart.py
    Richard Lyon, 25/9/21
"""
import matplotlib.pyplot as plt


def new_six_panel_chart(title: str):

    plt.rcParams["axes.facecolor"] = (0.95, 0.95, 0.95)
    fig, [(ax1, ax2), (ax3, ax4), (ax5, ax6)] = plt.subplots(3, 2)
    fig.suptitle(title)
    fig.set_size_inches(16, 12)

    ax1.annotate(
        "richardlyon.substack.com",
        (0, 0),
        (50, 50),
        xycoords="figure points",
        textcoords="offset pixels",
        va="top",
        color="grey",
    )
    ax1.annotate(
        "SOURCE: National Records of Scotland",
        (0, 0),
        (1250, 50),
        xycoords="figure points",
        textcoords="offset pixels",
        va="top",
        color="grey",
    )

    return fig, [(ax1, ax2), (ax3, ax4), (ax5, ax6)]
