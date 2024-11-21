# import pandas as pd
# from dataclasses import dataclass
# from datetime import datetime, timezone

# # Field index constants
# MMSI_FIELD = 0
# DATETIME_FIELD = 1
# LAT_FIELD = 2
# LON_FIELD = 3
# SOG_FIELD = 4
# COG_FIELD = 5
# HEADING_FIELD = 6
# VESSEL_NAME_FIELD = 7
# IMO_FIELD = 8
# CALL_SIGN_FIELD = 9
# VESSEL_TYPE_FIELD = 10
# STATUS_FIELD = 11
# LENGTH_FIELD = 12
# WIDTH_FIELD = 13
# DRAFT_FIELD = 14
# CARGO_FIELD = 15

# SHIP_WHITELIST = [30, 35, 36, 37, 60, 61, 62, 63, 64, 65,\
#                     66, 67, 68, 69, 70, 71, 72, 73, 74, 75,\
#                     76, 77, 78, 79, 80, 81, 82, 83, 84, 85, \
#                     86, 87, 88, 89]


# @dataclass
# class time_point:
#     time: str = None
#     lat: float = None
#     lon: float = None
#     sog: float = None
#     cog: float = None
#     heading: float = None
    
#     def compress_time(self):
        
#         time_components = self.time.split(":")
        
#         h = int(time_components[0])
#         m = int(time_components[1])
#         s = int(time_components[2])
        
#         return str(h * 3600 + m * 60 + s)

# class ship:
#     def __init__(self):
#         self.MMSI = None
#         self.date = None
#         self.IMO = None
#         self.callsign = None
#         self.length = None
#         self.width = None
#         self.draft = None
#         self.cargo = None
#         self.vessel_type = None
#         self.name = None
#         self.time_series = list()  # Dictionary of time-series data (key: str, value: list[time_point])
        
#         """
#             LAT, LON, SOG, COG, Heading, Status
#         """
#     def add_ship(self,
#                  MMSI: str,
#                  date: str,
#                  vesselName: str,
#                  IMO: str,
#                  callSign: str,
#                  vesselType: int,
#                  len: str,
#                  width: str,
#                  draft: str,
#                  cargo: str,
#                  ):
#         """
#         Populate the attributes of the ship with the provided values.

#         Args:
#         - MMSI (str): Maritime Mobile Service Identity
#         - date (str): Date of registration or entry
#         - vesselName (str): Name of the vessel
#         - IMO (str): International Maritime Organization number
#         - callSign (str): Ship's callsign
#         - len (float): Length of the ship (in meters)
#         - width (float): Width of the ship (in meters)
#         - draft (float): Draft of the ship (in meters)
#         - cargo (str): Type of cargo the ship carries
#         - vesselType (int): Type of vessel (e.g., cargo, tanker, etc.)
#         """
#         self.MMSI = MMSI
        
#         self.date = ''.join(date.split("-"))[2:]
        
#         if IMO != "":
#             self.IMO = IMO[3:]
#         else:
#             self.IMO = IMO

#         self.callsign = callSign
#         self.length = len
#         self.width = width
#         self.draft = draft
#         self.cargo = cargo
#         self.vessel_type = vesselType
#         self.name = vesselName
        
#     def add_point_data(self, 
#                        time: str,
#                        lat: float,
#                        lon: float,
#                        sog: float, 
#                        cog: float, 
#                        heading: float):
#         """
#         Add a time_point to the time_series list.

#         Args:
#         - time (str): The timestamp in seconds since epoch.
#         - lat (float): Latitude.
#         - lon (float): Longitude.
#         - sog (float): Speed over ground.
#         - cog (float): Course over ground.
#         - heading (float): Heading.
#         """
#         # Create a time_point object and append it to the time_series list
#         # lon *= -1
#         data_point = time_point(time=time, lat=lat, lon=lon, sog=sog, cog=cog, heading=heading)
#         self.time_series.append(data_point)
        
#     def to_compressed_csv(self):
#         """
#         Generate a compressed CSV row for the ship, including all time-series data.
#         """
#         # Basic ship information
#         ship_info = [
#             self.MMSI,
#             self.date,
#             self.IMO,
#             self.callsign,
#             self.length,
#             self.width,
#             self.draft,
#             self.cargo,
#             self.vessel_type,
#             self.name
#         ]

#         # Serialize time-series data
#         time_series_data = [
#             f"{tp.time};{tp.lat};{tp.lon};{tp.sog};{tp.cog};{tp.heading}"
#             for tp in self.time_series
#         ]
#         # Join all time-series entries as a single string
#         time_series_str = "|".join(time_series_data)

#         # Combine ship info with the serialized time-series data
#         return ",".join(map(str, ship_info)) + f',{time_series_str}'

#     def to_compressed_csv(self):
#         """
#         Generate a compressed CSV row for the ship, including all time-series data.
#         """
#         # Basic ship information
#         ship_info = [
#             self.MMSI,
#             self.date,
#             self.IMO,
#             self.callsign,
#             self.length,
#             self.width,
#             self.draft,
#             self.cargo,
#             self.vessel_type,
#             self.name
#         ]

#         # Serialize time-series data
#         time_series_data = [
#             f"{tp.compress_time()};{tp.lat};{tp.lon};{tp.sog};{tp.cog};{tp.heading}"
#             for tp in self.time_series
#         ]
        
#         # Join all time-series entries as a single string
#         time_series_str = "|".join(time_series_data)

#         # Combine ship info with the serialized time-series data
#         return ",".join(map(str, ship_info)) + f',{time_series_str}'

# import os
# import requests
# import zipfile
# import re

# def download_zip(url: str, download_path: str):
#     """
#     Downloads a zip file from the given URL to the current working directory.

#     Args:
#     - url (str): The URL to download the zip file from.

#     Returns:
#     - str: The local path of the downloaded zip file.
#     """
    
#     filename = url.split("/")[-1]  # Extract the filename from the URL
#     local_path = os.path.join(download_path, filename)  # Save in the current directory
    
#     # Download the file
#     response = requests.get(url, stream=True)
#     if response.status_code == 200:
#         with open(local_path, "wb") as f:
#             for chunk in response.iter_content(chunk_size=1024):
#                 f.write(chunk)
#         print(f"Downloaded: {filename}")
#     else:
#         raise Exception(f"Failed to download {url}. HTTP status code: {response.status_code}")

#     return local_path


# def unzip_raw_data(zip_file_path: str, extract_path: str):
#     """
#     Extracts the given zip file to the specified directory.

#     Args:
#     - zip_file (str): Path to the zip file to extract.
#     - extract_path (str): Path where the zip file should be extracted.

#     Returns:
#     - str: The path of the extracted CSV file(s).
#     """
    
#     file = zip_file_path.split("/")[-1]
#     csv_file = re.sub(".zip", ".csv", file)
#     csv_path = os.path.join(extract_path, csv_file)
#     print(csv_path)
    
#     if not os.path.exists(extract_path):
#         os.makedirs(extract_path)  # Create the extraction path if it doesn't exist

#     with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
#         zip_ref.extractall(path = extract_path)
#         print(f"Extracted: {zip_file_path} to {extract_path}")

#     return extract_path + csv_file

# from datetime import date, timedelta

# def generate_files_for_year(year):
#     """
#     Generate a list of file names for each day of a given year.

#     Args:
#     - year (int): The year for which to generate the file names.

#     Returns:
#     - list: A list of file names in the format 'AIS_YYYY_MM_DD.zip'.
#     """
#     start_date = date(year, 1, 1)
#     end_date = date(year, 12, 31)
#     delta = timedelta(days=1)

#     files = []
#     current_date = start_date
#     while current_date <= end_date:
#         files.append(f"AIS_{current_date.strftime('%Y_%m_%d')}.zip")
#         current_date += delta

#     return files

# files = generate_files_for_year(2020)

# ship_info: dict[str, ship] = {}

# line_num = 1

# site = "https://coast.noaa.gov/htdata/CMSP/AISDataHandler/2020/"
# unzip_path = "raw_data/"
# download_path = "downloads/"
# compressed_folder = "compressed_data/"

# for data_file in files:
#     ship_info = {}
#     url = site + data_file
    
#     downloaded_zip_path = download_zip(url, download_path)
#     csv_file_location = unzip_raw_data(downloaded_zip_path, unzip_path)
#     line_num=1
    
#     with open(csv_file_location, "r") as f:
        
#         temp = f.readline()

#         while(True):
#             line_num += 1
            
#             temp = f.readline()
#             if temp == "":
#                 break
            
#             info = temp.strip("\n").split(",")
#             ship_num = info[0]
            
#             if info[VESSEL_TYPE_FIELD] == '':
#                     continue
                
#             if int(info[VESSEL_TYPE_FIELD], base = 10) not in SHIP_WHITELIST:
#                 continue
            
#             if ship_num not in ship_info:
                            
#                 ship_info[ship_num] = ship()
                
#                 ship_info[ship_num].add_ship(
#                                             info[MMSI_FIELD],
#                                             info[DATETIME_FIELD].split("T")[0],
#                                             info[VESSEL_NAME_FIELD],
#                                             info[IMO_FIELD],
#                                             info[CALL_SIGN_FIELD],
#                                             info[VESSEL_TYPE_FIELD],
#                                             info[LENGTH_FIELD],
#                                             info[WIDTH_FIELD],
#                                             info[DRAFT_FIELD],
#                                             info[CARGO_FIELD],
#                                             )

#             ship_info[ship_num].add_point_data(info[DATETIME_FIELD].split("T")[1],
#                                             float(info[LAT_FIELD]),
#                                             float(info[LON_FIELD]),
#                                             float(info[SOG_FIELD]),
#                                             float(info[COG_FIELD]),
#                                             float(info[HEADING_FIELD]),
#                                             )

#     ship_count = 0
    
#     compressed_path = compressed_folder + re.sub(".zip", ".csv", data_file)
    
#     with open(compressed_path, "w") as f:
#         f.write("MMSI,Date,IMO,CallSign,Length,Width,Draft,Cargo,VesselType,Name,TimeSeries\n")
#         for s in ship_info.values():
#             f.write(s.to_compressed_csv() + "\n")
#             ship_count += 1

#     print(f"File compressed: {data_file}")
#     print(f"Number of lines (O): {line_num}")
#     print(f"Number of ships (C): {ship_count}")
#     # os.remove(csv_file_location)
#     os.remove(downloaded_zip_path)
# # import struct

# # with open("compressed_info_3.bin", "wb") as f:
# #     for s in ship_info.values():
# #         # Compress ship metadata
# #         metadata = [
# #             int(s.MMSI),
# #             int(s.date),
# #             int(s.IMO) if s.IMO else 0,
# #             s.callsign.encode('utf-8'),
# #             float(s.length) if s.length else 0.0,
# #             float(s.width) if s.width else 0.0,
# #             float(s.draft) if s.draft else 0.0,
# #             s.cargo.encode('utf-8'),
# #             int(s.vessel_type) if s.vessel_type else 0,
# #             s.name.encode('utf-8')
# #         ]
        
# #         # Write metadata as binary
# #         f.write(struct.pack("IIIsfffsIs", *metadata))
        
# #         # Compress time-series data
# #         for tp in s.time_series:
# #             time_data = (
# #                 int(tp.compress_time()),
# #                 float(tp.lat),
# #                 float(tp.lon),
# #                 float(tp.sog),
# #                 float(tp.cog),
# #                 float(tp.heading)
# #             )
# #             # Write time-series data as binary
#             # f.write(struct.pack("Ifffff", *time_data))
import os
import requests
import zipfile
import re
from datetime import date, timedelta
from concurrent.futures import ThreadPoolExecutor, as_completed
import pandas as pd
from dataclasses import dataclass
import time
import shutil
import csv
from collections import defaultdict

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

SHIP_WHITELIST = set([30, 35, 36, 37, 60, 61, 62, 63, 64, 65,
                    66, 67, 68, 69, 70, 71, 72, 73, 74, 75,
                    76, 77, 78, 79, 80, 81, 82, 83, 84, 85,
                    86, 87, 88, 89])

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
        self.time_series = list()

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
        self.MMSI = MMSI
        self.date = ''.join(date.split("-"))[2:]
        self.IMO = re.sub("IMO", "", IMO)
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
        data_point = time_point(time=time, lat=lat, lon=lon, sog=sog, cog=cog, heading=heading)
        self.time_series.append(data_point)

    def to_compressed_csv(self):
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
        time_series_data = [
            f"{tp.compress_time()};{tp.lat};{tp.lon};{tp.sog};{tp.cog};{tp.heading}"
            for tp in self.time_series
        ]
        time_series_str = "|".join(time_series_data)
        return ",".join(map(str, ship_info)) + f',{time_series_str}'

def download_zip(url: str, download_path: str):
    filename = url.split("/")[-1]
    local_path = os.path.join(download_path, filename)

    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(local_path, "wb") as f:
            # Use shutil.copyfileobj to copy the streamed content to the file
            shutil.copyfileobj(response.raw, f)
        print(f"Downloaded: {filename}")
    else:
        raise Exception(f"Failed to download {url}. HTTP status code: {response.status_code}")

    return local_path

def unzip_raw_data(zip_file_path: str, extract_path: str):
    file = zip_file_path.split("/")[-1]
    csv_file = re.sub(".zip", ".csv", file)
    csv_path = os.path.join(extract_path, csv_file)

    if not os.path.exists(extract_path):
        os.makedirs(extract_path)

    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(path=extract_path)
        print(f"Extracted: {zip_file_path} to {extract_path}")

    return csv_path

def generate_files_for_year(year):
    start_date = date(year, 1, 1)
    end_date = date(year, 12, 31)
    delta = timedelta(days=1)

    files = []
    current_date = start_date
    while current_date <= end_date:
        files.append(f"AIS_{current_date.strftime('%Y_%m_%d')}.zip")
        current_date += delta

    return files

# Main processing function for a single file
def process_file(data_file, site, download_path, unzip_path, compressed_folder, ship_info_template):
    s_time = time.time()
    try:
        url = site + data_file

        # Download the zip file
        downloaded_zip_path = download_zip(url, download_path)

        # Unzip the raw data
        csv_file_location = unzip_raw_data(downloaded_zip_path, unzip_path)

        # Process the data
        ship_info = defaultdict(ship)
        line_num = 1

        with open(csv_file_location, "r") as f:
            reader = csv.reader(f)
            next(reader)  # Skip header
            for info in reader:
                # line_num += 1
                # temp = f.readline()
                # if temp == "":
                    # break

                # info = line.strip("\n").split(",")
                ship_num = info[0]
                
                if info[VESSEL_TYPE_FIELD] == '' or\
                    int(info[VESSEL_TYPE_FIELD], base=10) not in SHIP_WHITELIST:
                    continue
                
                date, time_info = info[DATETIME_FIELD].split("T")
                
                if ship_num not in ship_info:
                    ship_info[ship_num].add_ship(
                        info[MMSI_FIELD],
                        date,
                        info[VESSEL_NAME_FIELD],
                        info[IMO_FIELD],
                        info[CALL_SIGN_FIELD],
                        info[VESSEL_TYPE_FIELD],
                        info[LENGTH_FIELD],
                        info[WIDTH_FIELD],
                        info[DRAFT_FIELD],
                        info[CARGO_FIELD],
                    )

                ship_info[ship_num].add_point_data(
                    time_info,
                    float(info[LAT_FIELD]),
                    float(info[LON_FIELD]),
                    float(info[SOG_FIELD]),
                    float(info[COG_FIELD]),
                    float(info[HEADING_FIELD]),
                )

        # Save compressed data
        print(f"Processesd: {data_file}")
        compressed_path = os.path.join(compressed_folder, re.sub(".zip", ".csv", data_file))
        with open(compressed_path, "w") as f:
            f.write("MMSI,Date,IMO,CallSign,Length,Width,Draft,Cargo,VesselType,Name,TimeSeries\n")
            for s in ship_info.values():
                f.write(s.to_compressed_csv() + "\n")
        print(f"Compressed: {data_file}")
        # Cleanup
        os.remove(csv_file_location)
        os.remove(downloaded_zip_path)
        
        e_time = time.time()
        return f"Processed: {data_file} in {e_time - s_time} seconds"

    except Exception as e:
        print(f"Error processing {data_file}: {e}")
        return f"Error: {data_file}"

# Multi-threaded processing
def process_files_concurrently(files, site, download_path, unzip_path, compressed_folder, ship_info_template, max_workers=5):
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {
            executor.submit(
                process_file, data_file, site, download_path, unzip_path, compressed_folder, ship_info_template
            ): data_file
            for data_file in files
        }
        for future in as_completed(futures):
            data_file = futures[future]
            try:
                result = future.result()
                print(result)
            except Exception as exc:
                print(f"{data_file} generated an exception: {exc}")

# Usage
site = "https://coast.noaa.gov/htdata/CMSP/AISDataHandler/2020/"
unzip_path = "raw_data/"
download_path = "downloads/"
compressed_folder = "compressed_data/"

files = generate_files_for_year(2020)
# print(files[0])
time_start = time.time()
process_files_concurrently(files[0:5], site, download_path, unzip_path, compressed_folder, lambda: {})
print(f"Time to process all files: {time.time() - time_start}")
