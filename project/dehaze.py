import cv2
import numpy as np
from flask import Flask, request, send_file, render_template
from io import BytesIO

app = Flask(__name__)

def dark_channel_prior(img, window_size=15):
    min_channel = np.amin(img, axis=2)
    dark_channel = cv2.erode(min_channel, np.ones((window_size, window_size), np.uint8))
    return dark_channel

def estimate_atmospheric_light(img, dark_channel, p=0.001):
    num_pixels = int(p * dark_channel.size)
    dark_vector = dark_channel.ravel()
    img_vector = img.reshape((dark_channel.size, 3))
    indices = np.argpartition(-dark_vector, num_pixels)[:num_pixels]
    atmospheric_light = np.mean(img_vector[indices], axis=0)
    return np.clip(atmospheric_light, 0, 255)  # Enforcing valid range

def transmission_map(img, atmospheric_light, omega=0.85, window_size=15):
    norm_img = img.astype(np.float64) / (atmospheric_light + 1e-5)  # Avoid division by zero
    transmission_raw = 1 - omega * dark_channel_prior(norm_img, window_size)
    return transmission_raw

def refine_transmission_map(img, transmission_map, radius=60, eps=1e-4):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    transmission_map = transmission_map.astype(np.float32)
    refined_map = cv2.ximgproc.guidedFilter(gray, transmission_map, radius, eps)
    return np.clip(refined_map, 0.1, 1)  # Enforcing valid range

def recover_scene_radiance(img, atmospheric_light, transmission_map, t0=0.1):
    img = img.astype(np.float64)
    transmission_map = np.maximum(transmission_map, t0)
    scene_radiance = (img - atmospheric_light) / transmission_map[:, :, np.newaxis] + atmospheric_light
    return np.clip(scene_radiance, 0, 255).astype(np.uint8)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dehaze', methods=['POST'])
def dehaze():
    file = request.files['image']
    img = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_COLOR)

    # Parameters
    window_size = 15
    omega = 0.85
    p = 0.001
    radius = 60  # Adjusted
    eps = 1e-4  # Adjusted
    t0 = 0.1    # Adjusted

    dark_channel = dark_channel_prior(img, window_size)
    atmospheric_light = estimate_atmospheric_light(img, dark_channel, p)
    trans_map = transmission_map(img, atmospheric_light, omega, window_size)
    refined_map = refine_transmission_map(img, trans_map, radius, eps)
    result = recover_scene_radiance(img, atmospheric_light, refined_map, t0)

    # Convert result image to BytesIO object
    _, buffer = cv2.imencode('.png', result)
    io_buffer = BytesIO(buffer)

    return send_file(io_buffer, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)
