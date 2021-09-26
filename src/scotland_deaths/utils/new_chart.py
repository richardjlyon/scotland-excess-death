"""
    new_chart.py
    Richard Lyon, 25/9/21
"""
import matplotlib.pyplot as plt

def new_chart(title:str):
    plt.rcParams['axes.facecolor'] = (0.95, 0.95, 0.95)
    fig, ax = plt.subplots(1,1)
    fig.set_size_inches(16, 8)
    fig.suptitle(title)

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.spines["bottom"].set_visible(False)

    return fig, ax