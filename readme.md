# FindMyPlane.Live client

This is the client software for [findmyplane.live](https://findmyplane.live), a simple, free, no-nonsense flight map for Microsoft Flight Simulator 2020.

This is what you need to download and run on the computer running the simulator.

## Installation (easy version)

Download the Windows installer:

1. Download from https://findmyplane.live/download/findmyplane-setup.exe or from the releases section on github

2. Double click to install

## Usage (easy version)

1. Load Microsoft Flight Simulator 2020

2. Run *findmyplane-client.exe* from the findmyplane-client directory in Program Files (it will also be in your start menu)

3. Once the client has connected to your simulator and the server it will provide you with a link and five digit ident code such as ABCDE

4. Copy and paste this link to a browser OR

5. Visit https://findmyplane.live and enter the code

6. Your plane location will be displayed

## Supported devices

Microsoft Flight Simulator 2020 only runs on Windows. The client should run on the same Windows computer that your simulator is running on.

You can view the map on most browsers or devices. This doesn't need to be on the same computer or network as the simulator.

Supported devices:
- PC
- Mac
- Linux
- Chromebook
- iOS
- Android

Supported browsers:
- Chrome (Desktop and mobile)
- Firefox (Desktop and mobile)
- Safari (Desktop and mobile)

Unsupported browsers:
- Internet Explorer
- Edge

## Support

If you are stuck then please raise an issue through [github issues](https://github.com/hankhank10/findmyplane-client/issues).

## Advanced installation and usage

If you don't want to use the installer you can just download the executable from [here](https://findmyplane.live/download/findmyplane-client.exe) or GitHub releases. It can run from wherever you want, doesn't need to be in the MSFS folder or anywhere else specific.

The source code is also provided and is open source. You can download findmyplane-client.py and run through your Python 3 interpreter.

Required pip libraries:
- [requests](https://pypi.org/project/requests/)
- [SimConnect](https://pypi.org/project/SimConnect/)

The server is also open source and on github as [hankhank10/findmyplane-server](https://github.com/hankhank10/findmyplane-server). Pull requests on both repos welcome.

## Buy me a beer

Find My Plane is free to use and *almost* free to run. If you want to support the running costs then you can [buy me a beer](https://www.buymeacoffee.com/hankhank10). Everybody likes beer.
