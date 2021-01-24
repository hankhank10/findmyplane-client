import requests
import time
from SimConnect import *
import tkinter as tk
import webbrowser


def browser_callback(url):
    webbrowser.open_new(url)


def request_new_plane_instance ():

    title = aq.get("TITLE")
    atc_id = aq.get("ATC_ID")

    if title == None or atc_id == None:
        return "error"

    data_to_send = {
        'title': title.decode("utf-8"),
        'atc_id': atc_id.decode("utf-8")
    }

    try:
        new_plane_request = requests.post(website_address + "/api/create_new_plane", json=data_to_send)
    except requests.exceptions.RequestException as e:
        return "error"

    if new_plane_request.status_code != 200:
        return "error"

    received_data = (new_plane_request.json())

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
        current_altitude = aq.get("PLANE_ALTITUDE")
        current_compass = aq.get("MAGNETIC_COMPASS")
        title = aq.get("TITLE")
        atc_id = aq.get("ATC_ID")
    except:
        sim_errors_logged += 1
        error_this_time = True

    try:
        title = title.decode('ascii')
        atc_id = atc_id.decode('ascii')
    except:
        sim_errors_logged += 1
        error_this_time = True

    if not error_this_time:
        data_to_send = {
            'ident_public_key': ident_public_key,
            'ident_private_key': ident_private_key,
            'current_latitude': current_latitude,
            'current_longitude': current_longitude,
            'current_compass': current_compass,
            'current_altitude': current_altitude,
            'title': title,
            'atc_id': atc_id
        }

        r = requests.post(website_address + "/api/update_plane_location", json=data_to_send)

        datapoints_sent += 1

    stats_label['text'] = str(datapoints_sent) + " datapoints: " + str(server_errors_logged) + " server errors and " + str(sim_errors_logged) + " sim errors"

    return "ok"


###############
# SET UP GUI
###############

# Create window
window = tk.Tk()
window.title("Find My Plane")
window.resizable(False, False)
window.geometry("400x270")

# Create labels
server_status_label = tk.Label(
    text="Not connected to server",
    fg="red"
)

sim_status_label = tk.Label (
    text="Not connected to sim",
    fg="red"
)

ident_label = tk.Label(
    text="LOADING",
    height=2,
    font=("Courier", 60)
)

link_label = tk.Label(
    text="https://findmyplane.live/",
)

stats_label = tk.Label(
    text=""
)

sim_status_label.pack()
server_status_label.pack()
ident_label.pack()
link_label.pack()
stats_label.pack()

window.update()


###############
# SET SETTINGS
###############

website_address = "https://findmyplane.live"
delay_after_failed_new_plane_request = 3
delay_between_updates = 1
verbose = False
version = "Alpha 0.4"

datapoints_sent = 0
server_errors_logged = 0
sim_errors_logged = 0


###############
# CONNECT TO SIM
###############

sim_status_label['text'] = 'Connecting to sim...'
sim_status_label['fg'] = "red"

connected_to_sim = False
connection_attempts = 0
while not connected_to_sim:
    connected_to_sim = True
    try:
        sm = SimConnect()
        aq = AircraftRequests(sm, _time=10)
    except:
        connected_to_sim = False
    connection_attempts = connection_attempts + 1

    sim_status_label['text'] = 'Trying to connect to sim: ' + str(connection_attempts) + ' attempts'
    time.sleep(1)
    window.update()

sim_status_label['text'] = 'Connected to sim'
sim_status_label['fg'] = 'green'

###############
# CONNECT TO SERVER
###############

received_plane_details = "error"
while received_plane_details == "error":
    received_plane_details = request_new_plane_instance()
    if received_plane_details == "error":
        server_status_label['text'] = 'Trying to connect to server'
        time.sleep(1)
        window.update()
        time.sleep(delay_after_failed_new_plane_request)

ident_public_key = received_plane_details['ident_public_key']
ident_private_key = received_plane_details['ident_private_key']

server_status_label['text'] = 'Connected to server'
server_status_label['fg'] = 'green'

ident_label['text'] = ident_public_key

link_label['text'] = "https://findmyplane.live/view/" + ident_public_key
link_label['cursor'] = "hand2"
link_label.bind("<Button-1>", lambda e: browser_callback("https://findmyplane.live/view/" + ident_public_key))


###############
# MAIN LOOP
###############

while True:
    update_location()
    window.update_idletasks()
    window.update()
    time.sleep(delay_between_updates)