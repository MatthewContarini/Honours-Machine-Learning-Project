import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np
import plotly.express as px


def get_spaced_colours(n):
    hard_coded_colours = [
        "#8b4513",
        "#006400",
        "#778899",
        "#000080",
        "#ff0000",
        "#ffa500",
        "#ffff00",
        "#00ff00",
        "#00ffff",
        "#0000ff",
        "#ff00ff",
        "#1e90ff",
        "#98fb98",
        "#ffdead",
        "#ff69b4",
        "#9acd32",
        "#d8bfd8",
        "#db7093",
        "#ee82ee",
        "#696969",
        "#000000",
        "#808000",
        "#7f0000",
        "#333333",
        "#666666",
    ]
    if n <= 25:
        return hard_coded_colours[:n]
    else:
        max_value = 16581375  # 255**3
        interval = int(max_value / n)
        colors = [hex(I)[2:].zfill(6) for I in range(0, max_value, interval)]
        return [
            (int(i[:2], 16) / 255, int(i[2:4], 16) / 255, int(i[4:], 16) / 255)
            for i in colors
        ]


def make_colour_map(keys):
    colours = get_spaced_colours(len(keys))
    return dict(zip(keys, colours))


def show_pca(pca_wrapper, colour=None, x=1, y=2):
    dataframe = pca_wrapper.pca_dataframe
    unique_colours = make_colour_map(dataframe[colour].unique())
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.scatter(
        dataframe[f"Principal Component {x}"].tolist(),
        dataframe[f"Principal Component {y}"].tolist(),
        c=dataframe[colour].map(unique_colours),
    )

    # add a legend
    handles = [
        Line2D(
            [0],
            [0],
            marker="o",
            color="w",
            markerfacecolor=value,
            label=key,
            markersize=8,
        )
        for key, value in unique_colours.items()
    ]
    ax.legend(handles=handles)

    plt.show()


def show_pca_3d(pca_wrapper, colour=None, x=1, y=2, z=3):
    dataframe = pca_wrapper.pca_dataframe
    fig = px.scatter_3d(
        dataframe,
        x=f"Principal Component {x}",
        y=f"Principal Component {y}",
        z=f"Principal Component {z}",
        color=colour,
    )
    fig.show()


def show_pca_statistics(pca_wrapper):
    x = range(len(pca_wrapper.pca.explained_variance_ratio_))
    y = pca_wrapper.pca.explained_variance_ratio_
    plt.title("Variance Captured from each Principal Component")
    plt.xlabel("Principal Component")
    plt.ylabel("Cumulative Explained Variance")
    plt.plot(x, np.cumsum(y))
    plt.grid()
    plt.show()
