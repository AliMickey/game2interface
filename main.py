import netifaces, os, ctypes, sys, subprocess
from scapy.arch.windows import *
from time import sleep
from setupIP import loadIPs, updateIPs

# Get and return secondary interface gateway
def getInterface(interface):
    interfaceGateways = netifaces.gateways()
    interfaceDetails = get_windows_if_list()
    interfaces = []

    # Keep only relevant interfaces
    for interface in interfaceDetails:
        if len(interface['ips']) > 0:
            if not any(n in interface['name'] for n in ['Loopback', 'Local Area Connection']):
                interfaces.append({'name': interface['name'], 'guid': interface['guid'], 'ips': interface['ips']})

    # If only one interface is found (primary only)
    if len(interfaces) <= 1:
        print("\nError: A secondary interface was not detected.")
        sleep(2)
        menu()

    # If there is a secondary interface
    os.system("cls")
    print("\nChoose your secondary interface:\n")
    count = 0
    for interface in interfaces[1:]: # Omit the primary interface
        print(f"{count}) {interface['name']}")
        count += 1
    
    while True:
        # Increase input by 1 to account for excluded primary interface
        chosenInterfaceIndex = int(input("\nPlease make a choice: ")) + 1
        if chosenInterfaceIndex > count:
            print("Invalid input: ")
        else:
            break

    # Get the gateway IP for the selected interface
    for x in interfaceGateways[2]:
        if interfaces[chosenInterfaceIndex]['guid'] == x[1]:
            interfaces[chosenInterfaceIndex]['gateway'] = x[0]
            break   
    
    if interface == "primary":
        return interfaces[0]
    else:
        return interfaces[chosenInterfaceIndex]

# Function to setup all necessary changes
def setup(network):
    ips = loadIPs(network)
    secondaryInterface = getInterface(interface="secondary")

    # Disable ipv6 on the secondary interface
    print("IPv6 being disabled...")
    subprocess.run(["powershell", "-Command", f"Disable-NetAdapterBinding -Name '{secondaryInterface['name']}' -ComponentID ms_tcpip6"])

    # Create a new static route for each ip within each subnet mask
    print("Routes being updated...")
    for subnetMask in ips:
        for ip in ips[subnetMask]:
            os.system(f'cmd /c "route -p ADD {ip} mask {subnetMask} {secondaryInterface["gateway"]}"')
    menu()

# Function to revert all changes made by the app
def reset():
    ips = loadIPs()
    secondaryInterface = getInterface(interface="secondary")
    
    # Enable ipv6 on the secondary interface
    print("IPv6 being enabled...")
    subprocess.run(["powershell", "-Command", f"Enable-NetAdapterBinding -Name '{secondaryInterface['name']}' -ComponentID ms_tcpip6"])
    
    # Delete all static routes
    print("Routes being removed...")
    for block in ips:
        for ip in block:
            os.system(f'cmd /c "route delete {ip}"')

implementedNetworks = {'valve': 'Valve', 'apex': 'Apex Legends', 'riot': 'Riot Games', 'bnet': 'Battle-Net'}
# Main menu for network selection
def menu():
    choice = '0'
    while choice == '0':
        os.system("cls")
        print("Welcome to game2interface. An app to route video game traffic through a secondary stable interface.")
        print("No guarantees are given, continually monitor to ensure that you do not eat up your mobile bandwidth.")
        print("For more info: https://github.com/AliMickey/game2interface\n")

        print("Choose a game network to divert:")
        for alias, network in implementedNetworks.items():
            print(f"Type {alias} for {network}.")

        print("\nType update to fetch the latest IP addresses.")
        print("Type reset to delete all diversions.")

        choice = input("\nPlease make a choice: ")

        if choice in implementedNetworks:
            setup(choice)
        elif choice == "update":
            updateIPs()
            menu()
        elif choice == "reset": 
            reset()
            menu()
        else: menu()

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