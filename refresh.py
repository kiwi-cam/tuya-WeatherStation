import tinytuya
import sys
import os
import socket
import datetime
import time
from csv import DictReader
import logging
from systemd.journal import JournalHandler

daemon = False
log = logging.getLogger('tuya-WeatherStation')
log.addHandler(JournalHandler(SYSLOG_IDENTIFIER='tuya-WeatherStation'))
log.setLevel(logging.INFO)

def main():
    global daemon
    if len(sys.argv) == 0:
        print("This script requires at least one argument:")
        log.error("This script requires at least one argument")
        print("<Required> A csv file with a list of Weather Stations including DeviceID,DeviceIP,DeviceKey,Version,OutFile")
        print("<Optional> -D or --daemon will make the script run constantly, polling every 30 seconds")
        sys.exit(1)
    
    for Arg in sys.argv:
        if Arg == '-D' or Arg == '--debug':
            daemon = True
        else:    
            DevListFile = str(Arg).strip()

    #Test Path is Valid
    if not os.path.isfile(DevListFile):
        print("<Invalid> The supplied csv file needs to contain a list of Weather Stations including DeviceID,DeviceIP,DeviceKey,Version,OutFile")    
        log.error("The supplied csv file needs to contain a list of Weather Stations")
        sys.exit(1)
        
    # open file in read mode
    with open(DevListFile, 'r') as read_obj:
        # pass the file object to DictReader() to get the DictReader object
        dict_reader = DictReader(read_obj)
        # get a list of dictionaries from dct_reader
        DevList = list(dict_reader)

    poll_list(DevList)
    while daemon:
        time.sleep(30)
        poll_list(DevList)        

def poll_list(DevList):
    for Dev in DevList:
        if not isgoodipv4(Dev['DeviceIP']):
            Dev['DeviceIP'] = socket.gethostbyname(Dev['DeviceIP'])
        if isgoodipv4(Dev['DeviceIP']):
            if not daemon: print("Processing Device "+Dev['DeviceID']+"("+Dev['DeviceIP']+")...")
            log.info("Processing Device "+Dev['DeviceID']+"("+Dev['DeviceIP']+")...")
            get_info(Dev)
        else:
            print("Unable to resolve "+Dev['DeviceID']+" at "+Dev['DeviceIP'])
            log.info("Unable to resolve "+Dev['DeviceID']+" at "+Dev['DeviceIP'])

def get_info(Dev):
    d = tinytuya.OutletDevice(Dev['DeviceID'], Dev['DeviceIP'], Dev['DeviceKey'])
    try:
        d.set_version(float(Dev['Version']))
    except:
        d.set_version(3.3)
    data = d.status()
    if not daemon: print('Got data:'+str(data))
    log.info('Got data:'+str(data))
    if 'dps' in data:
        results = {
        "indoorTemp": data['dps']['131'],
        "indoorHum": data['dps']['132'],
        "OutFile": Dev['OutFile']
        }
        if '133' in data['dps']:
            results['sub1Temp'] = data['dps']['133']
        if '134' in data['dps']:
            results['sub1Hum'] = data['dps']['134']
        if '135' in data['dps']:
            results['sub2Temp'] = data['dps']['135']
        if '136' in data['dps']:
            results['sub2Hum'] = data['dps']['136']
        if '137' in data['dps']:
            results['sub3Temp'] = data['dps']['137']
        if '138' in data['dps']:
            results['sub3Hum'] = data['dps']['138']
        write_info(results)
    else:
        print('Error getting data')
        log.warning('Error getting data')
        exit()    
                              
def write_info(data):
    if not daemon: print('Writing to '+data['OutFile']+' '+str(data['indoorTemp']/10)+':'+str(data['indoorHum']))
    log.info('Writing to '+data['OutFile']+' '+str(data['indoorTemp']/10)+':'+str(data['indoorHum']))
    now = datetime.datetime.now()
    f = open(data['OutFile'], "w")
    f.write("time:"+now.strftime("%Y-%m-%d %H:%M:%S")+'\n')
    f.write("temperature:"+str(data['indoorTemp']/10)+'\n')
    f.write("humidity:"+str(data['indoorHum'])+'\n')
    f.write("dewpt:"+str(round((data['indoorTemp']/10)-((100-data['indoorHum'])/5),2))+'\n')
    f.close()
    if 'sub1Temp' in data:
        if not daemon: print('Writing to '+os.path.splitext(data['OutFile'])[0]+'-sub1'+os.path.splitext(data['OutFile'])[1]+' '+str(data['sub1Temp']/10)+':'+str(data['sub1Hum']))
        log.info('Writing to '+os.path.splitext(data['OutFile'])[0]+'-sub1'+os.path.splitext(data['OutFile'])[1]+' '+str(data['sub1Temp']/10)+':'+str(data['sub1Hum']))
        f = open(os.path.splitext(data['OutFile'])[0]+'-sub1'+os.path.splitext(data['OutFile'])[1], "w")
        f.write("time:"+now.strftime("%Y-%m-%d %H:%M:%S")+'\n')
        f.write("temperature:"+str(data['sub1Temp']/10)+'\n')
        f.write("humidity:"+str(data['sub1Hum'])+'\n')
        f.write("dewpt:"+str(round((data['sub1Temp']/10)-((100-data['sub1Hum'])/5),2))+'\n')
        f.close()
    if 'sub2Temp' in data:
        if not daemon: print('Writing to '+os.path.splitext(data['OutFile'])[0]+'-sub2'+os.path.splitext(data['OutFile'])[1]+' '+str(data['sub2Temp']/10)+':'+str(data['sub2Hum']))
        log.info('Writing to '+os.path.splitext(data['OutFile'])[0]+'-sub2'+os.path.splitext(data['OutFile'])[1]+' '+str(data['sub2Temp']/10)+':'+str(data['sub2Hum']))
        f = open(os.path.splitext(data['OutFile'])[0]+'-sub2'+os.path.splitext(data['OutFile'])[1], "w")
        f.write("time:"+now.strftime("%Y-%m-%d %H:%M:%S")+'\n')
        f.write("temperature:"+str(data['sub2Temp']/10)+'\n')
        f.write("humidity:"+str(data['sub2Hum'])+'\n')
        f.write("dewpt:"+str(round((data['sub2Temp']/10)-((100-data['sub2Hum'])/5),2))+'\n')
        f.close()
    if 'sub3Temp' in data:
        if not daemon: print('Writing to '+os.path.splitext(data['OutFile'])[0]+'-sub3'+os.path.splitext(data['OutFile'])[1]+' '+str(data['sub3Temp']/10)+':'+str(data['sub3Hum']))
        log.info('Writing to '+os.path.splitext(data['OutFile'])[0]+'-sub3'+os.path.splitext(data['OutFile'])[1]+' '+str(data['sub3Temp']/10)+':'+str(data['sub3Hum']))
        f = open(os.path.splitext(data['OutFile'])[0]+'-sub3'+os.path.splitext(data['OutFile'])[1], "w")
        f.write("time:"+now.strftime("%Y-%m-%d %H:%M:%S")+'\n')
        f.write("temperature:"+str(data['sub3Temp']/10)+'\n')
        f.write("humidity:"+str(data['sub3Hum'])+'\n')
        f.write("dewpt:"+str(round((data['sub3Temp']/10)-((100-data['sub3Hum'])/5),2))+'\n')
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
