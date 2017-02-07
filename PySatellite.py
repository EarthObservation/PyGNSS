# PySatellite
# Analysis of GNSS data

# Imports
import pandas as pd
import datetime


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
