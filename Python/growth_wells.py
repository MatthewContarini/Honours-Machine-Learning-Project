from data_to_dictionary import load_growth_well_dictionary
import pandas as pd
import warnings


class GrowthWells:
    def __init__(self):
        self._growth_wells = {}

    def __str__(self):
        return f"GrowthWell wrapper.\nContaining: {self.growth_wells}"

    # TODO This impliments data_to_dictionary, functionality should eventually be
    # moved here
    def load_growth_data(
        self, data_file_specification, from_pickle, verbose, save_as_pickle
    ):
        self.growth_wells = load_growth_well_dictionary(
            data_file_specification=data_file_specification,
            from_pickle=from_pickle,
            verbose=verbose,
            save_as_pickle=save_as_pickle,
        )

    @property
    def growth_wells(self):
        return self._growth_wells

    @growth_wells.setter
    def growth_wells(self, growth_well_dictionary):
        self._growth_wells = growth_well_dictionary

    @property
    def number_of_growth_wells(self):
        return len(self.growth_wells)

    def get_growth_well(self, key):
        return self.growth_wells[key]

    def _get_number_of_od_reads(self):
        counter = 0
        for value in self.growth_wells.values():
            if counter != 0:
                if read_number != value.number_of_reads:
                    warnings.warn(
                        "The number of reads were not the same in each "
                        + "growth well.\nCall truncate() to truncate first."
                    )
                    return None
            else:
                counter += 1
                read_number = value.number_of_reads
        return read_number

    # Iterate over each growth well and set the starting time to 0 and adjust
    # accordingly.
    def set_start_time(self, start_time=0):
        # TODO: Add docstring
        """Set the starting time"""

        for key, growth_well in self.growth_wells.items():
            growth_well.set_start_time(start_time)

    # TODO:Add auto_align and doc string
    def align_times(self, multiple):
        """
        This function takes a dictionary containing {key : GrowthWells}.  From this
        the function removes time values from each of the GrowthWells in order to
        keep a multiple of all of the growth times.  From [0, 3, 6,
        9, 12, 15, 18, 21, 24, 27, 30] and [0 , 5, 10, 15, 20, 25, 30] to BOTH [0,
        15, 30]

        Args:
            var:

        Returns:
            var:
        """
        if multiple != None:
            for key in self.growth_wells.keys():

                self.growth_wells.get(key).keep_time_multiples_of(multiple)

    # TODO: Add docstring
    def truncate(self, cut_position):
        for value in self.growth_wells.values():
            value.delete_after(cut_position)

    def align_and_truncate(self, start_time, multiple, cut_position):
        """
        This function takes runs set_start_time(), align_times(), and
        truncate() in order.

        Args:
            start_time: see the documentation of set_start_time()
            multiple: see the documentation of align_times()
            cut_position: see the documentation of truncate()
        """

        self.set_start_time(start_time)
        self.align_times(multiple)
        self.truncate(cut_position)

    def generate_data_frame(self):
        number_of_od_reads = self._get_number_of_od_reads()
        column_names = ["Strain", "Date", "Media Concentration"]
        column_names += list(range(number_of_od_reads))
        list_of_od_reads = []
        for value in self.growth_wells.values():
            list_of_od_reads.append(value.generate_row())
        data_frame_to_return = pd.DataFrame(list_of_od_reads)

        data_frame_to_return.columns = column_names
        return data_frame_to_return

    @property
    def strains(self):
        list_of_strains = []
        for value in self.growth_wells.values():
            if value.strain not in list_of_strains:
                list_of_strains.append(value.strain)
        return list_of_strains

    @property
    def dates(self):
        list_of_dates = []
        for value in self.growth_wells.values():
            if value.date not in list_of_dates:
                list_of_dates.append(value.date)
        return list_of_dates

    @property
    def media_concentrations(self):
        media_concentrations = []
        for value in self.growth_wells.values():
            if value.media_concentration not in media_concentrations:
                media_concentrations.append(value.media_concentration)
        return media_concentrations
