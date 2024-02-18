from flask import Flask, request, jsonify
from flask_cors import CORS
import cv2
import numpy as np
from sklearn.cluster import KMeans

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
    
    #Black
    if color_hsv[2] <=45:
        return "Dark brown or black: Dark brown or black urine is indicative of severe hydration levels and may signal an underlying health concern. This profound discoloration is often associated with the presence of certain substances, such as blood or other pigments, in the urine. It can be a potential indication of a more serious condition, including but not limited to kidney or liver issues, hemolysis (breakdown of red blood cells), or certain medications... | Whizzard strongly recommends seeking medical attention promptly to address the root cause of the discoloration and determine the appropriate course of action for optimal health and well-being!" #severe dehydration
    
    #Clear
    elif color_hsv[1] <= 21 and color_hsv[2] >= 95:
        return "Clear: Clear urine is indicative of optimal hydration levels, often resulting from a well-maintained water intake. While this is generally favorable for healthy kidney function, it's important to be mindful of potential overhydration, leading to an electrolyte imbalance due to a substantial increase in water intake... | Whizzard suggests considering a moderation in water consumption to maintain a harmonious electrolyte balance while supporting overall well-being!"
    
    #Pale Yellow and Dark Yellow
    elif color_hsv[0] > 45 and color_hsv[0] <= 65 and color_hsv[2] > 85:
        return "Pale or transparent yellow: Pale or transparent urine is indicative of optimal hydration levels, often resulting from a well-maintained water intake... | Whizzard suggests maintaining this hydration approach to achieve an optimal balance for overall health and wellness!"
    
    #Dark Yellow or Orange
    elif (color_hsv[0] > 45 and color_hsv[0] <= 65 and color_hsv[2] <= 85) or (color_hsv[0] > 25 and color_hsv[0] <= 45 and color_hsv[2] > 75):
        return "Dark yellow or orange: Dark yellow urine is indicative of suboptimal hydration levels, often resulting from insufficient water intake. Orange urine could also be a result of a change of diet, especially carrots. This darker hue is typically attributed to a reduced volume of water available to dissolve and excrete waste products. This decrease in fluid levels leads to a higher concentration of minerals in the urine, resulting in its darker appearance. Additionally, the reduction in normal water content within the body can adversely affect physiological functions due to the imbalance of electrolytes... | Whizzard recommends an immediate consumption of 2-3 cups of water and an overall increase in water intake to restore an adequate balance of electrolytes!"
    
    #Dark Orange/Brown
    elif color_hsv[0] > 25 and color_hsv[0] <= 45 and color_hsv[2] <= 75:
        return "Dark orange or brown: Dark orange or brown urine is indicative of suboptimal hydration levels, often stemming from insufficient water intake. This intense coloration is typically associated with a significant decrease in volume of water available to dissolve and eliminate waste products. The diminished fluid levels contribute to a higher concentration of minerals in the urine, manifesting in the dark orange or brown appearance. Moreover, this could represent an increased workload on the kidneys, as they strive to filter and excrete waste products in a more concentrated urine, which could negatively impact physiological functions... | Whizzard recommends an immediate intake of 2-3 cups of water and an overall increase of water consumption to restore a balance of electrolytes, potentially relieving kidney stress and supporting optimal well-being."
    
    #Pink or Red
    elif (color_hsv[0] >= 0 and color_hsv[0] <= 25) or (color_hsv[0] > 270 and color_hsv[0] <= 360):
        return "Pink or red: The presence of pink or red urine can be indicative of various factors, including the presence of blood. This discoloration may stem from conditions such as urinary tract infections, kidney stones, trauma, or other underlying health issues. However, this could be a result of a change of diet, such as beets... | Whizzard strongly suggests promptly consulting with a healthcare professional if blood is clearly noticed in the urine, to identify the underlying cause and appropriate course of action for optimal health and well-being!"
    
    #Blue or Green
    elif (color_hsv[0] > 65 and color_hsv[0] <= 270):
        return "Blue or green: Blue or green urine can be influenced by various factors. Certain brightly colored food dyes, particularly methylene blue, and the consumption of asparagus are known to cause greenish discoloration. Additionally, urinary tract infections can contribute to changes in urine color, including shades of blue or green. If you observe persistent blue or green urine, it is advisable to consult with a healthcare professional for a comprehensive evaluation... | Whizzard suggests discussing dietary habits, medications, and the possibility of a urinary tract infection with your healthcare provider to help identify the specific cause and ensure appropriate measures are taken for optimal health!"
    
    else:
        return "Consult a doctor for a detailed analysis"
    
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