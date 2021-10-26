import os
import platform
import subprocess
import utils
import re
import random
from texttable import Texttable
import json
import sys

def isRoot():
    return False if os.geteuid() != 0 else True

def InitCheck():
    if isRoot() != True:
        print(f"{utils.CColor.RED}[ERROR] Execute the Script as Root user! (Execute with sudo..)\33[37m")
        exit()
    CheckOS()
    VirtCheck()

def VirtCheck():
    CheckResult=executeSystemCommand("systemd-detect-virt")

    if CheckResult in utils.unsupported_virts:
        print(f"{utils.CColor.RED}[ERROR] Your virtual-enviroment: {CheckResult} is not supported by Wireguard!")
        exit()

def CheckOS():
    OSOut = getOS()
    returnos=""
    if os.path.exists("/etc/debian_version"):
        returnos=OSOut
        if OSOut == "debian" or OSOut == "raspbian":
            if int(getOSVersion()) < 10:
                    print("You are using an outdated Version of Debian: " + getOSVersion())
            returnos = "debian"
    elif  os.path.exists("/etc/fedora-release"):
        returnos = OSOut
    elif os.path.exists("/etc/centos-release"):
       returnos =  "centos"
    elif os.path.exists("/etc/arch-release"):
        returnos = "arch"
    else:
        print("You are trying to install XGuard on an Invalid System!")
        exit()
    
    return returnos


def executeSystemCommand(inputcmd):
    output = subprocess.getoutput(inputcmd)
    return output

def getOS():
    with open("/etc/os-release") as f:
        d={}
        for line in f:
            k,v = line.rstrip().split("=")
            d[k] = v.strip('"') 
        return d['ID']
    
def getOSVersion():
    with open("/etc/os-release") as f:
        d={}
        for line in f:
            k,v = line.rstrip().split("=")
            d[k] = v.strip('"') 
        return d['VERSION_ID']





def InstallQuestions():

    print(f"""{utils.CColor.UNDERLINE}{utils.CColor.YELLOW}{utils.CColor.BOLD}Welcome to Wireguard Installer{utils.CColor.RESET}
{utils.CColor.RESET}{utils.CColor.YELLOW}Before I can start the setup of wireguard I need you to ask some important questions.
If you don't know what to enter exactly check the documentation on the github repository.

{utils.CColor.MAGENTA}+=======================================================================================+{utils.CColor.RESET}
    """)



    PI_IP=executeSystemCommand("ifconfig | grep -Eo 'inet (addr:)?([0-9]*\.){3}[0-9]*' | grep -Eo '([0-9]*\.){3}[0-9]*' | grep -v '127.0.0.1' | head -1")
    

    print(f"{utils.CColor.CYAN}(0/8) {utils.CColor.BOLD}Enter the IP of your Main Network Interface:{utils.CColor.RESET}")
    PI_IP = utils.PreInput("> ", PI_IP)



    utils.MainBanner()

    PI_NAM=executeSystemCommand("ip -4 route ls | grep default | grep -Po '(?<=dev )(\S+)' | head -1")
    print(f"""
{utils.CColor.CYAN}(1/7) {utils.CColor.BOLD}Enter the name of your Main Network Interface:{utils.CColor.RESET}""")
    PI_NAM = utils.PreInput("> ", PI_NAM)


    utils.MainBanner()
    WG_INTERFACE=""
    print(f"""
{utils.CColor.CYAN}(2/7) {utils.CColor.BOLD}Enter the name of your new Wireguard Network Interface{utils.CColor.RESET}""")
    WG_INTERFACE = utils.PreInput("> ", "wg0")



    utils.MainBanner()
    WG_IPv4=""
    while bool(re.match(utils.IPv4_Regex, WG_IPv4)) != True:
        print(f"""
{utils.CColor.CYAN}(3/7) {utils.CColor.BOLD}Enter the new IPv4 Address of your new WireGuard Interface:{utils.CColor.RESET}""")
        WG_IPv4= utils.PreInput("> ", "10.0.0.1")


    utils.MainBanner()
    WG_IPv6=""
    while bool(re.match(utils.IPv6_Regex, WG_IPv6)) != True:
        print(f"""
{utils.CColor.CYAN}(4/7) {utils.CColor.BOLD}Enter the new IPv6 Address of your new WireGuard Interface:{utils.CColor.RESET}""")
        WG_IPv6= utils.PreInput("> ", "fd42:42:42::1")



    utils.MainBanner()
    WG_PORT=""
    WG_RANDOM_Port=""
    while bool(re.match(utils.Int_Regex, WG_PORT)) != True:
        WG_RANDOM_Port=random.randint(49152, 65535)
        print(f"""
{utils.CColor.CYAN}(5/7) {utils.CColor.BOLD}Enter the new IPv6 Address of your new WireGuard Interface:{utils.CColor.RESET}""")
        WG_PORT=utils.PreInput("> ", str(WG_RANDOM_Port))



    utils.MainBanner()
    FIRST_DNS=""
    while bool(re.match(utils.IPv4_Regex, FIRST_DNS)) != True:
        print(f"""
{utils.CColor.CYAN}(6/7) {utils.CColor.BOLD}Enter your first DNS Resolver:{utils.CColor.RESET}""")
        FIRST_DNS= utils.PreInput("> ", "46.182.19.48")


    utils.MainBanner()
    SECOND_DNS=""
    while bool(re.match(utils.IPv4_Regex, SECOND_DNS)) != True:
        print(f"""
{utils.CColor.CYAN}(7/7) {utils.CColor.BOLD}Enter your second DNS Resolver:{utils.CColor.RESET}""")
        SECOND_DNS= utils.PreInput("> ", "1.1.1.1")

    utils.MainBanner()


    print("All configuration is done. Here an overview:\n")

    t = Texttable()
    t.add_rows([['Option', 'Setting'], ['Main Interface IP', PI_IP], ['Main Interface Name', PI_NAM], ['WG Interface Name', WG_INTERFACE], ['WG Interface IPv4', WG_IPv4], ['WG Interface IPv6', WG_IPv6], ['WG Port', WG_PORT], ['Primary DNS Server', FIRST_DNS], ['Second DNS Server', SECOND_DNS]])
    print(t.draw())

    input("Press Enter to Continue!")

    StartInstall(PI_IP, PI_NAM, WG_INTERFACE, WG_IPv4, WG_IPv6, WG_PORT, FIRST_DNS, SECOND_DNS)






def StartInstall(MI, MIM, WGI, WG4, WG6, WGP, DNS1, DNS2):
    OS=CheckOS()

    if OS == "ubuntu" or OS == "debian" and int(getOSVersion()) > 10:
        print("Updating Packages..")
        os.system("apt-get update > /dev/null")
        print("Installing all needed Packages..")
        os.system("apt-get install -y wireguard iptables qrencode > /dev/null")
    elif OS == "debian":
        print("Installing Backports..")
        os.system('''echo "deb http://deb.debian.org/debian buster-backports main" >/etc/apt/sources.list.d/backports.list
        apt-get update > /dev/null''')

        print("Installing all needed Packages..")
        os.system('''apt-get install -y iptables > /dev/null
        apt-get install -y  wireguard qrencode > /dev/null''')
    elif OS == "fedora":
        print("Installing all needed Packages..")
        if int(getOSVersion()) < 32:
            os.system('''dnf install -y dnf-plugins-core > /dev/null
			dnf copr enable -y jdoss/wireguard > /dev/null
			dnf install -y wireguard-dkms > /dev/null''')
        os.system('dnf install -y wireguard-tools iptables qrencode > /dev/null')
    elif OS == "centos":
        print("Installing all needed Packages..")
        os.system('yum -y install epel-release elrepo-release qrencode > /dev/null')
        if int(getOSVersion()) == 7:
            os.system('yum -y install yum-plugin-elrepo > /dev/null')
        os.system('yum -y install kmod-wireguard wireguard-tools iptables qrencode > /dev/null')
    elif OS == "arch":
        print("Installing all needed Packages..")
        os.system('pacman -S --needed --noconfirm wireguard-tools qrencode > /dev/null')


   
    

    if not os.path.exists("/etc/wireguard"):
        os.makedirs("/etc/wireguard")
        os.chmod('/etc/wireguard', 600)
    


    WireguardPrivateKey = executeSystemCommand("wg genkey")
    WireguardPublicKey = executeSystemCommand(f"echo {WireguardPrivateKey} | wg pubkey")
    


    aDict = {"PublicI":MIM, "PublicIIP":MI, "WGInterface":WGI, "WGv4":WG4, "WGv6":WG6, "WGPort":WGP, "DNS1":DNS1, "DNS2":DNS2, "ServerPubKey":WireguardPublicKey,"ServerPrivKey":WireguardPrivateKey}
    jsonFile = open("/etc/wireguard/config.json", "w")
    jsonFile.write(json.dumps(aDict))
    jsonFile.close()



    WGConf=f"""[Interface]
Address = {WG4}/24,{WG6}/64
ListenPort = {WGP}
PrivateKey = {WireguardPrivateKey}
PostUp = iptables -A FORWARD -i {MIM} -o {WGI} -j ACCEPT; iptables -A FORWARD -i {WGI} -j ACCEPT; iptables -t nat -A POSTROUTING -o {MIM} -j MASQUERADE; ip6tables -A FORWARD -i {WGI} -j ACCEPT; ip6tables -t nat -A POSTROUTING -o {MIM} -j MASQUERADE
PostDown = iptables -D FORWARD -i {MIM} -o {WGI} -j ACCEPT; iptables -D FORWARD -i {WGI} -j ACCEPT; iptables -t nat -D POSTROUTING -o {MIM} -j MASQUERADE; ip6tables -D FORWARD -i {WGI} -j ACCEPT; ip6tables -t nat -D POSTROUTING -o {MIM} -j MASQUERADE
"""

    with open(f"/etc/wireguard/{WGI}.conf", "w") as wgconf:
        wgconf.write(WGConf)


    with open("/etc/sysctl.d/wg.conf", "w") as text_file:
        text_file.write("net.ipv4.ip_forward = 1\nnet.ipv6.conf.all.forwarding = 1")



    print("Reloading system components..")
    os.system("sysctl --system")

    print("Starting Wireguard Service..")
    os.system(f"""systemctl start wg-quick@{WGI}
    systemctl enable wg-quick@{WGI}""")



    NewClient()



    





def NewClient():

    with open('/etc/wireguard/config.json') as f:
        wg = json.load(f)

        CLIENT_NAME=""
        print(f"""----------\nEnter the name of your new client:\n""")
        while bool(re.match(utils.Name_Regex, CLIENT_NAME)) != True: 
            CLIENT_NAME=input("> ")

        print(f"New Client: {CLIENT_NAME}")

        wgconf = (open(f"/etc/wireguard/{wg['WGInterface']}.conf", "r")).read()
        ClientCount=len(wgconf.split("[Peer]"))

        IPParts4=wg['WGv4'].split(".")
        IPParts6=wg['WGv6'].split("::")




        ClientPSK=executeSystemCommand("wg genpsk")
        ClientPriv=executeSystemCommand("wg genkey")
        ClientPublic=executeSystemCommand(f"echo {ClientPriv} | wg pubkey")

        print(f"PSK: {ClientPSK}")
        print(f"Priv: {ClientPriv}")
        print(f"Pub: {ClientPublic}")


        if ClientCount+1 > 253:
            print("ERROR: At the moment you can't configure more clients!")
            exit()


        ClientIP4=f"{IPParts4[0]}.{IPParts4[1]}.{IPParts4[2]}.{ClientCount+1}"
        ClientIP6=f"{IPParts6[0]}::{ClientCount+1}"




        # For Wireguard Con:qfguration
        WGConfEntry=f"""

## ---------- Client: {CLIENT_NAME} ---------- ##
[Peer]
PublicKey = {ClientPublic}
PresharedKey = {ClientPSK}
AllowedIPs = {ClientIP4}/32,{ClientIP6}/128"""

        print(WGConfEntry)

        with open(f"/etc/wireguard/{wg['WGInterface']}.conf", "a") as wgconf:
            wgconf.write(WGConfEntry)


        NewWG=f"""[Interface]
PrivateKey = {ClientPriv}
Address = {ClientIP4}/32,{ClientIP6}/128
DNS = {wg['DNS1']},{wg['DNS2']}

[Peer]
PublicKey = {wg['ServerPubKey']}
PresharedKey = {ClientPSK}
Endpoint = {wg['PublicIIP']}:{wg['WGPort']}
AllowedIPs = 0.0.0.0/0,::/0

        """

        with open(f"/root/wireguard-client-{CLIENT_NAME}({wg['WGInterface']})", "w+") as wgconf:
            wgconf.write(NewWG)

        os.system(f'systemctl restart wg-quick@{wg["WGInterface"]}')

        print(executeSystemCommand(f'qrencode -t ansiutf8 -l L <"/root/wireguard-client-{CLIENT_NAME}({wg["WGInterface"]})"'))





def Already():
    RESULT=""
    while bool(re.match("^[1-5]+$", RESULT)) != True:
        print("""
What do you want to do?

1) Add an new User
2) Remove an User (Soon)
3) Add an new Interface (Soon)
4) Check Status of Wireguard (Soon)
5) Uninstall Wireguard (Soon)
    """)
        RESULT = input("> ")

    if(RESULT == str(1)):
        NewClient()



# ----- Script Start ------

def main():

    utils.CC()
    
    print(utils.Welcome_Banner)

    InitCheck()

    if os.path.isfile("/etc/wireguard/config.json"):
        Already()
    else:
        InstallQuestions()

if __name__=='__main__':
    main()

