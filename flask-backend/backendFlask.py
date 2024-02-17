from flask import Flask, request, jsonify
from flask_cors import CORS
import cv2
import numpy as np
from sklearn.cluster import KMeans
import colorsys

app = Flask(__name__)
CORS(app)  # This is crucial for cross-origin requests from your React app

def find_predominant_color(image):
    h, w, _ = image.shape
    center_x, center_y = w // 2, h // 2
    size = min(w, h) // 8
    center_region = image[center_y-size//2:center_y+size//2, center_x-size//2:center_x+size//2]
    reshaped = center_region.reshape((-1, 3))
    kmeans = KMeans(n_clusters=1, random_state=0).fit(reshaped)
    predominant_color = kmeans.cluster_centers_.astype(int)[0]
    return tuple(predominant_color)

def analyze_urine_color(color):
    color_rgb = color[::-1]
    if color_rgb[0] > 200 and color_rgb[1] > 200 and color_rgb[2] > 160:
        return "Healthy (Hydrated)"
    elif color_rgb[0] > 160 and color_rgb[1] > 160 and color_rgb[2] < 100:
        return "Dehydrated"
    elif color_rgb[0] < 100 and color_rgb[1] > 100:
        return "Possible liver issues"
    else:
        return "Consult a doctor for detailed analysis"
    
def adjustImg(img, value = 30):
    ## CLAHE ADJUSTMENT
    # Convert the image from BGR to LAB color space
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    l_channel, a, b = cv2.split(lab)
    
    # Apply CLAHE to L-channel
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    c_l_channel = clahe.apply(l_channel)
    
    # Merge the CLAHE enhanced L-channel with the original a and b channel
    lab = cv2.merge((c_l_channel, a, b))
    
    # Convert the LAB image back to BGR
    corrected_image = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)

    ## BRIGHTNESS ADJUSTMENT
    hsv = cv2. cvtColor(corrected_image, cv2.COLOR_BGR2HSV)
    h,s,v = cv2.split(hsv)

    lim = 255 - cv2.split(hsv)
    v[v > lim] = 255
    v[v <= lim] += value

    final_hsv = cv2.merge((h, s, v))
    finalImg = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)

    return finalImg

def analyze_image(img):
    imgStd = adjustImg(img)
    predominant_color = find_predominant_color(imgStd)
    health_status = analyze_urine_color(predominant_color)

    # Convert numpy types to regular Python types
    predominant_color = tuple(map(int, predominant_color))
    color_rgb = predominant_color[::-1]
    
    
    health_status = str(health_status)

    return {"status": health_status, "predominant_color": color_rgb}


@app.route('/analyze', methods=['POST'])
def analyze_urine():
    file = request.files['image'].read()
    npimg = np.fromstring(file, np.uint8)
    img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
    
    analysis_result = analyze_image(img)
    
    return jsonify(analysis_result)

if __name__ == "__main__":
    app.run(debug=True)
