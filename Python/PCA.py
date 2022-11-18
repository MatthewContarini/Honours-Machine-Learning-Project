import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA


def standardise_data(data_frame, target_name, feature_names):
    feature_data_frame = data_frame.loc[:, feature_names].values
    target_data_frame = data_frame.loc[:, [target_name]].values
    # Standardise the features.
    return StandardScaler().fit_transform(feature_data_frame)


def run_pca(standard_data):
    pca = PCA(n_components=3)
    return pca.fit_transform(standard_data)


def pca_to_data_frame(principal_components):
    principalDf = pd.DataFrame(
        data=principal_components,
        columns=[
            "principal component 1",
            "principal component 2",
            "principal component 3",
        ],
    )
    return principalDf


def get_spaced_colours(n):
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
