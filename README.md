# Edge Computing System for Precision Agriculture & Solid Waste Segregation

An in-depth, unified edge computing architecture designed for real-time environmental monitoring and sustainable waste management. This project was developed as a Major Project in partial fulfillment of the B.Tech degree in Electronics & Communication Engineering at SRM Institute of Science and Technology.

This repository houses the complete hardware configurations, data acquisition scripts, and edge-processing analytics dashboards required to deploy the system locally without reliance on cloud infrastructure.

---

## 🌍 Project Overview

Traditional environmental monitoring and agricultural testing methods rely heavily on centralized laboratory analysis, which is costly, labor-intensive, and introduces severe latency. 

This project solves this by deploying a **unified edge computing node** that handles two critical sustainable development tasks:
1. **Precision Agriculture (Soil Nutrient Mapping):** Real-time, on-site monitoring of Soil Nitrogen (N), Phosphorus (P), and Potassium (K) levels combined with geographic coordinates.
2. **Solid Waste Segregation:** An integrated module designed to run in tandem on the edge hardware to automate waste classification.

By processing data locally on a Raspberry Pi rather than pushing it to the cloud, this architecture significantly reduces latency, completely eliminates the need for active internet connections in remote areas, and supports SDGs 2 (Zero Hunger), 9 (Industry, Innovation, and Infrastructure), and 12 (Responsible Consumption and Production).

---

## ⚙️ System Architecture

The system is divided into four distinct operational layers:

### 1. Sensing Layer
*   **JXBS-3001 NPK Sensor:** Extracts real-time N, P, and K values (in mg/kg) directly from the soil using the RS485 communication protocol.
*   **NEO-6M GPS Module:** Captures high-precision latitude and longitude coordinates simultaneously with nutrient data.

### 2. Data Acquisition Layer
*   **Arduino Uno:** Acts as the primary microcontroller for polling the sensors. It handles Modbus RTU CRC calculations, parses the GPS NMEA sentences, and formats the synchronized data into a CSV string for serial transmission.

### 3. Edge Computing Layer
*   **Raspberry Pi 4 (4GB):** The core intelligence of the system. It receives the serial data stream, buffers it, and handles all local data storage and computation, eliminating the need for external servers[cite: 1].

### 4. Local Storage & Visualization Layer
*   **Python Interactive Dashboard:** Built with `Tkinter`, this GUI displays live NPK and GPS data on a 3.5" touchscreen[cite: 1].
*   **Hardware Trigger:** An Omron B3F push button allows the user to manually trigger data capture for specific sampling zones[cite: 1].
*   **Spatial Heatmaps:** Utilizes `Pandas` and `Matplotlib` (`tricontourf`) to automatically generate spatial heat contour maps, providing visual gradients of soil nutrient distribution across the field[cite: 1].

---

## 🧰 Hardware Stack & Power System

To ensure complete mobility in remote agricultural zones, the system operates on a custom, portable power architecture[cite: 1]:
*   **Main Battery:** 14.8V 2600mAh rechargeable battery[cite: 1].
*   **Power Regulation:** A DC-DC Buck Converter steps down the voltage to provide a stable 5V line for the Arduino and GPS module, while passing the required 12-24V line to the NPK sensor[cite: 1].

### Pin Configuration (Arduino Data Acquisition)
Based on the `SoftwareSerial` implementation in the data acquisition codebase[cite: 1]:
*   **NPK Sensor (RS485 to TTL):** `RX = Pin 10`, `TX = Pin 11`[cite: 1]
*   **RS485 Control Pins:** `RE = Pin 6`, `DE = Pin 7`[cite: 1]
*   **NEO-6M GPS:** `RX = Pin 8`, `TX = Pin 9`[cite: 1]

---

## 💻 Software Stack & Dependencies

### Microcontroller (C/C++)
*   **IDE:** Arduino IDE[cite: 1]
*   **Libraries:** `SoftwareSerial.h`, `TinyGPS++.h`[cite: 1]

### Edge Node (Python 3)
Ensure the following Python packages are installed on the Raspberry Pi:
```bash
pip install pyserial pandas matplotlib gpiozero

## Authors
* **Dhruv Dhariwal**
