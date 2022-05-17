import netifaces
from onvif import ONVIFCamera
import getmac
from netifaces import interfaces, ifaddresses, AF_INET
import requests


def media_profile_configuration(address):
    try:
        mycam = ONVIFCamera(address, 80, 'Admin', '1234')
        print(mycam.devicemgmt.GetDeviceInformation()['Model'])
        info = mycam.devicemgmt.GetNetworkInterfaces()[0]
        print(info['Info']['HwAddress'])
        mycam.devicemgmt.SystemReboot()
    except Exception as s:
        print(s)


def ip_searh(a, b, c):
    a = int(a)
    b = int(b)
    c = int(c)
    if b > 255:
        b = 255
    for x in range(a, b + 1):
        # print(f"ip=192.168.{c}.{str(x)}", 'mac=' + str(getmac.get_mac_address(ip=f"192.168.{c}.{str(x)}")))
        print('--------------------------------------------')
        print(f"ip = 192.168.{c}.{str(x)}")
        # media_profile_configuration(f"192.168.{c}.{str(x)}")
        result = requests.get(f"http://192.168.{c}.{str(x)}/cgi-bin/"
                              "param.cgi?action=get&type= deviceInfo")
        print(result.text)
        print('--------------------------------------------\n')


if __name__ == '__main__':
    # addr = netifaces.ifaddresses(interfaces()[0])
    # print(netifaces.ifaddresses(interfaces()[0]))
    # for x in addr[netifaces.AF_INET]:
    #     print(x)

    result = requests.get(f"http://192.168.15.18/cgi-bin/"
                          f"param.cgi?"
                          f"action=get&type= deviceInfo")
    print(result.text)
    resrart = "http://192.168.15.18/cgi-bin/operate.cgi?userName=Admin&password=1234&action=restart"
    info = "http://192.168.15.18/cgi-bin/param.cgi?userName=Admin&password=1234&action=get&type=cameraInfo&cameraID=1"
    network = "http://192.168.15.18/cgi-bin/param.cgi?userName=Admin&password=1234" \
              "&action=get&type=localNetwork&IPProtoVer=1&netCardId=1"
    image = "http://192.168.15.18/cgi-bin/image.cgi?userName=Admin&password=1234&cameraID=1&quality%20=5"
    r = requests.get(info)

    print(r.content)
