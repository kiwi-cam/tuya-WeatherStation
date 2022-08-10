# tuya-WeatherStation
A python script based on tinytuya to extract current information from Tuya Weather stations. This was setup for a [qxj device](https://www.amazon.com/Wireless-Thermometer-Hygrometer-Backlight-Greenhouse/dp/B096ZV55G2/ref=cm_cr_arp_d_product_top?ie=UTF8)
![image](https://user-images.githubusercontent.com/32912464/184027000-2e26a103-5e41-4b40-8374-31b5293b49e5.png)

Requires one argument of a csv file containing information of the devices to be polled.  The file must contain these fields, including headings: DeviceID,DeviceIP,DeviceKey,Version,OutFile.

Example:<br />
DeviceID,DeviceIP,DeviceKey,Version,OutFile<br />
asdf1234,192.168.1.123,lkjh9876,3.3,/var/tmp/tuya.txt

For details on obtaining the device details, refer to [the tinytuya documentation](https://github.com/jasonacox/tinytuya#setup-wizard---getting-local-keys).

The device IP can be either the hostname or the IP address. Just make sure the hostname is resolvable or that the IP won't change.

The other optional argument is -D or --daemon which will make the script run constantly, polling every 30 seconds. This is useful if you'd like to run as a systemd service (refer to [the example](https://github.com/kiwi-cam/tuya-WeatherStation/blob/main/tuyaWeatherStation.service))
