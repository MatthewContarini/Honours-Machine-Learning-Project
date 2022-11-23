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

    # comment
    # TODO this is not the best way to define the column names from the growth well
    def generate_data_frame(self, data_type, safe):
        column_names = [
            "Strain",
            "Date",
            "Media Concentration",
            "Drug",
            "Plate",
            "Plate Reader",
            "Replicate",
            "Row",
            "Column",
        ]
        column_names += self.generate_data_frame_column_times(data_type, safe)
        if data_type == "ABS_OD":
            list_of_od_reads = []
            for value in self.growth_wells.values():
                list_of_od_reads.append(value.generate_row(data_type))
            data_frame_to_return = pd.DataFrame(list_of_od_reads)
            data_frame_to_return.columns = column_names
        elif data_type == "RGR":
            list_of_rgr = [] 
            for value in self.growth_wells.values():
                list_of_rgr.append(value.generate_row(data_type))
            data_frame_to_return = pd.DataFrame(list_of_rgr)
            data_frame_to_return.columns = column_names 
        return data_frame_to_return

    def generate_data_frame_column_times(self, data_type, safe):
        wells_information = self.get_number_reads_start_time_read_interval(safe)
        number_of_reads = wells_information[0]
        start_time = wells_information[1]
        read_interval = wells_information[2]
        if data_type == "ABS_OD":
            column_times = range(
                start_time, (number_of_reads * read_interval), read_interval
            )
        elif data_type == "RGR":
            column_times = range(
                start_time,
                (number_of_reads * read_interval) - read_interval,
                read_interval,  # FIX hard CODING TODO :UHU
            )
        else:
            raise Exception("Incorrect Setting")
        return column_times

    def get_number_reads_start_time_read_interval(self, safe):
        if safe:
            self.check_if_readings_standardised()
        a_growth_well = next(iter(self.growth_wells.values()))
        return (
            a_growth_well.number_of_reads,
            a_growth_well.start_time,
            a_growth_well.get_read_interval(safe=False),
        )  # Already checked if safe is True

    def check_if_readings_standardised(self):
        counter = 0
        for value in self.growth_wells.values():
            if counter == 1:
                if current_readings != value.readings_od.keys():
                    raise Exception(
                        "The number of reads, read intervals, or the start times of"
                        + " the growth wells are different.  "
                        + "Data align them before calling this function."
                    )
            else:
                current_readings = value.readings_od.keys()
                counter += 1
        return True

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
