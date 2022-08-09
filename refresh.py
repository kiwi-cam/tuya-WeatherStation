import tinytuya
import sys
import os
import datetime
from csv import DictReader

def main():
    if len(sys.argv) != 1:
        print("This script requires one argument:")
        print("<Required> A csv file with a list of Weather Stations including DeviceID,DeviceIP,DeviceKey,Version,OutFile")
        sys.exit(1)
        
    DevListFile = str(sys.argv[1]).strip()
    #Test Path is Valid
    if not os.path.isfile(DevListFile):
        print("<Invalid> The supplied csv file needs to contain a list of Weather Stations including DeviceID,DeviceIP,DeviceKey,Version,OutFile")
        sys.exit(1)
        
    # open file in read mode
    with open(DevListFile, 'r') as read_obj:
        # pass the file object to DictReader() to get the DictReader object
        dict_reader = DictReader(read_obj)
        # get a list of dictionaries from dct_reader
        DevList = list(dict_reader)
        
    for Dev in DevList:
        if isgoodipv4(Dev['DeviceIP]):
            print("Processing Device "+Dev['DeviceID']+"...")
            get_info(Dev)
                          
def get_info(Dev):
    d = tinytuya.OutletDevice(Dev['DeviceID'], Dev['DeviceIP'], Dev['DeviceKey'])
    d.set_version(Dev['Version'] || 3.3)
    data = d.status()
    results = {
      "indoorTemp" = data['dps']['131],
      "indoorHum" = data['dps']['132],
      "sub1Temp" = data['dps']['133],
      "sub1Hum" = data['dps']['134],
      "sub2Temp" = data['dps']['135],
      "sub2Hum" = data['dps']['136],
      "sub3Temp" = data['dps']['135],
      "sub3Hum" = data['dps']['136],
      "OutFile" = Dev['OutFile']
    }
    write_info(results)
                              
def write_info(data):
    now = datetime.datetime.now()
    f = open(data['OutFile'], "w")
    f.write("time:"+now.strftime("%Y-%m-%d %H:%M:%S"))
    f.write("temperature:"+data['indoorTemp])
    f.write("humidity:"+data['indoorHum])
    f.write("dewpt:"+(data['indoorTemp]-((100-data['indoorHum])/5)))