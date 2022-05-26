import netifaces
from onvif import ONVIFCamera
import getmac
from netifaces import interfaces, ifaddresses, AF_INET
import requests
import subprocess
import time
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


def scan_one_ip_address():
    """
    Функция возвращает кортеж найденых IP адресов
    :return:
    """
    r1 = int("0x00", 16)
    r2 = int("0x5f", 16)
    r3 = int("0x03", 16)
    r4 = int("0x88", 16)
    r5 = int("0x7f", 16)
    r6 = int("0xe0", 16)

    mac = f"{hex(r6)[2:]}-{hex(r5)[2:]}-{hex(r4)[2:]}-{hex(r3)[2:]}-{hex(r2)[2:]}-{hex(r1)[2:]}"
    subprocess.run(f"arp /d", creationflags=0x00000008, check=True)
    subprocess.run(f"arp /s 192.168.0.250 {mac}", creationflags=0x00000008, check=True)
    try:
        print(subprocess.run(f"ping 192.168.0.250 -n 1 -w 600", creationflags=0x00000008, check=True))

    except Exception as e:
        print(f"Not found {mac}")


    # time.sleep(1)
    # r1 = int("0xff", 16)
    # mac = f"{hex(r6)[2:]}-{hex(r5)[2:]}-{hex(r4)[2:]}-{hex(r3)[2:]}-{hex(r2)[2:]}-{hex(r1)[2:]}"
    # subprocess.run(f"arp /d", creationflags=0x00000008, check=True)
    # subprocess.run(f"arp /s 192.168.0.250 "
    #                f"{mac}",
    #                creationflags=0x00000008, check=True)
    # try:
    #     subprocess.run(f"ping 192.168.0.250 -n 1 -w 600", creationflags=0x00000008, check=True)
    #     print(r1)
    # except Exception as e:
    #     print(f"Not found {mac}")


if __name__ == '__main__':
    # print("Сетевые адреса")
    # addr = netifaces.ifaddresses(interfaces()[0])
    # for x in addr[netifaces.AF_INET]:
    #     print(x)
    # print("Камеры")
    # clear_arp_table()
    # print(search_ip_address(50, 53))
    # subprocess.call('arp -a', shell=True)
    # print(search_ip_address(52, 53))

    # clear_arp_table()
    # subprocess.call('arp -a', shell=True)

    # setup_ip_address('192.168.15.52')
    # setup_ip_address('192.168.15.58')
    scan_one_ip_address()

