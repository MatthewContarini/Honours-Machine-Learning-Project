class Unsupervised_Algorithm:
    def __init__(self, dataframe, target_names, feature_names):
        self.data_dataframe = dataframe
        self.features = dataframe.loc[:, feature_names]  # Get the features.
        self.targets = dataframe.loc[:, target_names]  # Get the targets.
        