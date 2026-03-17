import torch
import cv2
import time
import RPi.GPIO as GPIO
import serial
from luma.core.interface.serial import i2c
from luma.oled.device import sh1106  
from luma.core.render import canvas
from PIL import ImageFont
from torchvision import transforms
from PIL import Image

# Chargement du modèle TorchScript 
model = torch.jit.load("plant_dieseases_detection_scripted.pt")
model.eval()

# Initialisation du port série (pour récupérer les données des capteurs) 
ESP32_PORT = "/dev/serial0"
BAUD_RATE = 115200
ser = serial.Serial(ESP32_PORT, BAUD_RATE, timeout=1)

# GPIO bouton
BUTTON_PIN = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Config OLED 
oled_serial = i2c(port=1, address=0x3C)
oled = sh1106(oled_serial)
font = ImageFont.load_default()

def display_oled(lines):
    with canvas(oled) as draw:
        for i, line in enumerate(lines):
            draw.text((0, i * 10), line, font=font, fill=255)

def capture_image():
    cam = cv2.VideoCapture(0)
    time.sleep(1)
    ret, frame = cam.read()
    if ret:
        path = "/tmp/plant.jpg"
        cv2.imwrite(path, frame)
        cam.release()
        return path
    else:
        cam.release()
        raise RuntimeError("Échec capture image")

def get_prediction(img_path):
    
    
    # Prétraitement de l'image pour le modèle 
    image = cv2.imread(img_path)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image_pil = Image.fromarray(image_rgb)

    preprocess = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406],
                             std=[0.229, 0.224, 0.225])
    ])
    input_tensor = preprocess(image_pil).unsqueeze(0) 


    # Faire la prédiction 
    with torch.no_grad():
        output = model(input_tensor)
        predicted_index = torch.argmax(output, dim=1).item()

    # Classes : 38 du dataset plant village 
    classes = [
        "Apple___Apple_scab", "Apple___Black_rot", "Apple___Cedar_apple_rust",
        "Apple___healthy", "Blueberry___healthy", "Cherry___healthy",
        "Cherry___Powdery_mildew", "Corn___healthy", "Corn___Northern_Leaf_Blight",
        "Grape___healthy", "Grape___Leaf_blight", "Peach___healthy", "Pepper___healthy",
        "Potato___healthy", "Tomato___healthy",
        "Tomato___Bacterial_spot", "Tomato___Early_blight", "Tomato___Late_blight",
        "Tomato___Leaf_Mold", "Tomato___Septoria_leaf_spot", "Tomato___Spider_mites_Two-spotted_spider_mite",
        "Tomato___Target_Spot", "Tomato___Tomato_mosaic_virus", "Tomato___Tomato_Yellow_Leaf_Curl_Virus",
        "Strawberry___healthy", "Strawberry___Leaf_scorch", "Peach___Bacterial_spot",
        "Peach___healthy", "Grape___Esca_(Black_Measles)", "Apple___Apple_scab"
    ]
    predicted_class = classes[predicted_index]
    return predicted_class

def main():
    latest_data = ["En attente..."]

    try:
        while True:
            # Récupérer les données de l'ESP32 via UART
            if ser.in_waiting:
                line = ser.readline().decode().strip()
                if line.startswith("T:"):
                    latest_data = [x.replace(":", ": ") for x in line.split(",")]

            # Bouton pressé, capture image et prédiction
            if GPIO.input(BUTTON_PIN) == GPIO.LOW:
                print("🔘 Bouton pressé : capture image + prédiction")
                display_oled(["Traitement..."])

                img_path = capture_image()

                plant_condition = get_prediction(img_path)

                # Afficher les données sur l'OLED (données capteurs + prédiction)
                display_oled(latest_data + ["Plante : " + plant_condition])
                time.sleep(2)

            time.sleep(0.1)

    except KeyboardInterrupt:
        print("Arrêt par Ctrl+C")
    finally:
        GPIO.cleanup()
        ser.close()

