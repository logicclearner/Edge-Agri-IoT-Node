# Edge Computing System for Precision Agriculture

An edge computing architecture designed for real-time soil nutrient monitoring. This project was developed as a Major Project in partial fulfillment of the B.Tech degree in Electronics & Communication Engineering at SRM Institute of Science and Technology.

This repository houses the complete hardware configurations, data acquisition scripts, and edge-processing analytics dashboards required to deploy the system locally without reliance on cloud infrastructure.

---

## 🌍 Project Overview

Traditional environmental monitoring and agricultural testing methods rely heavily on centralized laboratory analysis, which is costly, labor-intensive, and introduces severe latency. 

This project solves this by deploying an **edge computing node** for **Precision Agriculture (Soil Nutrient Mapping):** Real-time, on-site monitoring of Soil Nitrogen (N), Phosphorus (P), and Potassium (K) levels combined with geographic coordinates.

By processing data locally on a Raspberry Pi rather than pushing it to the cloud, this architecture significantly reduces latency, completely eliminates the need for active internet connections in remote areas, and supports sustainable agricultural practices.

---

## ⚙️ System Architecture

The system is divided into four distinct operational layers:

### 1. Sensing Layer
* **JXBS-3001 NPK Sensor:** Extracts real-time N, P, and K values (in mg/kg) directly from the soil using the RS485 communication protocol.
* **NEO-6M GPS Module:** Captures high-precision latitude and longitude coordinates simultaneously with nutrient data.

### 2. Data Acquisition Layer
* **Arduino Uno:** Acts as the primary microcontroller for polling the sensors. It handles Modbus RTU CRC calculations, parses the GPS NMEA sentences, and formats the synchronized data into a CSV string for serial transmission.

### 3. Edge Computing Layer
* **Raspberry Pi 4 (4GB):** The core intelligence of the system. It receives the serial data stream, buffers it, and handles all local data storage and computation, eliminating the need for external servers.

### 4. Local Storage & Visualization Layer
* **Python Interactive Dashboard:** Built with `Tkinter`, this GUI displays live NPK and GPS data on a 3.5" touchscreen.
* **Hardware Trigger:** An Omron B3F push button allows the user to manually trigger data capture for specific sampling zones.
* **Spatial Heatmaps:** Utilizes `Pandas` and `Matplotlib` (`tricontourf`) to automatically generate spatial heat contour maps, providing visual gradients of soil nutrient distribution across the field.

---

## 🔌 Hardware Wiring & Connection Design

This section details the pin-to-pin connections for the Data Acquisition Layer (Arduino) and the Edge Computing Layer (Raspberry Pi), as well as the power distribution network.

### 1. Power Distribution Network
The system is designed for remote mobility, powered by a single high-capacity battery with regulated step-downs.

* **Main Power Source:** 14.8V 2600mAh Li-ion Battery
* **NPK Sensor (JXBS-3001):** Receives 12-24V directly from the unregulated battery line.
* **DC-DC Buck Converter:** Steps down the 14.8V source to a stable 5V.
* **5V Regulated Line:** Powers the Arduino Uno and the NEO-6M GPS Module.
* **Raspberry Pi 4:** Powered independently via a 5V Power Bank (or adapted from the buck converter).

### 2. Arduino Uno (Data Acquisition Node)
The Arduino acts as the central polling hub. It uses `SoftwareSerial` to communicate with both the NPK sensor (via an RS485-to-TTL module) and the GPS module.

| Arduino Pin | Connected Component | Function / Details |
| :--- | :--- | :--- |
| **Pin 10** | RS485 Module (RO) | NPK Sensor SoftwareSerial RX |
| **Pin 11** | RS485 Module (DI) | NPK Sensor SoftwareSerial TX |
| **Pin 6** | RS485 Module (RE) | Receiver Enable (Active Low) |
| **Pin 7** | RS485 Module (DE) | Driver Enable (Active High) |
| **Pin 8** | NEO-6M GPS (TX) | GPS SoftwareSerial RX |
| **Pin 9** | NEO-6M GPS (RX) | GPS SoftwareSerial TX |
| **5V / GND**| RS485 & GPS Modules | Shared logic power ground |

*Note: The RS485 module's A and B terminals connect directly to the JXBS-3001 sensor's A (Yellow) and B (Blue) wires.*

### 3. Raspberry Pi 4 (Edge Processing Node)
The Raspberry Pi handles local computation, CSV logging, and GUI rendering. 

| Raspberry Pi Port/Pin | Connected Component | Function / Details |
| :--- | :--- | :--- |
| **USB Port** | Arduino Uno | Serial data transfer (Mapped to `/dev/ttyACM0`) |
| **GPIO 21 (Pin 40)** | Omron B3F Push Button | Hardware interrupt for manual data capture |
| **GND (Pin 39)** | Omron B3F Push Button | Ground for the physical trigger |
| **Display Header/I2C**| 3.5" Touchscreen | Renders the Tkinter GUI dashboard |

---

## 💻 Software Stack & Dependencies

### Microcontroller (C/C++)
* **IDE:** Arduino IDE
* **Libraries:** `SoftwareSerial.h`, `TinyGPS++.h`

### Edge Node (Python 3)
Ensure the following Python packages are installed on the Raspberry Pi:
```bash
pip install pyserial pandas matplotlib gpiozero
```
## 👨‍🔬 Author

**Dhruv Dhariwal** 

