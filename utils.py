
import readline
import os
def PreInput(prompt, prefill=''):
   readline.set_startup_hook(lambda: readline.insert_text(prefill))
   try:
      return input(prompt) 
   finally:
      readline.set_startup_hook()


def CC():
   os.system("clear")


class CColor:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'




unsupported_virts = ["openvz", "lxz"]


IPv4_Regex="^((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)(\.(?!$)|$)){4}$"
IPv6_Regex="^\s*((([0-9A-Fa-f]{1,4}:){7}([0-9A-Fa-f]{1,4}|:))|(([0-9A-Fa-f]{1,4}:){6}(:[0-9A-Fa-f]{1,4}|((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3})|:))|(([0-9A-Fa-f]{1,4}:){5}(((:[0-9A-Fa-f]{1,4}){1,2})|:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3})|:))|(([0-9A-Fa-f]{1,4}:){4}(((:[0-9A-Fa-f]{1,4}){1,3})|((:[0-9A-Fa-f]{1,4})?:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){3}(((:[0-9A-Fa-f]{1,4}){1,4})|((:[0-9A-Fa-f]{1,4}){0,2}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){2}(((:[0-9A-Fa-f]{1,4}){1,5})|((:[0-9A-Fa-f]{1,4}){0,3}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){1}(((:[0-9A-Fa-f]{1,4}){1,6})|((:[0-9A-Fa-f]{1,4}){0,4}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(:(((:[0-9A-Fa-f]{1,4}){1,7})|((:[0-9A-Fa-f]{1,4}){0,5}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:)))(%.+)?\s*$"
Int_Regex="^[0-9]+$"
Name_Regex="^[a-zA-Z0-9_-]+$"

Welcome_Banner="""\33[32m __      __.__                                             .___
/  \    /  \__|______   ____   ____  __ _______ _______  __| _/
\   \/\/   /  \_  __ \_/ __ \ / ___\|  |  \__  \\_  __ \/ __ | 
 \        /|  ||  | \/\  ___// /_/  >  |  // __ \|  | \/ /_/ | 
  \__/\  / |__||__|    \___  >___  /|____/(____  /__|  \____ | 
       \/                  \/_____/            \/           \/ 
    .___                 __         .__  .__                   
    |   | ____   _______/  |______  |  | |  |   ___________    
    |   |/    \ /  ___/\   __\__  \ |  | |  | _/ __ \_  __ \   
    |   |   |  \\___ \  |  |  / __ \|  |_|  |_\  ___/|  | \/   
    |___|___|  /____  > |__| (____  /____/____/\___  >__|      
             \/     \/            \/               \/        
             
\33[37m  
"""



def MainBanner():
   os.system("clear")
   print(Welcome_Banner)
   print(f"""
{CColor.MAGENTA}+=======================================================================================+{CColor.RESET}
   """)



def GenerateUnboundConfig(Network, Host):
   return f"""server:
    verbosity: 0

    interface: {Host}
    port: 53
    do-ip4: yes
    do-udp: yes
    do-tcp: yes

    access-control: {Network} allow

    do-ip6: yes

    prefer-ip6: no

    harden-glue: yes

    harden-dnssec-stripped: yes

    use-caps-for-id: no

    edns-buffer-size: 1472

    prefetch: yes

    num-threads: 2

    so-rcvbuf: 1m

    private-address: 192.168.0.0/16
    private-address: 169.254.0.0/16
    private-address: 172.16.0.0/12
    private-address: 10.0.0.0/8
    private-address: fd00::/8
    private-address: fe80::/10"""