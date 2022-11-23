import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D


def run_pca(standard_data):
    number_of_columns = len(standard_data[0])  # Length of first entry.
    pca = PCA(n_components=number_of_columns)
    print(pca.explained_variance_ratio_)
    return pca.fit_transform(standard_data)


def pca_to_data_frame(principal_components):
    column_names = []
    number_of_columns = len(principal_components[0])  # Length of first entry.
    for i in range(number_of_columns):
        column_names.append(f"Principal Component {i+1}")
    principalDf = pd.DataFrame(data=principal_components, columns=column_names)
    return principalDf


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


def run_and_show_pca(data_frame, x, y, target=None, features=None, colour_target=None):
    # TODO: add funcitonality, comment better
    if target == None:
        pass
    elif features == None:
        pass
    elif (target == None) and (features == None):
        raise Exception("At least target or features must be specified.")

    if type(target) != list:
        # If it is a string.
        target = [target]
        colour_target = target[0]
    # Already a list.
    elif len(target) > 1 and colour_target == None:
        raise Exception(
            "If parsing in two or more targets, a colour target must be specified."
        )
    elif len(target) == 1 and colour_target == None:
        colour_target = target[0]

    # TODO: Check if the target is in the column names of the data frame and throw an exception
    target_data = data_frame.loc[:, target].values
    target_data_frame = pd.DataFrame(target_data, columns=target)
    feature_data = data_frame.loc[:, features].values
    standard_data = StandardScaler().fit_transform(feature_data)
    pca = run_pca(standard_data)
    pca_data_frame = pca_to_data_frame(pca)

    final_df = pd.concat([pca_data_frame, target_data_frame], axis=1)

    fig, ax = plt.subplots(figsize=(6, 6))

    unique_colours = make_colour_map(data_frame[colour_target].unique())

    ax.scatter(
        final_df[f"Principal Component {x}"].tolist(),
        final_df[f"Principal Component {y}"].tolist(),
        c=final_df[colour_target].map(unique_colours),
        #       xlabel=f"Principal Component {x}",
        #       ylabel=f"Principal Component {y}",
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
