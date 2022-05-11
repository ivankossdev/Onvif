import netifaces
import onvif
from onvif import ONVIFCamera
import getmac
from netifaces import interfaces, ifaddresses, AF_INET


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
        media_profile_configuration(f"192.168.{c}.{str(x)}")
        print('--------------------------------------------\n')


if __name__ == '__main__':
    addr = netifaces.ifaddresses(interfaces()[0])
    for x in addr[netifaces.AF_INET]:
        print(x)
    my_cam = onvif.ONVIFCamera('192.168.15.18', 80, 'Admin', '1234')
    print(my_cam.devicemgmt.GetDeviceInformation())
    print(my_cam.devicemgmt.GetUsers())
    # try:
    #     my_cam.devicemgmt.CreateUsers('User', 'User', 'User', 'User')
    #     print(my_cam.devicemgmt.GetUsers())
    # except Exception as e:
    #     print(e)
    ip_searh(20, 28, 15)


