from growth_wells import GrowthWells
import pandas as pd
import matplotlib.pyplot as plt
from PCA import *

# Import Settings
ians_summer_data_mutants = []  # "RIF2_B5", "RIF2_F4", "RIF3_1B10", "RIF4_1E6"
alicias_mutants_new = [
    "R12",
    "R14",
    "R17",
    "R18",
    "R19",
    "R2",
    "R26",
    "R3",
    "R30",
    "R36",
    "R8",
    "R9",
]
alicias_honours_mutants = [
    "R17",
    "R18",
    "R21",
    "R22",
    "R26",
    "R29",
    "R30",
    "R34",
    "R36",
    "R9",
]
data_specifciation = {
    "ians_summer_data": (
        "data/csv_data/Ians_Summer_01_18_to_01_28_Data.csv",
        ians_summer_data_mutants,
    ),
    "alicias_new_data": ("data/csv_data/Alicias_New_Data.csv", alicias_mutants_new),
    "alicias_honours_data": (
        "data/csv_data/Alicias_Honours_Data.csv",
        alicias_honours_mutants,
    ),
}
pickle_file_path = "data/pickled_data/growth_well_dictionary.pickle"

data = GrowthWells()
data.load_growth_data(
    data_file_specification=pickle_file_path,
    from_pickle=True,
    verbose=False,
    save_as_pickle=False,
)
data.align_and_truncate(start_time=0, multiple=15, cut_position=1380)
growth_wells_data_frame = data.generate_data_frame()

range_of_features = list(range(0, int(93)))


standard_data = standardise_data(
    growth_wells_data_frame, "Media Concentration", range_of_features
)
pca = run_pca(standard_data)
pca_data_frame = pca_to_data_frame(pca)


final_df = pd.concat(
    [pca_data_frame, growth_wells_data_frame[["Media Concentration"]]], axis=1
)

plt.scatter(
    final_df["principal component 1"].tolist(),
    final_df["principal component 2"].tolist(),
    c=list(
        final_df["Media Concentration"].map(make_colour_map(data.media_concentrations))
    ),
    alpha=0.8,
)

plt.show()
