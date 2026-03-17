# Plant Diseases Detection — Embedded AI System

> Edge AI system for **real-time plant disease detection** using **Raspberry Pi 4, ESP32, and ResNet-50**.

---

#  Overview

This project presents the design and development of an **embedded intelligent system** capable of detecting plant diseases directly on-device using **computer vision and environmental sensors**.

The system combines:

* **ResNet-50 deep learning model** for plant disease classification
* **Raspberry Pi 4** for image processing and AI inference
* **ESP32 microcontroller** for environmental sensor acquisition
* **OLED display** for real-time output

The solution enables **early detection of plant diseases without internet connectivity**, making it suitable for **smart agriculture and edge AI applications**.

---

#  Objectives

* Detect plant diseases from leaf images using **deep learning**
* Monitor **environmental conditions** (temperature, humidity, light)
* Perform **on-device inference** on Raspberry Pi
* Provide a **portable and low-cost agricultural diagnostic system**

---

#  Methodology

Two development approaches were used:

| Model        | Purpose                    |
| ------------ | -------------------------- |
| **CRISP-DM** | Machine learning lifecycle |
| **V-Model**  | Embedded system design     |

---

# 🏗 System Architecture

## Physical Architecture

**Tier 1 — Presentation**

* OLED display showing predictions and sensor data

**Tier 2 — Control**

* ESP32 microcontroller collecting environmental data

**Tier 3 — Processing**

* Raspberry Pi running the deep learning model

---

## Logical Architecture

The software architecture follows an **MVC pattern** with design patterns:

* **Singleton**
* **Observer**

This improves modularity and maintainability of the embedded system.

---

#  Hardware Components

| Component              | Function                                |
| ---------------------- | --------------------------------------- |
| Raspberry Pi 4         | Runs AI inference and system logic      |
| ESP32                  | Collects environmental sensor data      |
| BMP280                 | Temperature and pressure sensor         |
| Soil Moisture Sensor   | Measures soil humidity                  |
| Light Sensor           | Measures light intensity                |
| Raspberry Pi Camera V2 | Captures plant images                   |
| OLED Display           | Displays predictions and sensor data    |
| 3D Printed Case        | Custom enclosure designed in SolidWorks |

---

#  Software Environment

### Training Environment

* CPU: Intel Core i5-12400F
* GPU: NVIDIA RTX 3060 (12GB)
* RAM: 16GB
* OS: Windows 11
* CUDA 12.1 + cuDNN 8.9

### Deployment Environment

* Raspberry Pi 4
* Raspberry Pi OS
* Python 3

---

#  Technologies & Libraries

### Languages

* Python
* MicroPython

### Libraries

* torch
* torchvision
* opencv-python
* numpy
* scikit-learn
* matplotlib
* pyserial
* PIL
* luma.oled

---

#  Dataset

The model was trained using the **PlantVillage dataset**.

Dataset characteristics:

* **54,315 images**
* **14 crop species**
* **38 plant disease classes**

Dataset source:

https://www.kaggle.com/datasets/emmarex/plantdisease

---

#  Model Development

### Preprocessing

* Image resizing: **224 × 224**
* Normalization
* Conversion to tensor

### Training Configuration

| Parameter                | Value                           |
| ------------------------ | ------------------------------- |
| Base Model               | ResNet-50 (pretrained ImageNet) |
| Optimizer                | Adam                            |
| Epochs                   | 40                              |
| Loss                     | CrossEntropyLoss                |
| Train / Validation Split | 80% / 20%                       |

### Results

| Metric    | Score      |
| --------- | ---------- |
| Accuracy  | **99.12%** |
| Precision | **98%**    |

---

#  Project Structure

```
plant-disease-detection/
│
├── esp32/
│   └── esp32.py
│
├── raspberry_pi/
│   └── raspberry.py
│
├── model/
│   └── Resnet50.ipynb
│
├── hardware/
│   └── Conception3D.SLDPRT
│
├── dataset/
│   └── dataset_link.txt
│
└── README.md
```

---

#  Deployment

The trained model is **not included in the repository** because it must be generated from the training notebook.

## Step 1 — Train the model

Open the notebook:

```
model/Resnet50.ipynb
```

Run all cells to train the model using the PlantVillage dataset.

---

## Step 2 — Export the model

After training, export the model to **TorchScript** format for Raspberry Pi inference.

Example:

```python
import torch

scripted_model = torch.jit.script(model)
scripted_model.save("plant_diseases_detection_scripted.pt")
```

Move the generated file to:

```
model/plant_diseases_detection_scripted.pt
```

---

## Step 3 — Setup Raspberry Pi

Install dependencies:

```
pip install torch torchvision opencv-python pyserial pillow luma.oled
```

---

## Step 4 — Run the system

Start the Raspberry Pi script:

```
python raspberry_pi/raspberry.py
```

When the button is pressed:

1. Camera captures a leaf image
2. The AI model predicts the disease
3. Sensor data from ESP32 is combined
4. Results are displayed on the OLED screen

---

#  ESP32 Sensors

The ESP32 reads environmental sensors and sends data to the Raspberry Pi through **UART communication**.

Example transmitted data:

```
T:25.3,P:1012,H:42,L:1800
```

Where:

* **T** = Temperature
* **P** = Pressure
* **H** = Soil humidity
* **L** = Light intensity

---

#  Future Improvements

* Mobile application for monitoring
* Cloud data logging
* Model optimization with **TensorRT / ONNX**
* Real-time field deployment

---

#  Author

Embedded AI project developed for academic purposes in **AI, IoT, and Smart Agriculture**.
