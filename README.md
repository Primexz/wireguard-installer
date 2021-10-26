# XGuard (Wireguard Server Installer)
![visitor badge](https://visitor-badge.glitch.me/badge?page_id=Primexz.wireguard-installer)

**This Python script should make the installation of a [Wireguard VPN](https://www.wireguard.com/) server as easy as possible.**

Wireguard is a modern VPN protocol.
To ensure the security of the traffic, Wireguard uses the latest cryptographic methods.
Wireguard offers the best performance compared to OpenVPN or IPSec.

To ensure your security / privacy all traffic from the clients is routed through the server. This is done via the so-called NAT. IPv4, but also IPv6 packets are routed via the Wireguard server.


## Requirements (Supported OS's)
- Ubuntu >= 16.04
- Debian >= 10
- CentOS
- Fedora
- Arch Linux

## Quick Start
Download the Python script and run the script.
The script will ask you important questions about the installation.
```bash
git clone https://github.com/Primexz/wireguard-install.git
cd wireguard-install
python3 xguard.py
```
The script will now install all necessary packages for Wireguard. Also already needed interfaces and clients will be configured.

# ToDo's
- Code Optimization
- More Client Options
  - Remove Clients
- Interface Managment
  - Add new Interfaces
  - Remove Interfaces
- Tunnel Monitoring
- Better DNS Resolver Options
  - Custom Unbound Installer
  - Premade DNS Server Selections
 


