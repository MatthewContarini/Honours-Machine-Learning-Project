class GrowthWell:
    """
    This class represents a unique growth well over time.

    Attributes:
        plate: A string that represents the name of the plate that the well is on.
        plate_reader: The plate reader for this well.
        date: The date the plate was read.
        replicate: The number of the replicate of the well.
        row96: The row on the 96 well plate (represented by a Char).
        column96: The column on the 96 well plate (represented by a Int).
        well_type: What te well is was used for (DATA, BLANK, EMPTY).
        strain: The strain present within this well.
        readings_od: A dictionary containing the readings from the optical
            density reader.  The dictionary is in the form {time : OD}.
        drugs: (optional) The drugs present within the growth media.
        media_concentration: (optional) The consentration of glucose within the
            growth media.
    """

    # TODO: Add functionality to the following four class attributes.  This may
    #     require changing the {time : OD} to {time : [TEMPERATURE,
    #     RAW_OPTICAL_DENSITY, BLANKED_OPTICAL_DENSITY,
    #     CALCULATED_OPTICAL_DENSITY]}.
    TEMPERATURE = 0
    RAW_OPTICAL_DENSITY = 1
    BLANKED_OPTICAL_DENSITY = 2
    CALCULATED_OPTICAL_DENSITY = 3

    def __init__(
        self,
        plate,
        plate_reader,
        date,
        replicate,
        row96,
        column96,
        well_type,
        strain,
        readings_od={},
        drugs=None,
        media_concentration=None,
    ):
        """Initialize a GrowthWell."""

        self.plate = plate
        self.plate_reader = plate_reader
        self.date = date
        self.replicate = replicate
        self.row96 = row96
        self.column96 = column96
        self.well_type = well_type
        self.drugs = drugs
        self.media_concentration = media_concentration
        self.strain = strain
        # readings_od is a dictionary with the minutes as the key, and the
        # OD readings as the values.
        self.readings_od = readings_od
        self.read_interval = self.__caluculate_start_and_read_interval()

    def __str__(self):
        return (
            f"Plate: {self.plate}, Replicate: {self.replicate}, Row: {self.row96}, Column: {self.column96}"
            + f' -- ("{self.plate}", {self.replicate}, "{self.row96}", {self.column96}) \n'
            + f"\tStrain: {self.strain}, Drug(s): {self.drugs}, Well Type: {self.well_type} \n"
        )

    def __repr__(self):
        return f"{self.plate}, {self.replicate}, {self.row96}, {self.column96}\n"

    @property
    def number_of_reads(self):
        return len(self.readings_od)

    def get_ods(self, time_in_minutes=None):
        """
        This function takes a time in minutes and returns the od at that time.
        If no time is provided then the entire od list is returned.

        Args:
            time_in_minutes: The time in minutes to return the od.

        Returns:
            Either a single od or a list of them if time is not given.
        """

        if time_in_minutes is not None:
            try:
                readings_to_return = self.readings_od.get(time_in_minutes)
            except:
                raise Exception("Invalid Time")
            else:
                return self.readings_od.get(time_in_minutes)
        else:
            return list(self.readings_od.values())

    def add_OD_and_time(self, time, optical_density):
        """Append a {time : OD} to the readings_od"""
        self.readings_od.update({time: optical_density})

    # TODO: Make more efficient / Comment better.
    def __caluculate_start_and_read_interval(self):
        read_interval = None
        for_counter = 0
        for current_key, current_value in self.readings_od.items():
            if for_counter == 0:
                data_start_time = current_key  # First time point.
            elif for_counter == 1:
                read_interval = current_key - data_start_time  # Difference.
                break
        # set the read_interval
        self.read_interval = read_interval

    def delete_after(self, time):
        keys_to_keep = []
        if self.readings_od.get(time) != None:
            for key, value in self.readings_od.items():
                if key <= time:
                    keys_to_keep.append(key)
                    # Set the new keys
            self.readings_od = {
                new_key: self.readings_od[new_key] for new_key in keys_to_keep
            }

    def set_start_time(self, start_time=0):
        # TODO: Make doc string and comment well
        """Make Doc String"""
        # Get the original start time and the time difference between
        # the measurments of the optical density.
        for_counter = 0
        for current_key, current_value in self.readings_od.items():
            if for_counter == 0:
                data_start_time = current_key  # First time point.
            elif for_counter == 1:
                read_frequency = current_key - data_start_time  # Difference.
                break
            for_counter += 1
        # If the old start time and the new start time are different.
        if start_time != data_start_time:
            new_keys = []
            for i in range(len(self.readings_od)):
                new_key = i * read_frequency + start_time
                new_keys.append(new_key)
            self.readings_od = dict(zip(new_keys, list(self.readings_od.values())))

    # TODO: Better name, add docstring, more efficenc
    def keep_time_multiples_of(self, multiple):
        keys_to_keep = []
        # Iterate over all of the items in the dictionary
        for key, value in self.readings_od.items():
            if key % multiple == 0:
                keys_to_keep.append(key)
        # Set the new keys
        self.readings_od = {
            new_key: self.readings_od[new_key] for new_key in keys_to_keep
        }
        # Change the read interval
        self.read_interval = multiple

    def generate_row(self):
        return (
            [self.strain]
            + [self.date]
            + [self.media_concentration]
            + list(self.get_ods())
        )
