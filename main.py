import netifaces, os, ctypes, sys
from scapy.arch.windows import *
from time import sleep
from setupIP import loadIPs

# Get and return secondary interface gateway
def getInterface(interface):
    interfaceGateways = netifaces.gateways()
    interfaceDetails = get_windows_if_list()
    interfaces = []

    for interface in interfaceDetails:
        if len(interface['ips']) > 0:
            if not any(n in interface['name'] for n in ['Loopback', 'Local Area Connection']):
                interfaces.append({'name': interface['name'], 'guid': interface['guid'], 'ips': interface['ips']})

    for interface in interfaces:
        for x in interfaceGateways[2]:
            if interface['guid'] == x[1]:
                interface['gateway'] = x[0]
                break

    if len(interfaces) >= 2:
        primaryInterface = interfaces[0]
        secondaryInterface = interfaces[1]
    else:
        print("\nError: A secondary interface was not detected.")
        sleep(2)
        menu()

    if interface == "primary":
        return primaryInterface['gateway']
    else:
        return secondaryInterface['gateway']

# Function to create static routes for given network and region
def addRoutes(network, region=None):
    print(f"\nNetwork chosen: {network}")
    if region:
        print(f"Region chosen: {region}")

    ips = loadIPs(network, region)
    secondaryGateway = getInterface(interface="secondary")

    print("Routes updating...")
    for ip in ips:
        os.system(f'cmd /c "route -p ADD {ip} mask 255.255.255.255 {secondaryGateway}"')
    menu()

# Function to remove all created static routes
def removeRoutes():
    ips = loadIPs()
    print("Routes being removed...")
    for block in ips:
        for ip in block:
            os.system(f'cmd /c "route delete {ip}"')
    menu()

# Main menu for network selection
def menu():
    choice = '0'
    while choice == '0':
        os.system("cls")
        print("Welcome to game2interface. An app to route video game traffic through a secondary stable interface.")
        print("No guarantees are given, continually monitor to ensure that you do not eat up your mobile bandwidth.")
        print("For more info: https://github.com/AliMickey/game2interface\n")
        print("A secondary interface MUST be active for this tool to work.\n\n")

        print("Choose a game to divert:")
        print("Type valve for all Valve games.")
        print("Type riot for all Riot games. (Not implemented yet)")
        print("Type bnet for all Battle-Net Games.")
        print("Type reset to delete all diversions. (This may take a few moments)")

        choice = input ("Please make a choice: ")

        if choice == "valve":
            valveRegionMenu()
        elif choice == "riot":
            addRoutes('riot')
        elif choice == "bnet":
            addRoutes('battlenet')
        elif choice == "reset":
            removeRoutes()
        else:
            menu()

# Choose a region for valve network
def valveRegionMenu():
    regions = ["africa (afr)", "asia (sea)", "australia (aus)", "europe (eu)", "north_america (na)", "south_america (sa)"]
    print("\nChoose a region:")
    for region in regions:
        print(region)

    choice = input ("\nPlease make a choice: ")
    
    for region in regions:
        if choice in region:
            addRoutes('valve', choice)      

# Request UAC
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if is_admin():
    menu()
else:
    # Re-run the program with admin rights
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)