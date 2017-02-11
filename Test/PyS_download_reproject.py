# PySatellite test
#
# Download SP3, reproject and extract by satellite
#
# Kristof Ostir, 2017-02-10
# University of Ljubljana, Faculty of Civil and Geodetic Engineering
# (c) 2017

# Imports
import PySatellite as pys

# Parameters
data_folder = "D:/Kristof/Python/PySatellite/Data/"
data_file = "D:/Kristof/Python/PySatellite/Data/igu19355_06.sp3"
kml_file = "D:/Kristof/Python/PySatellite/Data/igu19355_06.kml"

# Read current SP3 for current time
# sp3_fn = pys.download_sp3(data_folder="D:/Kristof/Python/PySatellite/Data/")

# Read data to dataframe
sp3_df = pys.read_sp3(data_file)

# Reproject
sp3_df_lla = pys.convert_ecef2lla(sp3_df, True)

# Display data
print(sp3_df.head())
print(sp3_df_lla.head())

# Positions to file
# sat_pos = sp3_df_lla[["coor_x", "coor_y", "coor_z",	"lat", "long", "alt"]]
# for name, group in sat_pos.groupby(level=[0]):
#     group.to_csv("%s_sp3_positions.csv" % name)

pys.write_kml(sp3_df_lla, kml_file)
