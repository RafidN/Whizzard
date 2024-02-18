from flask import Flask, request, jsonify
from flask_cors import CORS
import cv2
import numpy as np
from sklearn.cluster import KMeans
import colorsys

app = Flask(__name__)
CORS(app)  # This is crucial for cross-origin requests from your React app

def find_predominant_color_rgb(image):
    h, w, _ = image.shape
    center_x, center_y = w // 2, h // 2
    size = min(w, h) // 8
    center_region = image[center_y-size//2:center_y+size//2, center_x-size//2:center_x+size//2]
    reshaped = center_region.reshape((-1, 3))
    kmeans = KMeans(n_clusters=1, random_state=0).fit(reshaped)
    predominant_color = kmeans.cluster_centers_.astype(int)[0]
    return tuple(predominant_color)

def analyze_urine_color(color_hsv):
    if color_hsv[2] <=45:
        return "Very Dark" #severe dehydration
    elif color_hsv[0] > 45 and color_hsv[0] < 65 and color_hsv[2] > 85:
        return "Pale Yellow"
    elif color_hsv[0] > 45 and color_hsv[0] < 65 and color_hsv[2] <= 85:
        return "Dark Yellow"
    elif color_hsv[0] > 25 and color_hsv[0] < 45 and color_hsv[2] > 85:
        return "Orange"
    elif color_hsv[0] > 25 and color_hsv[0] < 45 and color_hsv[2] <= 85:
        return "Dark Orange"
    else:
        return "Consult a doctor for detailed analysis"
    
def rgb_to_hsv(r, g, b):
    r, g, b = r/255.0, g/255.0, b/255.0
    mx = max(r, g, b)
    mn = min(r, g, b)
    df = mx-mn
    if mx == mn:
        h = 0
    elif mx == r:
        h = (60 * ((g-b)/df) + 360) % 360
    elif mx == g:
        h = (60 * ((b-r)/df) + 120) % 360
    elif mx == b:
        h = (60 * ((r-g)/df) + 240) % 360
    if mx == 0:
        s = 0
    else:
        s = (df/mx)*100
    v = mx*100
    return h, s, v

def add_thirty_value(color_hsv):
    # Convert the predominant color to a list for modification
    hsv_list = list(color_hsv)

    # Modify the values as needed
    # For example, let's assume you want to increase the red component by 10
    if(hsv_list[2] <= 70):
         hsv_list[2] += 30
    else:
        hsv_list[2] = 100
        
    # Convert each value to an integer
    hsv_list = [int(value) for value in hsv_list]
    
    
    # Convert the list back to a tuple if necessary
    hsv_tuple = tuple(hsv_list)
    return hsv_tuple
    

def analyze_image(img):
    predominant_color = find_predominant_color_rgb(img)

    # Convert numpy types to regular Python types
    predominant_color = tuple(map(int, predominant_color))
    
    color_rgb = predominant_color[::-1]
    
    color_hsv = rgb_to_hsv(color_rgb[0], color_rgb[1], color_rgb[2])
    brightened_hsv = add_thirty_value(color_hsv)
    health_status = analyze_urine_color(brightened_hsv)
    health_status = str(health_status)

    return {"status": health_status, "predominant_color_rgb": color_rgb, "brightened_color_hsv": brightened_hsv}


@app.route('/analyze', methods=['POST'])
def analyze_urine():
    file = request.files['image'].read()
    npimg = np.fromstring(file, np.uint8)
    img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

    analysis_result = analyze_image(img)

    return jsonify(analysis_result)

if __name__ == "__main__":
    app.run(debug=True)