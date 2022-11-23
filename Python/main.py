from growth_wells import GrowthWells
from PCA import *

# Import Settings
ians_summer_data_mutants = ["RIF2_B5", "RIF2_F4", "RIF3_1B10", "RIF4_1E6"]
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
    "MG1655",
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
    "MG1655",
]
data_specifciation = {
    "ians_summer_data": (
        "Python/data/csv_data/Ians_Summer_01_18_to_01_28_Data.csv",
        ians_summer_data_mutants,
    ),
    "alicias_new_data": (
        "Python/data/csv_data/Alicias_New_Data.csv",
        alicias_mutants_new,
    ),
    "alicias_honours_data": (
        "Python/data/csv_data/Alicias_Honours_Data.csv",
        alicias_honours_mutants,
    ),
}
pickle_file_path = "Python/data/pickled_data/growth_well_dictionary.pickle"

data = GrowthWells()
data.load_growth_data(
    data_file_specification=pickle_file_path,
    from_pickle=True,
    verbose=False,
    save_as_pickle=False,
)

data.set_start_time(0)
data.align_times(15)
data.truncate(1380)

# print(data.get_growth_well(("mainMutants", 1, "B", 5)).get_relative_growth_rates())

growth_wells_data_frame = data.generate_data_frame(data_type="RGR", safe=True)
# growth_wells_data_frame = growth_wells_data_frame.loc[
#     growth_wells_data_frame["Media Concentration"] == 0.1
# ]

run_and_show_pca(
    growth_wells_data_frame,
    x=1,
    y=2,
    target="Strain",
    features=list(range(0, 1380, 15)),
)
