import tinytuya
import sys
import os
import datetime
import time
from csv import DictReader

def main():
    if len(sys.argv) == 0:
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
        if isgoodipv4(Dev['DeviceIP']):
            print("Processing Device "+Dev['DeviceID']+"...")
            get_info(Dev)
                          
def get_info(Dev):
    d = tinytuya.OutletDevice(Dev['DeviceID'], Dev['DeviceIP'], Dev['DeviceKey'])
    try:
        d.set_version(float(Dev['Version']))
    except:
        d.set_version(3.3)
    data = d.status()
    print('Got data:'+str(data))
    results = {
      "indoorTemp": data['dps']['131'],
      "indoorHum": data['dps']['132'],
      "OutFile": Dev['OutFile']
    }
    if hasattr(data['dps'], '133'):
        results['sub1Temp'] = data['dps']['133']
    if hasattr(data['dps'], '134'):
        results['sub1Hum'] = data['dps']['134']
    if hasattr(data['dps'], '135'):
        results['sub2Temp'] = data['dps']['135']
    if hasattr(data['dps'], '136'):
        results['sub2Hum'] = data['dps']['136']
    if hasattr(data['dps'], '137'):
        results['sub3Temp'] = data['dps']['137']
    if hasattr(data['dps'], '138'):
        results['sub3Hum'] = data['dps']['138']
    write_info(results)
                              
def write_info(data):
    print('Writing to '+data['OutFile'])
    now = datetime.datetime.now()
    f = open(data['OutFile'], "w")
    f.write("time:"+now.strftime("%Y-%m-%d %H:%M:%S")+'\n')
    f.write("temperature:"+str(data['indoorTemp']/10)+'\n')
    f.write("humidity:"+str(data['indoorHum'])+'\n')
    f.write("dewpt:"+str((data['indoorTemp']/10)-((100-data['indoorHum'])/5))+'\n')
    f.close()
    if hasattr(data, 'sub1Temp'):
        f = open(os.path.splitext(data['OutFile'])[0]+'-sub1'+os.path.splitext(data['OutFile'])[1], "w")
        f.write("time:"+now.strftime("%Y-%m-%d %H:%M:%S")+'\n')
        f.write("temperature:"+str(data['sub1Temp']/10)+'\n')
        f.write("humidity:"+str(data['sub1Hum'])+'\n')
        f.write("dewpt:"+str((data['sub1Temp']/10)-((100-data['sub1Hum'])/5))+'\n')
        f.close()
    if hasattr(data, 'sub2Temp'):
        f = open(os.path.splitext(data['OutFile'])[0]+'-sub1'+os.path.splitext(data['OutFile'])[1], "w")
        f.write("time:"+now.strftime("%Y-%m-%d %H:%M:%S")+'\n')
        f.write("temperature:"+str(data['sub2Temp']/10)+'\n')
        f.write("humidity:"+str(data['sub2Hum'])+'\n')
        f.write("dewpt:"+str((data['sub2Temp']/10)-((100-data['sub2Hum'])/5))+'\n')
        f.close()
    if hasattr(data, 'sub3Temp'):
        f = open(os.path.splitext(data['OutFile'])[0]+'-sub1'+os.path.splitext(data['OutFile'])[1], "w")
        f.write("time:"+now.strftime("%Y-%m-%d %H:%M:%S")+'\n')
        f.write("temperature:"+str(data['sub3Temp']/10)+'\n')
        f.write("humidity:"+str(data['sub3Hum'])+'\n')
        f.write("dewpt:"+str((data['sub3Temp']/10)-((100-data['sub3Hum'])/5))+'\n')
        f.close()

def isgoodipv4(s):
    pieces = s.split(".")
    if len(pieces) != 4:
        return False
    try:
        return all(0 <= int(p) < 256 for p in pieces)
    except ValueError:
        return False

if __name__ == "__main__":
    sys.exit(main())
