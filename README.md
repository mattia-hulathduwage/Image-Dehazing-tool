# Dehaze Image Processing App 🌫️

A **web-based application** built using **Flask** that applies the **Dark Channel Prior (DCP)** method to remove haze from images. Users can upload an image, and the app will dehaze it using advanced computer vision techniques.

## Features  
✅ **Image Upload**: Upload an image from your local device to be processed.  
✅ **Dehazing**: Removes haze from the uploaded image using the **Dark Channel Prior** method.  
✅ **Real-time Processing**: The app processes images in real-time and returns the dehazed image.  
✅ **Flask Web Application**: Built using Flask for a simple web interface.

## Technologies Used  
- **Backend**: Flask 🖥️  
- **Computer Vision**: OpenCV for image processing  
- **Image Processing**: Dark Channel Prior (DCP) for dehazing  
- **Frontend**: HTML (rendered with Flask templates)

## How It Works  
1. **Dark Channel Prior**: The algorithm calculates a "dark channel" for the image by finding the minimum value across color channels.
2. **Atmospheric Light Estimation**: Estimates the atmospheric light in the hazy image using the dark channel.
3. **Transmission Map Calculation**: A map is computed that shows the transmission level of light through the haze.
4. **Refinement**: The transmission map is refined using a guided filter.
5. **Scene Radiance Recovery**: The final step involves recovering the scene radiance (clear image) from the hazy image using the transmission map.

## Setup Instructions  
1. **Clone the repository**  
   ```sh
   git clone https://github.com/mattia-hulathduwage/Image-Dehazing-tool.git
   cd dehaze-image-processing
