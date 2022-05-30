import netifaces
from onvif import ONVIFCamera
from FileParser import file_parser
import getmac
from netifaces import interfaces, ifaddresses, AF_INET
import requests
import subprocess
import time
import pathlib
import threading


def media_profile_configuration(address):
    try:
        mycam = ONVIFCamera(address, 80, 'Admin', '1234')
        print(mycam.devicemgmt.GetDeviceInformation()['Model'])
        info = mycam.devicemgmt.GetNetworkInterfaces()[0]
        print(info['Info']['HwAddress'])
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
        pass
    else:
        return f"{a}.{b}.{c}.{d}"


def search_ip_address(first, last):
    ip_addreses = []
    for camera_ip in range(first, last + 1):
        if get_ping_result(192, 168, 15, camera_ip):
            ip_addreses.append(get_ping_result(192, 168, 15, camera_ip))
    return ip_addreses


def setup_ip_address(ip):
    subprocess.run("arp /d", creationflags=0x00000008, check=True)
    subprocess.run("ping 192.168.0.250 -n 1 -w 600", creationflags=0x00000008, check=True)
    r = (f"http://192.168.0.250/cgi-bin/param.cgi?"
         f"userName=Admin&password=1234&action=set&type=localNetwork&netCardId=1&IPProtoVer=1&"
         f"IPAddress={ip}&"
         f"subNetmask=255.255.255.0&"
         f"subGetway=192.168.15.1&preferredDNS=128.0.0.1&alternateDNS=128.0.0.2")
    try:
        result = requests.get(r)
        print(result)
        time.sleep(3)
        print("restart camera")
        result = requests.get(f"http://{ip}/cgi-bin/operate.cgi?userName=Admin&password=1234&action=restart")
        print(result)
        subprocess.run("arp /d", creationflags=0x00000008, check=True)
    except Exception as error:
        print(error)


def scan_one_ip_address(th):
    """
    Функция возвращает кортеж найденых IP адресов
    :return:
    """
    path = pathlib.Path("arp-ping.exe")
    try:
        # os.system(f"{path} 192.168.0.250 -n 20")
        with open(f'mac_{th}.txt', 'w') as output:
            process = subprocess.Popen(f"{path} 192.168.0.250 -n 20", stdout=output)
            process.communicate()
    except Exception as e:
        print(e)

def thread_scanner():
    my_thread_1 = threading.Thread(target=scan_one_ip_address, args="1")
    my_thread_2 = threading.Thread(target=scan_one_ip_address, args="2")
    my_thread_3 = threading.Thread(target=scan_one_ip_address, args="3")
    my_thread_4 = threading.Thread(target=scan_one_ip_address, args="4")
    my_thread_1.start()
    time.sleep(3)
    my_thread_2.start()
    time.sleep(3)
    my_thread_3.start()
    time.sleep(3)
    my_thread_4.start()


if __name__ == '__main__':

    print('ok')
















