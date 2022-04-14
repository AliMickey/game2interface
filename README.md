# Game2Interface
App to route video game traffic through a secondary stable interface. 

## Motivation
Playing video games on a mobile hotspot is often needed as my main internet connection is unstable.
I would normally have to disable my main interface in order to utilise the hotspot. 
This would lead to all traffic (YouTube, downloads, updates) go through the already low data bandwidth hotspot. 

## Usage
1. Launch the app
2. Enter the game network you wish to divert.
3. If asked, enter the specific region within the network.

## Notes
- All internet traffic will use the primary interface (Ethernet/WiFi). Any selections made by you will be diverted through the secondary interface.
- All changes made by this app are revertable by running `reset` in the main menu. (Confirm with running `route print` in cmd)
- No guarantees are given, continually monitor to ensure that you do not eat up your mobile bandwidth.
- A secondary interface MUST be active (connected) when running this tool.
- IPv6 connectivity will be disabled on the secondary interface to ensure no traffic leakage.
- Make sure to confirm that this tool is working by using task manager and viewing interface network usage.

- Source build: `pyinstaller --onefile --add-data "setupIP.py;." --add-data "ips.json;." --name game2interface --icon=icon.ico main.py`
- IP List: `https://pastebin.com/mpZdJ12n`