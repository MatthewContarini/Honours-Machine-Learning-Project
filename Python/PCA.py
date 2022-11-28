import pandas as pd
from sklearn.decomposition import PCA


class PCA_for_growth_well_data:
    def __init__(self, dataframe, target_names, feature_names):
        self.data_dataframe = dataframe
        self.features = dataframe.loc[:, feature_names]  # Get the features.
        self.targets = dataframe.loc[:, target_names]  # Get the targets.
        # Run a PCA transformation and store results in a tuple.
        pca_and_pca_dataframe = self.run_pca()
        self.pca = pca_and_pca_dataframe[0]
        self.pca_dataframe = pd.concat([pca_and_pca_dataframe[1], self.targets], axis=1)

    def run_pca(self):
        number_of_features = len(self.features.columns)  # Length of first entry.
        # Set up pca object
        pca = PCA(n_components=number_of_features)
        pca_array = pca.fit_transform(self.features)
        pca_dataframe = self.pca_to_dataframe(pca_array)
        return (pca, pca_dataframe)

    def get_explained_variance(self):
        return self.pca.explained_variance_ratio_

    def pca_to_dataframe(self, pca_array):
        column_names = []
        number_of_columns = len(pca_array[0])  # Length of first entry.
        for i in range(number_of_columns):
            column_names.append(f"Principal Component {i+1}")
        principalDf = pd.DataFrame(data=pca_array, columns=column_names)
        return principalDf
