import requests
import time
from SimConnect import *
import tkinter as tk
import webbrowser
from tkinter import messagebox
import sys

client_version = 2000


def browser_callback(url):
    webbrowser.open_new(url)


def request_new_plane_instance ():

    title = aq.get("TITLE")
    atc_id = aq.get("ATC_ID")

    if title == None or atc_id == None:
        return "error"

    data_to_send = {
        'title': title.decode("utf-8"),
        'atc_id': atc_id.decode("utf-8"),
        'client_version': client_version
    }

    try:
        new_plane_request = requests.post(website_address + "/api/create_new_plane", json=data_to_send)
    except requests.exceptions.RequestException as e:
        return "error"

    if new_plane_request.status_code != 200:
        return "error"

    received_data = new_plane_request.json()

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
        on_ground = aq.get("SIM_ON_GROUND")
        seatbelt_sign = aq.get("CABIN_SEATBELTS_ALERT_SWITCH")
        no_smoking_sign = aq.get("CABIN_NO_SMOKING_ALERT_SWITCH")
        gear_handle_position = aq.get("GEAR_HANDLE_POSITION")
        canopy_open = aq.get("CANOPY_OPEN")
        parking_brake = aq.get("BRAKE_PARKING_INDICATOR")
    except Exception as e:
        sim_errors_logged += 1
        error_this_time = True
        print (str(e))

    try:
        title = title.decode('ascii')
        atc_id = atc_id.decode('ascii')
    except Exception as e:
        sim_errors_logged += 1
        error_this_time = True
        print (str(e))

    if not error_this_time:
        data_to_send = {
            'ident_public_key': ident_public_key,
            'ident_private_key': ident_private_key,
            'current_latitude': current_latitude,
            'current_longitude': current_longitude,
            'current_compass': current_compass,
            'current_altitude': current_altitude,
            'title': title,
            'atc_id': atc_id,
            'on_ground': on_ground,
            'seatbelt_sign': seatbelt_sign,
            'no_smoking_sign': no_smoking_sign,
            'gear_handle_position': gear_handle_position,
            'door_status': canopy_open,
            'parking_brake': parking_brake,
            'client_version': client_version
        }

        try:
            r = requests.post(website_address + "/api/update_plane_location", json=data_to_send)
        except:
            server_errors_logged = server_errors_logged + 1

        datapoints_sent += 1

    stats_label['text'] = str(datapoints_sent) + " datapoints: " + str(server_errors_logged) + " server errors and " + str(sim_errors_logged) + " sim errors"

    return "ok"


def on_closing():
    global user_has_quit

    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        user_has_quit = True


def kill_the_window():
    window.destroy()
    sys.exit()

###############
# SET UP GUI
###############

# Create window
window = tk.Tk()
window.title("Find My Plane")
window.resizable(False, False)
window.geometry("400x270")
window.protocol("WM_DELETE_WINDOW", on_closing)

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

user_has_quit = False


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

    if user_has_quit:
        kill_the_window()
    else:
        sim_status_label['text'] = 'Waiting to connect to sim: ' + str(connection_attempts) + ' attempts'
        time.sleep(1)
        window.update()

sim_status_label['text'] = 'Connected to sim'
sim_status_label['fg'] = 'green'

###############
# CONNECT TO SERVER
###############

received_plane_details = "error"
while received_plane_details == "error":
    if user_has_quit:
        kill_the_window()
    else:
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

while not user_has_quit:
    update_location()
    window.update_idletasks()
    window.update()
    time.sleep(delay_between_updates)
