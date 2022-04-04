import json, sys, os, requests

# Get absolute path to resource, works for dev and for PyInstaller
def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

# Function to return ips
def loadIPs(network=None):
    with open(resource_path('ips.json'), 'r') as f:
        ips = json.load(f)

    if network == 'valve': return ips['valve']
    elif network == 'bnet': return ips['battlenet']
    else: 
        allIPs = []
        for network in ips:
            for subnetMask in ips[network]:
                allIPs.append(ips[network][subnetMask])
        return allIPs

def updateIPs():
    url = 'https://raw.githubusercontent.com/AliMickey/game2interface/main/ips.json'
    ipFile = requests.get(url)
    with open(resource_path('ips.json'), 'wb') as f:
        f.write(ipFile.content)