import os
import sys
import argparse
import numpy as np
import tensorflow as tf

# =====================================================================
# EXACT LOCAL PATHS & CONFIGURATION
# =====================================================================
# Using your exact local path structure
MODEL_PATH = r"D:\hamad\FYP_Project\VeriCure_Project\models\VeriCure_Model_v1.0.keras"
IMG_SIZE = (512, 512)
CONFIDENCE_THRESHOLD = 0.70  # Below 70% confidence is categorized as Unknown

# Your exact 9 classes from 'dataset_final'
CLASS_NAMES = [
    "Background_Unknown",
    "froben_Counterfeit",
    "froben_Genuine",
    "glucophage_Counterfeit",
    "glucophage_Genuine",
    "nise_Counterfeit",
    "nise_Genuine",
    "panadol_Counterfeit",
    "panadol_Genuine"
]

# =====================================================================
# PROCESSING & PREDICTION
# =====================================================================
def load_and_preprocess(img_path):
    if not os.path.exists(img_path):
        print(f"[ERROR] Target image not found: {img_path}")
        sys.exit(1)
    img = tf.keras.utils.load_img(img_path, target_size=IMG_SIZE)
    img_array = tf.keras.utils.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0)  # Create batch axis (1, 224, 224, 3)
    return img_array

def predict_side(model, img_path):
    processed = load_and_preprocess(img_path)
    preds = model.predict(processed, verbose=0)[0]
    best_idx = np.argmax(preds)
    confidence = preds[best_idx]
    predicted_class = CLASS_NAMES[best_idx]
    return predicted_class, confidence

# =====================================================================
# SYSTEM VERIFICATION LOGIC
# =====================================================================
def main():
    parser = argparse.ArgumentParser(description="VeriCure Local CMD Authenticator")
    parser.add_argument("--front", required=True, help="Path to front side image")
    parser.add_argument("--back", required=True, help="Path to back side image")
    args = parser.parse_args()

    print("\n" + "="*60)
    print("           VERICURE LOCAL PACKAGING VERIFICATION          ")
    print("="*60)

    # Load Model
    if not os.path.exists(MODEL_PATH):
        print(f"[ERROR] Model file not found at: {MODEL_PATH}")
        print("Please copy your trained VeriCure_Model_v1.0.keras to this directory.")
        sys.exit(1)

    print("[*] Loading local neural network...")
    model = tf.keras.models.load_model(MODEL_PATH)

    # Run predictions
    print("[*] Processing Front Image...")
    front_class, front_conf = predict_side(model, args.front)
    
    print("[*] Processing Back Image...")
    back_class, back_conf = predict_side(model, args.back)

    print("-" * 60)
    print(f"Front Scan Result: {front_class} ({front_conf*100:.1f}%)")
    print(f"Back Scan Result:  {back_class} ({back_conf*100:.1f}%)")
    print("-" * 60)

    # 1. Guardrail Check: Low Confidence or "Background_Unknown"
    if (front_class == "Background_Unknown" or back_class == "Background_Unknown" or 
        front_conf < CONFIDENCE_THRESHOLD or back_conf < CONFIDENCE_THRESHOLD):
        print("\n[VERDICT] ⚠️ UNKNOWN / SUSPICIOUS")
        print("Reason: Model could not securely recognize the packaging or the image details were unclear.")
        print("="*60 + "\n")
        return

    # Extract Brand and Status (e.g., "panadol" and "Genuine")
    front_brand, front_status = front_class.split("_")
    back_brand, back_status = back_class.split("_")

    # 2. Guardrail Check: Brand Mismatch (e.g. user scans Panadol front and Nise back)
    if front_brand != back_brand:
        print("\n[VERDICT] ⚠️ SUSPICIOUS PACKAGING")
        print(f"Reason: Brand mismatch detected! (Front: {front_brand.upper()} | Back: {back_brand.upper()})")
        print("="*60 + "\n")
        return

    # 3. Final Multi-Side Decision Check
    if front_status == "Genuine" and back_status == "Genuine":
        print(f"\n[VERDICT] ✅ GENUINE {front_brand.upper()} DETECTED")
        print("Details: Both sides match our genuine verification metrics.")
    else:
        print(f"\n[VERDICT] ❌ COUNTERFEIT {front_brand.upper()} DETECTED")
        print(f"Details: Fail. (Front Side: {front_status} | Back Side: {back_status})")
    
    print("="*60 + "\n")

if __name__ == "__main__":
    main()