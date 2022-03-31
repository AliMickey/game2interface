import json, sys, os

# Get absolute path to resource, works for dev and for PyInstaller
def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

# Function to return IPs
def loadIPs(network=None, region=None):
    with open(resource_path('ips.json'), 'r') as f:
        ips = json.load(f)
        if network == 'valve':
            if region == 'africa' or region == 'afr':
                return ips['valve']['africa']
            elif region == 'asia' or region == 'sea':
                return ips['valve']['asia']
            elif region == 'australia' or region == 'aus':
                return ips['valve']['australia']
            elif region == 'europe' or region == 'eu':
                return ips['valve']['europe']
            elif region == 'north_america' or region == 'na':
                return ips['valve']['north_america']
            elif region == 'south_america' or region == 'sa':
                return ips['valve']['south_america']
            else:
                return ips['valve']
        
        elif network == 'riot':
            return ips['riot']
        
        elif network == "battlenet":
            return ips['battlenet']
        
        else:
            allIPs = []
            for network in ips:
                for region in ips[network]:
                    allIPs.append(ips[network][region])
            return allIPs