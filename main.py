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
        return primaryInterface
    else:
        return secondaryInterface

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
        print("valve for all Valve games.")
        print("riot for all Riot games. (Not implemented yet)")
        print("bnet for all Battle-Net Games.")
        print("update to fetch the latest IP addresses.")
        print("Type reset to delete all diversions.")

        choice = input ("Please make a choice: ")

        if choice == "valve": setup('valve')
        elif choice == "riot": setup('riot')
        elif choice == "bnet": setup('battlenet')
        elif choice == "update": updateIPs()
        elif choice == "reset": reset()
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