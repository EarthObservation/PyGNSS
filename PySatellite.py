# PySatellite
# Analysis of GNSS data

# Imports
import pandas as pd
import datetime
import numpy as np
from io import StringIO

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

# Download SP3 file
def sp3_download(dt, data_folder):
    """
    sp3_download: Download SP3 file closest to specified date

    Args:
        dt: GPS date and time, if missing current time is used
        data_folder: Location of downloaded file

    Returns:
        res: True on success
    """

    return res

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
    df_cols = ["dt_y", "dt_m", "dt_d", "dt_hour", "dt_min", "dt_secfra",
               "vehicle", "coor_x", "coor_y", "coor_z", "clock",
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
            cur_time = ",".join(ln.split()[1:])
            continue
        if ln.startswith('EOF'):
            continue
        if cur_time is None:
            print('NO time found')
            sys.exit(1)
        spf_s.write(cur_time + "," + ",".join(ln.split()[:9]) + "\n")
    spf_s.seek(0)

    # Create initial dataframe
    sp3_df = pd.read_csv(spf_s, header=None,
                         names=df_cols)
    sp3_df["dt_sec"] = sp3_df["dt_secfra"].astype(int)
    sp3_df["dt_mic"] = ((sp3_df["dt_secfra"] - sp3_df["dt_sec"]) * 1e6).astype(int)
    sp3_df['date_time'] = \
        sp3_df[['dt_y', 'dt_m', 'dt_d',
                "dt_hour", "dt_min", "dt_sec",
                "dt_mic"]].apply\
            (lambda s: datetime.datetime(*s), axis=1)
    sp3_df.drop(['dt_y', 'dt_m', 'dt_d',
                "dt_hour", "dt_min", "dt_sec",
                "dt_mic", "dt_secfra"], axis=1, inplace=True)
    # sp3_df.set_index('date_time')
    return sp3_df
