# IT Preparation


## Contents

* [Definitions](#def)
* [Job Terms](#term)

<br/><a name="def"></a>
## Definitions
* 802.1X
  - Enhance security of WLAN by IEEE, provides authentication frame work, allows users to be authenticated by a central authority. wireless.
* Authenticated DHCP
  - First network access control, authenticating user id/password be for delivering a DHCP.
* Backbone
   - Primary connectivity mechanism of a hierarchical distribution system. All systems that have connectivity to the backbone are assured of connectivity to each other. 
* Blacklisting
  - An access control system that denies entry to specific users, programs, or net work addresses
* Berkeley Internet Name Domain (BIND)
  - The most commonly used DNS service of the internet
* Broadcasting
  - A packet that is received by all stations in the domain
* Cloud Computing
  - The logical computational resources (data, software, hardware), accessible via a computer network. e.g. Gmail
* Command-line interface (CLI)
  - It is a mechanism for interacting with an operating system. It contrasts with a graphical user interface (GUI), or menus on a text user interface (TUI). Many companies use this mechanism to communicate with their systems.
* Cyclic Redundant Check (CRC)
  - A mathematical calculation on a frame work or cell that is used for error detection. If two CRCs don't match, there is an error.
* DDI
  - a unified service or solution that integrate DNS, DHCP, and IPAM (IP Address Management) into one.
* Dynamic Host Configuration Protocol
  - Assigning IP address to device
* Domain Name System
  - the system of domain names. eg. google.com (no www) godaddy.com
* Frame
  - A unit of data transmission in layer two, containing a packet to layer three
* File Transfer Protocol (FTP)
  - the protocol to transfer files from one host to another. eg. cyberduck (assure the security of transfer). Now people use FTP. 
* Hypertext Transfer Protocol (HTTP)
  - Protocol that supports request-response from a server. eg. a browser sends hyper text "www.google.com" to google.com through HTTP, then google.com returns a HTML to our browser
* Hop
  - Each time a packet is forwarded, it undergoes a "hop". (traceroute www.google.com)
* IP Address Management (IPAM)
  - The administration of DNC and DHCP. It means Planing, tracking, and managing the Internet Protocol space used in a network. eg. DNS knowing the IP address taken via DHCP, and updating itself.
* Local Area Network (LAN)
  - Its a Network that connects computers and devices in a limited geographical area. oppose with WANs (Wide Area Network). eg. home and school. Smaller area, faster speed, no need for telecommunication line.
* deep packet inspection
  - routers looking inside the data packet other than just read the ip address, take very slow

<br/><a name="terms"></a>
## Job Terms

### Hub, Switch and Router
* Hub
  - connects all the network devices together
  - multiple ports
  - not intelligent, do not know where data going to be sent
  - data is copied to all its ports -- broadcasting
* Switch
  - like a hub, accepts ethernet connections from network devices
  - it is intelligent, knows the physical address(MAC address) in switch table. 
  - when a data is sent, it is directed to to intended port
  - reduce unnecessary traffic
* Hub and switch are not capable of exchanging data outside its own network, because to be able to reach outside network a device need to be able to read IP addresses
* Router
  - A router routes data from one network to another based on its IP address
  - The gateway of a network
* Hub and switches are used create networks while routers are used to connect networks

## Firewall
* scans each little packet of data
* physical(routers) or software
* can me exceptions by users

## Malware
* Virus are a little piece of code, that can copy itself to other programs when triggered. corrupt datas. Often attached to an excutable file. 
* Malware are software crashing systems, stealing important information. 
* Trojans are harmful software that can steal information, user are usually lead to open the software.
* Ransomware host pc hostage, threatening to destroy data
* Spyware secretly gathers private information such as passwords
* Worms replicate themselves and attack other devices in the network, slowing down traffic and 
* Malware today is an conclusion of all above and more. 

## Intrusion Detection Prevention (IDP)

### Intrusion Detection System (IDS)
* connect to one of the port at a switch
* IDS determine whether the traffic that is going to the web service is dangerous. eg. compare the signatures, anomalies with in quantity and types. 
* It does not stop the attack from happening. it simply alerts the attack

### Intrusion Prevention System (IPS)
* plug Between the firewall and switch.
* can be virtual or physical
* prevent attack from the begin, protect the computer or server

### Hosted Intrusion Detection/Prevention System (HIDS)
* a IDS/IPS system sometime cost money, if we want to just protect one server, we can run prevent system as an software in tha server
* We can install it into many devices in our networl. eg. routers, firewalls(eg. UTM(Unified Threat Management):Palo Alto, checkpoint)

## Domain Name System(DNS)
* resolves domain names to IP addresses
* domain name typed in **> DNS server search through its database to find its matching IP address **> DNS will resolve the domain name into IP addresses
* works like a phone book

### Detailed Steps:
* type in the Domain Name in web browser
* if the computer can't find its IP address in its cache memory, it will send the query to the Resolver server(basically your ISP)
* Resolver will check its own cache memory, if not, it will send the query to Root server, the top or the root of the DNS hierarchy, 13 sets of root servers around the world, operated by 12 organizations. each set has its own IP address
* The root server will direct the resolver the Top Level Domain server (TLD), for the .com, .net, .org(top level domains) domain. 
* TLD will direct the resolver to the Authoritative Name Server(ANS), and the resolver will ask the ANS for the IP address
* ANS is responsible for knowing everything including the IP address of the domain
* ANS will respond with IP address
* the resolver will tell the computer the IP address
* the resolver will store the IP Address in its cache memory

## Network Topology
* network topology is a layout of how a network communicates with different devices
* wired and wireless

### Wired Topologies

#### Star
* all devices connected to one hub or switch
* pro: one devices failed to connect will not affect other devices
* con: if the central hub or switch failed, it will affect every all devices on that point. single point failure

#### Ring
* connected in a circle, every computer has two neighbors, every packet is sent through the ring
* rarely used today
* easy to install and fix
* one point failure

#### Bus
* each device is connected to the back bone
* the back bone is a coaxial cable, connected to the computers using BNC connector(T connectors) 
* pro: cheap and easy to implement
* con: needs terminators at both end of back bone, if not there will be signal reflection, causing data flow disrupted

#### Mesh
* each computer is connected to each other
* con: high redundancy level, rare failure
* pro: expensive
* rarely used on LAN, mainly used on WAN(like internet)

### Wireless Topologies

#### Infrastructure
* a wireless port connected to one of switch or hub like a star topology

## Next-Gen Firewalls (NGFW)
* similarities
  - static packet filtering
  - Stateful inspection or dynamic packet filtering, which checks every connection on every interface of a firewall for validity
  - Network address translation for re-mapping the IP addresses included in packet headers (NAT)
  - Port address translation that facilitates the mapping of multiple devices on a LAN to a single IP address (PAT)
  - Virtual private network (VPN) support, which maintains the same safety and security features of a private network over the portion of a connection that traverses the internet or other public network
* differences
  - block to add application-level inspectioin
  - IPS
  - bringing intelligence from outside the firewall

## Secure Shell SSH
* communication Protocol(like http, https, ftp, etc)
* do just about anything on the remote computer
* traffic is encrypted
* used mostly in the terminal/command line
* SSH is the client, SSHD is the server (Open SSH Daemon), the server must have sshd installed and running
* **generating keys**: 
  - ssh-keygen
  - ~/.ssh/id_rsa (private key)
  - ~/.ssh/id_rsa.pub (public key)
  - public key goes into server "authorized_keys" file
* in windows: putty in older versions of windows, git bash & other terminal programs include the ssh command & other Unix tools
