from growth_wells import GrowthWells
from data_to_dictionary import *

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
    # "ians_summer_data": (
    #     "data/csv_data/Ians_Summer_01_18_to_01_28_Data.csv",
    #     ians_summer_data_mutants,
    # ),
    "alicias_new_data": (
        "G:/My Drive/Uni/Honours/Honours-Machine-Learning-Project/Python/data/csv_data/Alicias_New_Data.csv",
        alicias_mutants_new,
    ),
    # "alicias_honours_data": (
    #     "data/csv_data/Alicias_Honours_Data.csv",
    #     alicias_honours_mutants,
    # ),
}
pickle_file_path = "data/pickled_data/growth_well_dictionary.pickle"

data = GrowthWells()
data.load_growth_data(
    data_file_specification=data_specifciation,
    from_pickle=False,
    verbose=True,
    save_as_pickle=False,
)

data.set_start_time(0)
data.align_times(3)
data.truncate(1380)

# print(data.get_growth_well(("mainMutants", 1, "B", 5)).get_relative_growth_rates())

growth_wells_dataframe = data.generate_dataframe(data_type="ABS_OD", safe=True)

concnetrations = [0.0005, 0.001, 0.002, 0.003, 0.004, 0.005, 0.006, 0.008, 0.01]
names = ['0-0005', '0-001', '0-002', '0-003', '0-004', '0-005', '0-006', '0-008', '0-01']
j = 0
for i in concnetrations:
    growth_wells_dataframe_p = growth_wells_dataframe.loc[growth_wells_dataframe['Media Concentration'] == i]
    print(growth_wells_dataframe_p.head())

    growth_wells_dataframe_p.to_csv(f"G:/My Drive/Uni/Honours/Honours-Machine-Learning-Project/data_for_colab/proccessed_growth_data/3Min_{names[j]}MC_OD", encoding="utf-8", index=False)
    j += 1

# wrapper = PCA_for_growth_well_data(
#     growth_wells_dataframe, ["Media Concentration", "Strain"], list(range(0, 1380, 15))
# )


# show_pca_3d(wrapper, "Strain")

# show_pca_statistics(wrapper)
