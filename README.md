# VeriCure_Project
AI-Powered Counterfeit Medicine Detection System

# VeriCure: AI-Powered Counterfeit Packaging Detection

VeriCure is a dual-sided verification system that detects counterfeit medicine packaging using deep learning.

## 📥 Model & Dataset Downloads
Due to GitHub upload limits, the trained model weights and sample datasets are hosted externally:
* **Trained Model:** [Download Model Weights from Google Drive](https://drive.google.com/file/d/1JTHn61Z66YQwQNN4oUIdJRVAy74O6aAx/view?usp=sharing)
* **Dataset:** [Download Dataset from Google Drive](https://drive.google.com/file/d/1trJSBX09C5U99ncwDAz_zo2cUYog1gRW/view?usp=sharing)

## 🚀 Execution Guide
1. Create environment:
   ```cmd
   py -3.12 -m venv vc_env
   vc_env\Scripts\python.exe -m pip install numpy tensorflow pillow

   vc_env\Scripts\python.exe scripts/verify.py --front "path/to/front.jpg" --back "path/to/back.jpg"
   
