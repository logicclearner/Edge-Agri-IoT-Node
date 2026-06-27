import tkinter as tk
import serial
import csv
import os
from datetime import datetime
from gpiozero import Button
import pandas as pd
import matplotlib
# Force matplotlib to save silently in the background
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# --- CONFIGURATION & SESSION SETUP --
# Create a unique timestamp for this specific boot/session
session_time = datetime.now().strftime("%Y%m%d_%H%M%S")
CSV_FILE = f'/home/pi/field_data_{session_time}.csv'
SERIAL_PORT = '/dev/ttyACM0' 
BAUD_RATE = 9600

# Physical Button on GPIO 21 (Physical Pin 40, other leg to Ground)
physical_button = Button(21, pull_up=True, bounce_time=0.2)
latest_data = {"Lat": "0.000000", "Lon": "0.000000", "N": "0", "P": "0", "K": "0"}

try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    print("Connected to Arduino on", SERIAL_PORT)
except:
    ser = None
    print("Warning: Arduino not found!")

# --- FUNCTIONS
def update_data():
    if ser and ser.in_waiting > 0:
        try:
            line = ser.readline().decode('utf-8').strip()
            parts = line.split(',')
            if len(parts) >= 5: 
                # Note: Adjust indices if Arduino CSV format includes Date/Time first
                latest_data["Lat"] = parts[-5]
                latest_data["Lon"] = parts[-4]
                latest_data["N"] = parts[-3]
                latest_data["P"] = parts[-2]
                latest_data["K"] = parts[-1]
        except Exception as e:
            pass
    
    now = datetime.now()
    time_label.config(text=f"Time: {now.strftime('%Y-%m-%d %H:%M:%S')}")
    gps_label.config(text=f"Lat: {latest_data['Lat']} Lon: {latest_data['Lon']}")
    npk_label.config(text=f"N: {latest_data['N']} | P: {latest_data['P']} | K: {latest_data['K']}")
    root.after(100, update_data)

def save_to_csv():
    now = datetime.now()
    file_exists = os.path.isfile(CSV_FILE)
    try:
        with open(CSV_FILE, mode='a', newline='') as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(["Date", "Time", "Latitude", "Longitude", "Nitrogen", "Phosphorus", "Potassium"])
            writer.writerow([now.strftime("%Y-%m-%d"), now.strftime("%H:%M:%S"),
                             latest_data["Lat"], latest_data["Lon"], latest_data["N"], latest_data["P"], latest_data["K"]])
        status_label.config(text=f"Saved to {session_time}!", fg="#00ff00")
        root.after(2000, lambda: status_label.config(text=""))
    except Exception as e:
        status_label.config(text="Error Saving!", fg="red")

def generate_maps():
    status_label.config(text="Generating Maps... Wait", fg="#ffaa00")
    root.update()
    try:
        df = pd.read_csv(CSV_FILE)
        df['Latitude'] = df['Latitude'].astype(float)
        df['Longitude'] = df['Longitude'].astype(float)
        
        # Filter out invalid coordinates
        df_clean = df[(df['Latitude'] != 0.0) & (df['Longitude'] != 0.0)].copy()
        df_clean = df_clean.drop_duplicates(subset=['Latitude', 'Longitude'])
        
        if len(df_clean) < 3:
            status_label.config(text="Need 3+ unique GPS spots!", fg="red")
            root.after(3000, lambda: status_label.config(text=""))
            return
        
        nutrients = ['Nitrogen', 'Phosphorus', 'Potassium']
        colors = ['Greens', 'Blues', 'Oranges']
        
        for nut, colormap in zip(nutrients, colors):
            plt.figure(figsize=(8, 6))
            plt.tricontourf(df_clean['Longitude'], df_clean['Latitude'],
                            df_clean[nut].astype(float), levels=15, cmap=colormap)
            plt.scatter(df_clean['Longitude'], df_clean['Latitude'], color='red',
                        edgecolor='black', s=50)
            plt.colorbar(label=f"{nut} (mg/kg)")
            plt.title(f"{nut} Soil Heatmap - Edge Computed")
            plt.xlabel("Longitude")
            plt.ylabel("Latitude")
            
            # Save the map with the session timestamp so they never overwrite old maps!
            plt.savefig(f"/home/pi/{nut}_map_{session_time}.png", dpi=150)
            plt.close()
            
        status_label.config(text="Maps Saved to /home/pi!", fg="#00ff00")
        root.after(4000, lambda: status_label.config(text=""))
    except Exception as e:
        status_label.config(text="Map Error (Check CSV)", fg="red")

physical_button.when_pressed = save_to_csv

# --- UI SETUP
root = tk.Tk()
root.title("Edge Dashboard")
root.geometry("480x320")
root.configure(bg="#121212")

tk.Label(root, text="SOIL & GPS DASHBOARD", font=("Arial", 16, "bold"), bg="#121212", fg="#00ffcc").pack(pady=4)

time_label = tk.Label(root, text="Time: Loading...", font=("Arial", 12), bg="#121212", fg="white")
time_label.pack(pady=2)

gps_label = tk.Label(root, text="Lat: -- Lon: --", font=("Arial", 14), bg="#121212", fg="#55aaff")
gps_label.pack(pady=6)

npk_label = tk.Label(root, text="N: -- | P: -- | K: --", font=("Arial", 18, "bold"), bg="#121212", fg="#ffaa00")
npk_label.pack(pady=6)

btn_frame = tk.Frame(root, bg="#121212")
btn_frame.pack(pady=8)

save_btn = tk.Button(btn_frame, text="SAVE (CSV)", font=("Arial", 12, "bold"), bg="#cc0000", fg="black", command=save_to_csv, width=10)
save_btn.grid(row=0, column=0, padx=10)

map_btn = tk.Button(btn_frame, text="MAKE MAPS", font=("Arial", 12, "bold"), bg="#00ccff", fg="black", command=generate_maps, width=10)
map_btn.grid(row=0, column=1, padx=10)

status_label = tk.Label(root, text="", font=("Arial", 12, "bold"), bg="#121212")
status_label.pack()

update_data()
root.mainloop()
