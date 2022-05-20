import netifaces
from onvif import ONVIFCamera
import getmac
from netifaces import interfaces, ifaddresses, AF_INET
import requests
import subprocess


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


def get_ping_result(a, b, c, d):
    cmd_str = f"ping {a}.{b}.{c}.{d} -n 1 -w 600"
    DETACHED_PROCESS = 0x00000008
    try:
        subprocess.run(cmd_str, creationflags=DETACHED_PROCESS, check=True)
    except subprocess.CalledProcessError as err:
        return False
    else:
        return f"{a}.{b}.{c}.{d}"


def search_ip_address(first, last):
    ip_addreses = []
    for camera_ip in range(first, last+1):
        if get_ping_result(192, 168, 15, camera_ip):
            ip_addreses.append(get_ping_result(192, 168, 15, camera_ip))
    return ip_addreses


def clear_arp_table():
    subprocess.run("netsh interface ip delete arpcache", creationflags=0x00000008, check=True)


if __name__ == '__main__':
    # print("Сетевые адреса")
    # addr = netifaces.ifaddresses(interfaces()[0])
    # for x in addr[netifaces.AF_INET]:
    #     print(x)
    print("Камеры")

    print(search_ip_address(50, 53))
    clear_arp_table()




