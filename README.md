# PySatellite - Analysis an visualisation of GNSS precise orbits

Functions for downloading, time conversion, reprojection and visualisation of precise GNSS orbits.

First we have to load the package with
```python
import PySatellite as pys
```

We are using the standard libraries, like pandas, datetime, numpy, io, ftplib, subprocess, and os. In addition pyproj is required for reprojection.

Than we download current satellite precise orbit data from FTP.


We have to convert from ECEF to longitude, latitude and height.

Parameters
data_folder = "D:/Kristof/Python/PySatellite/Data/"
data_file = "D:/Kristof/Python/PySatellite/Data/igu19355_06.sp3"
kml_file = "D:/Kristof/Python/PySatellite/Data/igu19355_06.kml"

Read current SP3 for current time
sp3_fn = pys.download_sp3(data_folder="D:/Kristof/Python/PySatellite/Data/")

Read data to dataframe
sp3_df = pys.read_sp3(data_file)

Reproject
sp3_df_lla = pys.convert_ecef2lla(sp3_df, False, True)

Display data
print(sp3_df.head())
print(sp3_df_lla.head())

Write data to KML.
pys.write_kml(sp3_df_lla, kml_file)

KML can be opened in Google Earth. Orbits are displayed as lines for each of the GPS satellites. In addition for every satellite we have positions iu time. Google Earth time feature enables navigation.

Krištof Oštir and Polona Pavlovčič Prešeren  
University of Ljubljana, Faculty of Civil and Geodetic Engineering  
(c) 2017

