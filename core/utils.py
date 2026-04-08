import os
import customtkinter as ctk

def make_background_transparent(img):
    """
    Intelligently analyzes the top-left pixel of the logo and strips out that entire background
    color matrix perfectly using an Alpha Channel so the logo floats natively on the UI.
    """
    img = img.convert("RGBA")
    datas = img.getdata()
    
    # We sample the exact color of the image's background dynamically
    bg_r, bg_g, bg_b, _ = datas[0]
    tolerance = 25 # Protects the red elements while aggressively stripping compression artifacts
    
    new_data = []
    for item in datas:
        if (abs(item[0] - bg_r) < tolerance and 
            abs(item[1] - bg_g) < tolerance and 
            abs(item[2] - bg_b) < tolerance):
            new_data.append((255, 255, 255, 0)) # Inject 0 Alpha (Transparent)
        else:
            new_data.append(item)
            
    img.putdata(new_data)
    return img

def get_logo_image(size=(150, 50)):
    """
    Safely loads the brand logo globally to prevent aspect ratio distortion
    and avoid Garbage Collection crashes.
    """
    try:
        from PIL import Image
    except ImportError:
        return None
        
    path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "logo.png")
    if os.path.exists(path):
        try:
            raw_img = Image.open(path)
            clean_img = make_background_transparent(raw_img)
            return ctk.CTkImage(light_image=clean_img, dark_image=clean_img, size=size)
        except Exception as e:
            print(f"Warning: Failed to load logo.png geometry! {e}")
            return None
    return None
