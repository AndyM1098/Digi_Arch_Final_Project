import pandas as pd
from dataclasses import dataclass
from datetime import datetime, timezone

# Field index constants
MMSI_FIELD = 0
DATETIME_FIELD = 1
LAT_FIELD = 2
LON_FIELD = 3
SOG_FIELD = 4
COG_FIELD = 5
HEADING_FIELD = 6
VESSEL_NAME_FIELD = 7
IMO_FIELD = 8
CALL_SIGN_FIELD = 9
VESSEL_TYPE_FIELD = 10
STATUS_FIELD = 11
LENGTH_FIELD = 12
WIDTH_FIELD = 13
DRAFT_FIELD = 14
CARGO_FIELD = 15

SHIP_WHITELIST = [30, 35, 36, 37, 60, 61, 62, 63, 64, 65,\
                    66, 67, 68, 69, 70, 71, 72, 73, 74, 75,\
                    76, 77, 78, 79, 80, 81, 82, 83, 84, 85, \
                    86, 87, 88, 89]


@dataclass
class time_point:
    time: str = None
    lat: float = None
    lon: float = None
    sog: float = None
    cog: float = None
    heading: float = None
    
    def compress_time(self):
        
        time_components = self.time.split(":")
        
        h = int(time_components[0])
        m = int(time_components[1])
        s = int(time_components[2])
        
        return str(h * 3600 + m * 60 + s)

class ship:
    def __init__(self):
        self.MMSI = None
        self.date = None
        self.IMO = None
        self.callsign = None
        self.length = None
        self.width = None
        self.draft = None
        self.cargo = None
        self.vessel_type = None
        self.name = None
        self.time_series = list()  # Dictionary of time-series data (key: str, value: list[time_point])
        
        """
            LAT, LON, SOG, COG, Heading, Status
        """
    def add_ship(self,
                 MMSI: str,
                 date: str,
                 vesselName: str,
                 IMO: str,
                 callSign: str,
                 vesselType: int,
                 len: str,
                 width: str,
                 draft: str,
                 cargo: str,
                 ):
        """
        Populate the attributes of the ship with the provided values.

        Args:
        - MMSI (str): Maritime Mobile Service Identity
        - date (str): Date of registration or entry
        - vesselName (str): Name of the vessel
        - IMO (str): International Maritime Organization number
        - callSign (str): Ship's callsign
        - len (float): Length of the ship (in meters)
        - width (float): Width of the ship (in meters)
        - draft (float): Draft of the ship (in meters)
        - cargo (str): Type of cargo the ship carries
        - vesselType (int): Type of vessel (e.g., cargo, tanker, etc.)
        """
        self.MMSI = MMSI
        
        self.date = ''.join(date.split("-"))[2:]
        
        if IMO != "":
            self.IMO = IMO[3:]
        else:
            self.IMO = IMO

        self.callsign = callSign
        self.length = len
        self.width = width
        self.draft = draft
        self.cargo = cargo
        self.vessel_type = vesselType
        self.name = vesselName
        
    def add_point_data(self, 
                       time: str,
                       lat: float,
                       lon: float,
                       sog: float, 
                       cog: float, 
                       heading: float):
        """
        Add a time_point to the time_series list.

        Args:
        - time (str): The timestamp in seconds since epoch.
        - lat (float): Latitude.
        - lon (float): Longitude.
        - sog (float): Speed over ground.
        - cog (float): Course over ground.
        - heading (float): Heading.
        """
        # Create a time_point object and append it to the time_series list
        # lon *= -1
        data_point = time_point(time=time, lat=lat, lon=lon, sog=sog, cog=cog, heading=heading)
        self.time_series.append(data_point)
        
    def to_compressed_csv(self):
        """
        Generate a compressed CSV row for the ship, including all time-series data.
        """
        # Basic ship information
        ship_info = [
            self.MMSI,
            self.date,
            self.IMO,
            self.callsign,
            self.length,
            self.width,
            self.draft,
            self.cargo,
            self.vessel_type,
            self.name
        ]

        # Serialize time-series data
        time_series_data = [
            f"{tp.time};{tp.lat};{tp.lon};{tp.sog};{tp.cog};{tp.heading}"
            for tp in self.time_series
        ]
        # Join all time-series entries as a single string
        time_series_str = "|".join(time_series_data)

        # Combine ship info with the serialized time-series data
        return ",".join(map(str, ship_info)) + f',{time_series_str}'

    def to_compressed_csv(self):
        """
        Generate a compressed CSV row for the ship, including all time-series data.
        """
        # Basic ship information
        ship_info = [
            self.MMSI,
            self.date,
            self.IMO,
            self.callsign,
            self.length,
            self.width,
            self.draft,
            self.cargo,
            self.vessel_type,
            self.name
        ]

        # Serialize time-series data
        time_series_data = [
            f"{tp.compress_time()};{tp.lat};{tp.lon};{tp.sog};{tp.cog};{tp.heading}"
            for tp in self.time_series
        ]
        
        # Join all time-series entries as a single string
        time_series_str = "|".join(time_series_data)

        # Combine ship info with the serialized time-series data
        return ",".join(map(str, ship_info)) + f',{time_series_str}'


# datafile = "AIS_2016_01_01/AIS_2016_01_01.csv"
datafile = "AIS_2022_01_01/AIS_2022_01_01.csv"

from typing import Dict

ship_info: dict[str, ship] = {}

line_num = 1

with open(datafile, "r") as f:
    
    temp = f.readline()

    while(True):
        line_num += 1
        
        temp = f.readline()
        if temp == "":
            break
        
        info = temp.strip("\n").split(",")
        ship_num = info[0]
        
        if info[VESSEL_TYPE_FIELD] == '':
                continue
            
        if int(info[VESSEL_TYPE_FIELD], base = 10) not in SHIP_WHITELIST:
            continue
        
        if ship_num not in ship_info:
                        
            ship_info[ship_num] = ship()
            
            ship_info[ship_num].add_ship(
                                        info[MMSI_FIELD],
                                        info[DATETIME_FIELD].split("T")[0],
                                        info[VESSEL_NAME_FIELD],
                                        info[IMO_FIELD],
                                        info[CALL_SIGN_FIELD],
                                        info[VESSEL_TYPE_FIELD],
                                        info[LENGTH_FIELD],
                                        info[WIDTH_FIELD],
                                        info[DRAFT_FIELD],
                                        info[CARGO_FIELD],
                                        )

        ship_info[ship_num].add_point_data(info[DATETIME_FIELD].split("T")[1],
                                           float(info[LAT_FIELD]),
                                           float(info[LON_FIELD]),
                                           float(info[SOG_FIELD]),
                                           float(info[COG_FIELD]),
                                           float(info[HEADING_FIELD]),
                                           )

ship_count = 0
with open("compressed_info_3.csv", "w") as f:
    f.write("MMSI,Date,IMO,CallSign,Length,Width,Draft,Cargo,VesselType,Name,TimeSeries\n")
    for s in ship_info.values():
        f.write(s.to_compressed_csv() + "\n")
        ship_count += 1
import struct

# with open("compressed_info_3.bin", "wb") as f:
#     for s in ship_info.values():
#         # Compress ship metadata
#         metadata = [
#             int(s.MMSI),
#             int(s.date),
#             int(s.IMO) if s.IMO else 0,
#             s.callsign.encode('utf-8'),
#             float(s.length) if s.length else 0.0,
#             float(s.width) if s.width else 0.0,
#             float(s.draft) if s.draft else 0.0,
#             s.cargo.encode('utf-8'),
#             int(s.vessel_type) if s.vessel_type else 0,
#             s.name.encode('utf-8')
#         ]
        
#         # Write metadata as binary
#         f.write(struct.pack("IIIsfffsIs", *metadata))
        
#         # Compress time-series data
#         for tp in s.time_series:
#             time_data = (
#                 int(tp.compress_time()),
#                 float(tp.lat),
#                 float(tp.lon),
#                 float(tp.sog),
#                 float(tp.cog),
#                 float(tp.heading)
#             )
#             # Write time-series data as binary
            # f.write(struct.pack("Ifffff", *time_data))

print(f"Number of lines: {line_num}")
print(f"Number of ships: {ship_count}")
