import pandas as pd
import pickle
import warnings
from growth_well import GrowthWell
from tqdm.auto import tqdm

# TODO: Add functionalty
def __run_r_script():
    pass


# TODO: add functionality
def __quality_control(data):
    # TODO: Add if statment
    # if "TimeMinutes" contains NA
    #    raise Warning
    passed_quality_control = True
    if passed_quality_control:
        return "Passed Quality Control"
    else:
        raise Exception(f'"{data.name}" Failed Quality Control')


def __screen_data(data, mutants_to_analyse):
    name = data.name
    # TODO: This is inefficient and not inplace.
    # Change Strain to strain / impliment some lowercase version.
    screened_data = data[data.Strain.isin(mutants_to_analyse)]
    screened_data.name = name
    # Screen out NA values in the time columns.
    print("(This is a Hard Coded Print), Values May contain NaN data.")
    screened_data = screened_data.dropna(subset=["TimeMinutes"])
    return screened_data


def __dataframe_into_list_of_growth_wells(grow96_data, verbose):
    # Check if MediaConcentration or Drug columns exist in the data frame.
    media_concentration_exits = False
    drug_exists = False
    if "MediaConcentration" in grow96_data.columns:
        media_concentration_exits = True
    if "Drug" in grow96_data.columns:
        drug_exists = True
    # Ensure indexes pair with number of rows
    grow96_data = grow96_data.reset_index()
    dictionary_of_growth_wells = {}
    # Iterate over the entire data frame and make a new GrowthWell instance
    # for each new growth well.  If a unique growth well already exists
    # append {time : OD} to the already existing GrowthWell.
    for index, row in tqdm(
        grow96_data.iterrows(),
        total=len(grow96_data),
        colour="Green",
        disable=not verbose,
    ):  # tqmd returns the progress
        composite_key = (row["Plate"], row["Replicate"], row["Row"], row["Column"])
        # Check if this key is already in dictionary_of_growth_wells.
        if (composite_key) in dictionary_of_growth_wells:
            # If it is in the dictionary_of_growth_wells add the time and OD
            dictionary_of_growth_wells[composite_key].add_OD_and_time(
                round(row["TimeMinutes"]), row["OD"]
            )
        else:
            # If the GrowthWell is not in the overarching dictionary, add the
            # key and the value to the dictionary and populate the readings_od.
            # field.
            dictionary_of_growth_wells.update(
                {
                    composite_key: GrowthWell(
                        plate=row["Plate"],
                        plate_reader=row["PlateReader"],
                        date=row["Date"],
                        replicate=row["Replicate"],
                        row96=row["Row"],
                        column96=row["Column"],
                        well_type=row["WellType"],
                        drugs=(row["Drug"] if (drug_exists) else None),
                        media_concentration=(
                            row["MediaConcentration"]
                            if (media_concentration_exits)
                            else None
                        ),
                        strain=row["Strain"],
                        readings_od={round(row["TimeMinutes"]): row["OD"]},
                    )
                }
            )
    return dictionary_of_growth_wells


def generate_growth_well_dictionary(name, file_path, mutants_to_analyse, verbose=False):
    """
    This function takes a data.csv of growth well data and returns a
    dictionary of GrowthWells which can be accesed via a key.

    Args:
        name: The name of the data
        file_path: The path to the file containing the growth well data
        mutants_to_analyse: The list of mutant IDs to screen for.

    Returns:
        dictionary_of_growthwells: A dictionary of GrowthWells which can be
        accessed through a composite key: (plate, replicate, row, column).
        These GrowthWells can then be accessed and manipulated.
    """

    raw_data = pd.read_csv(file_path)
    # Name the dataframe.name after reading it in.
    raw_data.name = name
    # Screen the data for Rif strains etc.
    screened_data = __screen_data(raw_data, mutants_to_analyse)
    # Quality control the data
    __quality_control(screened_data)
    # Generate the dictionary of growth wells
    dictionary_of_growth_wells = __dataframe_into_list_of_growth_wells(
        screened_data, verbose
    )
    return dictionary_of_growth_wells


def load_growth_well_dictionary(
    from_pickle,
    data_file_specification,
    verbose=False,
    save_as_pickle=True,
    run_r_script=False,
):
    """
    This function takes four arguments to determine where the final dictionary
    of growth well data should be taken from and whether it should be saved.
    The funciton calls generate_growth_well_dictionary() on each of the files
    in the data_file_specification if from_pickle == False and merges them and saves
    them as a pickle (if save_as_pickle == True).  If from_pickle == True then
    the data_file_specification represents a file_path to the .pickle file and
    loads the growth_dictionary from it.  The returned values from each
    from_pickle state will be a dictionary containing {(composite_key) :
    GrowthWells}

    Args:
        from_pickle: Is a flag indicating whether to load from a .pickle file
            or from grow96 data files.
        data_file_specification: Is either a type = {str(name) : (str(file_path),
            list(str(mutants))} or a type = str depending on the from_pickle
            state.
        verbose: Will print out the steps within the loading process for greater
            insight.
        save_as_pickle: Determines whether the loaded in data should be saved
            as a .pickle after it has been loaded.
        run_r_script: Determines whether to run the r script from raw OD
            readings first.

    Returns:
        comprehenisve_dictionary: A dictionary containing {tuple(composite_key)
            : GrowthWells} from all the grow96 output.

    Warnings:
        warning: When trying to save pickle after loading in from pickle.  And
            when not saving as a pickle after loading in from grow96.

    Raises:
        TypeError: Depending on what the state of from_pickle is, an error will
        be raised if a file_path / dictionary is being passed when it should be
        the opposite of what was passed.
    """

    if run_r_script:
        __run_r_script()

    # Branch if the data should be loaded in from a .pickle file.
    if from_pickle:
        # Check if data_file_specification is a string.
        if type(data_file_specification) != str:
            raise TypeError(
                "data_file_specification must be a string if from_pickle == True"
            )
        if verbose:
            print("Loading pickle.")
        # Load the pickle file from the given data_file_specification file_path.
        pickle_in = open(data_file_specification, "rb")
        comprehenisve_dictionary = pickle.load(pickle_in)
        pickle_in.close()
        # Warn if trying to save as a pickle using the same file just retrived.
        if save_as_pickle:
            warnings.warn(
                "\nThe flag: save_as_pickle == True, but data loaded from pickle.  "
                + "Did not save the data as a pickle file.\nTo avoid this warning, "
                + "set save_as_pickle to False."
            )
        return comprehenisve_dictionary
    # Branch if the data should be loaded in from grow96 data.
    else:
        # check if data_file_information is a {str : []}
        if type(data_file_specification) != dict:
            raise TypeError(
                "data_file_information must be a dict if from_pickle == False"
            )
        if verbose:
            print("Loading each .csv file.")
        # Variables describing the indexes of the file path and the list of mutants.
        file_path_index = 0
        mutants_index = 1
        # Initialise the dicitonary.
        comprehenisve_dictionary = {}
        # Iterate over each of the grow96 files and create a dictionary.  From
        # this, join them together to create a dictionary containing all data.
        for name, file_information in data_file_specification.items():
            if verbose:
                print(f"Loading file: {data_file_specification.get(name)[0]}")
            current_dictionary = generate_growth_well_dictionary(
                name,
                file_information[file_path_index],
                file_information[mutants_index],
                verbose,
            )
            # Inplace merge.
            comprehenisve_dictionary |= current_dictionary
        if save_as_pickle == True:
            if verbose:
                print("Saving as .pickle")
            _save_growth_well_dictionary(comprehenisve_dictionary)
        else:
            # Warn if the data just retrieved from the grow96 data is not being
            # saved as a pickle file.
            if verbose:
                print("The data is NOT SAVING as a .pickle")
            warnings.warn("\nThe data was not saved as a .pickle file.")
        return comprehenisve_dictionary


def _save_growth_well_dictionary(growth_well_dictionary):
    try:
        # Save the dictionary from load_growth_well_dictionary as a .pickle file.
        pickle_out = open(
            "Python/data/pickled_data/growth_well_dictionary.pickle", "wb"
        )
        pickle.dump(growth_well_dictionary, pickle_out)
        pickle_out.close()
    except:
        raise Exception("Could not save: growth_well_dictionary.")
