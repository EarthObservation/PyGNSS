# Analysis an visualisation of GNSS precise orbits
#
# Functions for downloading , time conversion, reprojection and visualisation of precise GNSS orbits
#
# Krištof Oštir and Polona Pavličič Prešeren
# University of Ljubljana, Faculty of Civil and Geodetic Engineering
# (c) 2017


# Imports
import pandas as pd
import datetime
import numpy as np
from io import StringIO
import pyproj
from ftplib import FTP
import subprocess
import os

# Parameters
# Difference beetween UTM in and GPS time
utm_gps_diff = pd.DataFrame([("1980-01-01", 0),
                     ("1981-07-01", 1),
                     ("1982-07-01", 2),
                     ("1983-07-01", 3),
                     ("1985-07-01", 4),
                     ("1988-01-01", 5),
                     ("1990-01-01", 6),
                     ("1991-01-01", 7),
                     ("1992-07-01", 8),
                     ("1993-07-01", 9),
                     ("1994-07-01", 10),
                     ("1996-01-01", 11),
                     ("1997-07-01", 12),
                     ("1999-01-01", 13),
                     ("2006-01-01", 14),
                     ("2009-01-01", 15),
                     ("2012-07-01", 16),
                     ("2015-07-01", 17),
                     ("2017-01-01", 18)],
                            columns=["From", "GPS_UTC"])
utm_gps_diff["From"]  = pd.to_datetime(utm_gps_diff['From'])
utm_gps_diff = utm_gps_diff.set_index("From")
# Projections
ecef = pyproj.Proj(proj='geocent', ellps='WGS84', datum='WGS84')
lla = pyproj.Proj(proj='latlong', ellps='WGS84', datum='WGS84')
# FTP server
ftp_address = "igs.ensg.ign.fr"
ftp_data_root = "/pub/igs/products/"
fn_data_root = "D:/Kristof/Python/PySatellite/Data/"
# Unzip tool, complete path or command, 7-ZIP handles .Z on Windows
gunzip = "7z"
# GPS epoch, time measurements
secWeek = 604800 # seconds in week
secDay = 86400 # seconds in day
gpsStart = datetime.datetime(1980, 1, 6, 0, 0, 0) # GPS start of time


# Convert UTC time to GPS time
def time_utc2gps(dt):
    """
    time_utc2gps converts datetime from UTC to GPS
    
    Args:
        dt - utm date and time
    
    Returns:
        time_gps: time in GPS seconds
    """

    time_diff = int(utm_gps_diff[:dt]["GPS_UTC"][-1])
    time_gps = dt + datetime.timedelta(seconds=time_diff)
    return time_gps


# Convert UTC time to GPS time
def time_gps2utc(dt):
    """
    time_utc2gps converts datetime from GPS to UTC

    Args:
        dt - GPS date and time

    Returns:
        time_gps: time in GPS seconds
    """

    time_diff = int(utm_gps_diff[:dt]["GPS_UTC"][-1])
    time_utm = dt + datetime.timedelta(seconds=-time_diff)
    return time_utm


# Compute GPS week, day and time
def time_gps2wdt(dt=None):
    """
    time2gps_wdt: Convert time to gpsWeek, gpsSecWeek, gpsDay, gpsSecsDay

    Args:
        dt: date and time, current time if missing

    Returns:
        gpsWeek: GPS week
        gpsSecWeek: GPS second in week
        gpsDay: GPS day
        gpsSecsDay: GPS second in day
    """

    if dt == None:
        dt = datetime.datetime.now()
    # Convert to GPS time
    dt_gps = time_utc2gps(dt)

    # Time difference to GPS start
    gpsDiff = dt_gps - gpsStart

    gpsWeek = int(np.floor(gpsDiff.total_seconds()/secWeek))
    gpsSecWeek =  gpsDiff.total_seconds() % secWeek
    gpsDay = int(np.floor(gpsSecWeek/secDay))
    gpsSecsDay = gpsSecWeek % secDay

    return gpsWeek, gpsSecWeek, gpsDay, gpsSecsDay


# Download SP3 file
def download_sp3(**kwargs):
    """
    download_sp3: Download SP3 file closest to specified date

    Args:
        dt: date and time, if missing current time is used
        data_folder: Location of downloaded file, if missing current path is used

    Returns:
        res: downloaded filename, empty on error
    """

    # Read and set parameters
    dt = kwargs.get('dt', datetime.datetime.now())
    data_folder = kwargs.get('data_folder', "")
    if not os.path.exists(data_folder):
        print('Data folder %s does not exist, using current folder.' % data_folder)
        data_folder = ""

    # get GPS time parameters
    gpsW, _, gpsD, gpsS = time_gps2wdt(dt)
    gpsH = int(gpsS) // 3600 // 6 * 6
    # GPS precise orbit filename
    gps_orbit_fn = "igu%d%d_%02d.sp3.Z" % (gpsW, gpsD, gpsH)
    # If file not yet available check also previous
    gpsW2, gpsW2, gpsD2, gpsH2 = gpsW, gpsW, gpsD, gpsH
    gpsH2 -= 6
    if gpsH2 < 0:
        gpsH2 = gpsH2 + 24
        gpsD2 -= 1
    if gpsD2 < 0:
        gpsD2 = gpsD2 + 7
        gpsW2 -= 1
    gps_orbit_fn_previous = "igu%d%d_%02d.sp3.Z" % (gpsW2, gpsD2, gpsH2)

    # File to get
    ftp_file = "%s%d/%s" % (ftp_data_root, gpsW, gps_orbit_fn)
    get_file = "%s%s" % (data_folder, gps_orbit_fn)
    # Getting file from FTP
    # Open FTP connection
    try:
        ftp = FTP(ftp_address)
        ftp.login()
    except:
        print("Can not login to %s" % ftp_address)
        raise
    # Check if file exists, otherwise load previous
    try:
        # Open the file for writing in binary mode
        ftp.size(ftp_file)
    except:
        try:
            gps_orbit_fn = gps_orbit_fn_previous
            ftp_file = "%s%d/%s" % (ftp_data_root, gpsW, gps_orbit_fn)
            get_file = "%s%s" % (data_folder, gps_orbit_fn)
            ftp.size(ftp_file)
        except:
            print("No file %s on server" % gps_orbit_fn)
            get_file = ""
    print('Getting precise orbit for ' + gps_orbit_fn)
    file = open(get_file, 'wb')
    ftp.retrbinary('RETR %s' % ftp_file, file.write)
    # Clean up files
    file.close()
    ftp.close()

    # Decompress file
    get_file_dec = get_file[:-2]
    res = subprocess.call([gunzip, 'e', get_file, "-o" + os.path.dirname(get_file), "-aoa"])
    if res != 0:
        print("Can not decopress %" % get_file)
        print(result.returncode, result.stdout, result.stderr)
    # Delete downloaded file
    os.remove(get_file)

    return get_file_dec


# Read SP3 file
def read_sp3(sp3_fn):
    """
    read_sp3: Reads SP3 file to dataframe

    Args:
        sp3_fn: file name

    Returns:
        res: dataframe
    """

    # Dataframe column names
    df_cols = ["date_time", "vehicle",
               "coor_x", "coor_y", "coor_z", "clock",
               "std_x", "std_y", "std_z", "std_c"]
    # Open file and prepare IO string
    try:
        spf_in = open(sp3_fn)
    except:
        return False
    spf_s = StringIO()
    spf_in_lines = spf_in.readlines()[22:]

    # Read SP3 and extract orbit part
    # Line with GPS time is followed by satellite data
    cur_time = None
    for ln in spf_in_lines:
        if not ln.strip():
            continue
        if ln.startswith('*  '):
            ln_split = ln.split()[1:]
            ct_y = int(ln_split[0])
            ct_m = int(ln_split[1])
            ct_d = int(ln_split[2])
            ct_hour = int(ln_split[3])
            ct_min = int(ln_split[4])
            ct_secmic = float(ln_split[5])
            ct_sec = int(ct_secmic)
            ct_mic = int((ct_secmic-ct_sec)*1e6)
            ct = datetime.datetime(ct_y, ct_m, ct_d,
                                   ct_hour, ct_min, ct_sec, ct_mic)
            cur_time = time_gps2utc(ct)
            continue
        if ln.startswith('EOF'):
            continue
        if cur_time is None:
            print('NO time found')
            raise
        spf_s.write(str(cur_time) + "," + ",".join(ln.split()[:9]) + "\n")
    spf_s.seek(0)

    # Create initial dataframe
    sp3_df = pd.read_csv(spf_s, header=None,
                         names=df_cols)
    sp3_df["date_time"] = pd.to_datetime(sp3_df["date_time"])
    sp3_df["vehicle"] = sp3_df["vehicle"].map(lambda x: str(x)[1:])
    sp3_df.set_index(["vehicle", 'date_time'], inplace=True)
    return sp3_df


# Reproject from ECEF x, y, z to latitude, longitude, altitude
def reproject_ecef2lla(args):
    """
    reproject_ecf2lla: Reproject from ECEF x, y, z to latitude, longitude, altitude as a array

    Args:
        args are coordinates
        x: ECEF x coordinate in km
        y: ECEF y coordinate in km
        z: ECEF z coordinate in km

    Returns:
        lat: latitude
        long: longitude
        alt: altitude in km
    """

    # Extract arguments
    x = args[0] * 1000
    y = args[1] * 1000
    z = args[2] * 1000

    lon, lat, alt = pyproj.transform(ecef, lla, x, y, z)

    return pd.Series([lat, lon, alt/1000], index=['lat', 'long', 'alt'])


# Convert coordinates from ECEF to lat, long, alt
def convert_ecef2lla(df, remove=False):
    """
    convert_ecef2lla: Convert coordinates in dataframe from ECEF to lat, long, alt

    Args:
        df: dataframe with coor_x, coor_y, coor_z
        remove: remove cartesian coordinates, default False

    Returns:
        df_out: dataframe with lat, lon, alt
    """

    df_lla = df[["coor_x", "coor_y", "coor_z"]].apply(reproject_ecef2lla, axis=1)
    df_out = df.join(df_lla)
    if remove:
        df_out.drop(["coor_x", "coor_y", "coor_z"], axis=1, inplace=True)
    return df_out
