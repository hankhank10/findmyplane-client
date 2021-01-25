import tkinter as tk
import time

# Create window
window = tk.Tk()
window.title("Find My Plane")
window.resizable(False, False)
window.geometry("400x250")

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
    text="LOADING IDENT",
    height=5,
    font=("Courier", 30)
)

link_label = tk.Label(
    text="https://findmyplane.live/"
)

stats_label = tk.Label(
    text=""
)

server_status_label.pack()
sim_status_label.pack()
ident_label.pack()
link_label.pack()
stats_label.pack()

window.mainloop()

#time.sleep(5)
#label['text'] = 'change the value'
