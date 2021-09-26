"""
    new_single_panel_chart.py
    Richard Lyon, 25/9/21
"""
import matplotlib.pyplot as plt

def new_single_panel_chart(title:str):
    plt.rcParams['axes.facecolor'] = (0.95, 0.95, 0.95)
    fig, ax = plt.subplots(1,1)
    fig.set_size_inches(16, 8)
    fig.suptitle(title)

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.spines["bottom"].set_visible(False)

    ax.annotate(
        "richardlyon.substack.com",
        (0, 0),
        (50, 50),
        xycoords="figure points",
        textcoords="offset pixels",
        va="top",
        color="grey",
    )
    ax.annotate(
        "SOURCE: National Records of Scotland",
        (0, 0),
        (1250, 50),
        xycoords="figure points",
        textcoords="offset pixels",
        va="top",
        color="grey",
    )

    return fig, ax