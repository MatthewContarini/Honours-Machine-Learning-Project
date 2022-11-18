library(grow96)
library(tidyverse)

#### Read ####
# Import Ians_Summer_01_18_to_01_28_Data
Ians_Summer_01_18_to_01_28_Data <- 
          processODData(specPath = "data/spec/Ians_Spec_Summer_01_18_to_01_28/", 
                        dataPath = "data/raw/Ians_Raw_Summer_01_18_to_01_28/",
                        filePrefix = "")
# Import Alicias Honours Data
Alicias_Honours_Data <- 
          processODData(specPath = "data/spec/Alicias_Honours_Spec/", 
                        dataPath = "data/raw/Alicias_Honours_Raw/")
# Import Alicias New Data
Alicias_New_Data <- 
  processODData(specPath = "data/spec/Alicias_New_Spec/", 
                dataPath = "data/raw/Alicias_New_Raw/",
                filePrefix = "raw_",
                blankGroups = "mediaconc",
                tukeyK = TRUE)

#### Process Data ####
alicia_columns <- c("Plate", "Replicate",	"Date",	
                    "PlateReader",	"SetTemperature",	"Row", 
                    "Column",	"Well",	"WellType", "Strain",	
                    "MediaConcentration", "TimeMinutes",
                    "TimeHours", "Temperature",	"OD",	
                    "BlankedOD")
ians_summer_columns  <- c("Plate", "Replicate",	"Date",	
                          "PlateReader",	"SetTemperature",	
                          "Row", "Column",	"Well",	
                          "WellType",	"Drug", "Strain",	
                          "TimeMinutes",	"TimeHours", 
                          "Temperature",	"OD",	"BlankedOD")
colnames(Alicias_Honours_Data) <- alicia_columns
colnames(Alicias_New_Data) <- alicia_columns
colnames(Ians_Summer_01_18_to_01_28_Data) <- ians_summer_columns

#### Write ####
# Save Ians_Summer_01_18_to_01_28_Data as .csv in
write_csv(Ians_Summer_01_18_to_01_28_Data, file =
          "../Python/data/csv_data/Ians_Summer_01_18_to_01_28_Data.csv")
# Save Alicias_Honours_Data as .csv in
write_csv(Alicias_Honours_Data, file =
          "../Python/data/csv_data/Alicias_Honours_Data.csv")
# Save Alicias_New_Data as .csv in
write_csv(Alicias_New_Data, file =
            "../Python/data/csv_data/Alicias_New_Data.csv")