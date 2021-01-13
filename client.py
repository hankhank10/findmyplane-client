import requests
import time
from SimConnect import *


def print_art():
    print()
    print(" ______ _           _ __  __       _____  _                    _ _           ")
    print("|  ____(_)         | |  \/  |     |  __ \| |                  | (_)          ")
    print("| |__   _ _ __   __| | \  / |_   _| |__) | | __ _ _ __   ___  | |___   _____ ")
    print("|  __| | | '_ \ / _` | |\/| | | | |  ___/| |/ _` | '_ \ / _ \ | | \ \ / / _ \ ")
    print("| |    | | | | | (_| | |  | | |_| | |    | | (_| | | | |  __/_| | |\ V /  __/")
    print("|_|    |_|_| |_|\__,_|_|  |_|\__, |_|    |_|\__,_|_| |_|\___(_)_|_| \_/ \___|")
    print("                              __/ |                                          ")
    print("                             |___/                                           ")
    print()


def print_settings():
    print ("# SETTINGS:")
    print ("Server address is", website_address)
    print ("Delay after failed new plane request is", str(delay_after_failed_new_plane_request), "seconds")
    print ("Delay between updates is", str(delay_between_updates), "seconds")
    print ()


def request_new_plane_instance ():
    print ("Attempting to connecting to server to request new plane instance...")

    print (aq.get("ATC_MODEL"))
    print (aq.get("ATC_ID"))
    print (aq.get("ATC_AIRLINE"))
    print (aq.get("ATC_FLIGHT_NUMBER"))

    try:
        new_plane_request = requests.get(website_address + "/api/create_new_plane")
    except requests.exceptions.RequestException as e:
        print ("... connection failed")
        return "error"

    if new_plane_request.status_code == 200:
        print("Connected to server")
    else:
        print ("... error code received from server")
        return "error"

    received_data = (new_plane_request.json())

    print ("Public key: ", received_data['ident_public_key'])
    if verbose: print ("Received private key", received_data['ident_private_key'])
    print ()

    return received_data


def update_location():

    error_this_time = False
    global datapoints_sent
    global server_errors_logged
    global sim_errors_logged

    # Get data from sim
    try:
        current_latitude = aq.get("PLANE_LATITUDE")
        current_longitude = aq.get("PLANE_LONGITUDE")
        current_altitude = aq.get("ALTITUDE")
        current_compass = aq.get("MAGNETIC_COMPASS")
    except:
        if verbose: print ("Error getting sim data")
        sim_errors_logged += 1
        error_this_time = True

    if not error_this_time:
        data_to_send = {
            'ident_public_key': ident_public_key,
            'ident_private_key': ident_private_key,
            'current_latitude': current_latitude,
            'current_longitude': current_longitude,
            'current_compass': current_compass,
            'current_altitude': current_altitude
        }

        if verbose: print ("Sending ", data_to_send)
        
        try:
            r = requests.post(website_address+"/api/update_plane_location", json=data_to_send)
        except:
            if verbose: print ("Error sending data")
            server_errors_logged += 1

        if r.status_code != 200:
            server_errors_logged += 1

        datapoints_sent += 1

    if not verbose: print (str(datapoints_sent) + " datapoints sent of which " + str(server_errors_logged) + " generated server errors and " + str(sim_errors_logged) + " sim errors", end='\r')

    return "ok"


# Settings
website_address = "https://findmyplane.live"
delay_after_failed_new_plane_request = 3
delay_between_updates = 1
test_mode = False  #testing only
verbose = False
version = "Alpha 0.2"

datapoints_sent = 0
server_errors_logged = 0
sim_errors_logged = 0

print_art()
print ("Windows client")
print ("Version", version)
print ()
if verbose: print_settings()

# Connect to sim here
print ("# CONNECTING TO SIMULATOR")
print ("Attempting to connect to MSFS 2020...")
try:
    sm = SimConnect()
    aq = AircraftRequests(sm, _time=10)
except:
    print ("... no sim found")
    input ("Press a key to exit...")
    exit()

print ("... connected to MSFS 2020")
print ()

# Request new plane instance from the server
if test_mode:
    print("# CONNECTING TO SERVER IN TEST MODE")
    ident_public_key = "QDSDX"
    ident_private_key = "LfN_uXQMtJCAThKY5ZkfJn_V8Dw"
else:
    print("# CONNECTING TO SERVER")
    received_plane_details = "error"
    while received_plane_details == "error":
        received_plane_details = request_new_plane_instance()
        if received_plane_details == "error": time.sleep(delay_after_failed_new_plane_request)

    ident_public_key = received_plane_details['ident_public_key']
    ident_private_key = received_plane_details['ident_private_key']

print ("Connected to server at", website_address)
print ("Find your plane at:", website_address + "/view/" + ident_public_key)
print ("Press CTRL-C to exit")
print ()

# Report the info to the server
run_forever = True
try:
    while run_forever:
        update_location()
        time.sleep(delay_between_updates)
except KeyboardInterrupt:
    quit()


