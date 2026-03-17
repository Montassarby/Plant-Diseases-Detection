# Plant Diseases Detection  
> Embedded AI system for early plant disease detection using Raspberry Pi 4, ESP32, and ResNet-50.

---

## Overview  
This project aims to design and implement an **embedded intelligent system** capable of detecting plant diseases using **computer vision** and **environmental sensors**.  
The solution combines:
- A **ResNet-50** deep learning model deployed on a **Raspberry Pi 4**.  
- A set of sensors (BMP280, humidity, and light sensors) connected to an **ESP32**.  
- An **OLED screen** that displays both predictions and environmental data in real time.  

The system assists farmers and agronomists in early disease detection — even **without Internet access** — providing a low-cost, portable, and autonomous tool for sustainable agriculture.

---

##  Objectives  
- **Real-time image analysis** of plant leaves using ResNet-50.  
- **Acquisition of environmental data** (temperature, soil moisture, light intensity).  
- **On-device disease prediction** and OLED display output.  
- **Hardware integration** for portability, autonomy, and low power consumption.  

---

##  Methodology  
Two complementary development models were adopted:
- **CRISP-DM** for building and validating the machine learning model.  
- **V-Model** for the embedded hardware–software development cycle.  

---

##  System Architecture  

### Physical Architecture  
- **Tier 1 — Presentation:** OLED display (output interface).  
- **Tier 2 — Control:** ESP32 microcontroller (sensor data collection + UART transmission).  
- **Tier 3 — Processing:** Raspberry Pi 4 (AI inference + data aggregation + visualization).  

### Logical Architecture  
Implemented using an **MVC pattern** and design patterns (**Singleton**, **Observer**) to improve modularity and maintainability.

---

## Hardware Components  

| Component | Function |
|------------|-----------|
| **Raspberry Pi 4** | Runs the AI model and handles the user interface |
| **ESP32** | Collects and transmits sensor data (UART) |
| **BMP280** | Measures temperature and atmospheric pressure |
| **Soil Humidity Sensor** | Measures soil moisture level |
| **BH1750 Light Sensor** | Measures light intensity |
| **Raspberry Pi Camera V2 (IMX219)** | Captures leaf images |
| **OLED Display** | Displays prediction and sensor data |
| **Custom 3D-printed case** | Houses components (modeled in SolidWorks) |

---

## Software Environment  

**Hardware setup:**  
- CPU: Intel Core i5-12400F  
- GPU: NVIDIA RTX 3060 (12 GB VRAM)  
- RAM: 16 GB  
- OS: Windows 11 (for model training)  
- Deployment: Raspberry Pi OS on Raspberry Pi 4  

**Software tools:**  
- **VS Code** – code editor  
- **SolidWorks** – 3D modeling  
- **Arduino IDE / MicroPython** – ESP32 development  
- **Raspberry Pi Imager** – system installation  

---

## Technologies & Libraries  

| Language | Usage |
|-----------|--------|
| **Python 3.x** | Model training & inference |
| **MicroPython** | Embedded ESP32 code |

**Libraries used:**  
- `torch`, `torchvision` – Deep Learning (ResNet-50, fine-tuning)  
- `numpy`, `scikit-learn` – data manipulation & evaluation  
- `matplotlib` – visualization  
- `opencv-python` – image capture & processing  
- `pyserial` – UART communication  
- `os` – system file management  

---

##  Model Development  

### Dataset  
- **PlantVillage Dataset** — 54 315 images of 14 crops and 38 disease classes.  
- Classes balanced between healthy and infected leaves.  

### Preprocessing  
- Image resizing to **224 × 224 px**  
- Normalization & tensor conversion  
- Train/validation split: **80 % / 20 %**  

### Model Training  
- Base model: **ResNet-50 (pretrained on ImageNet)**  
- Optimizer: **Adam**  
- Learning rate: **0.01**  
- Epochs: **40**  
- Loss: **CrossEntropyLoss**  
- Hardware acceleration: **CUDA 12.1 + cuDNN 8.9** on RTX 3060  

### Results  
| Metric | Value |
|--------:|:------|
| **Accuracy** | **99.12 %** |
| **Precision** | **98 %** |

The model was exported as a `.pth` file and later integrated into the Raspberry Pi system for on-device inference.

---

## Deployment  

1. Install **Raspberry Pi OS** using Raspberry Pi Imager.  
2. Enable **SSH** and configure Wi-Fi for remote access.  
3. Create a Python virtual environment and install dependencies:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install torch torchvision opencv-python pyserial
