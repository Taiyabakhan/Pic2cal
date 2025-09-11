# Pic2Cal - Picture to Calorie Analyzer

---

## 🚀 Project Overview

Pic2Cal is a web-based application that estimates nutritional values (calories, macro-nutrients, etc.) from images of food. Using computer vision and machine learning, the app allows users to upload a photo, and it returns an approximate calorie count, helping with diet tracking and healthy eating.

---

## 🔍 Features

- Upload images of food and get calorie & ingredient estimation
- Preprocessing of images to improve accuracy (resizing, normalization, etc.)
- Use of a trained ML model (e.g., convolutional neural network) for food classification / detection
- Smooth user interface (templates, static content)
- Responsive design so the app works on mobile & desktop
- Possibility of extensions:
  - adding local cuisine datasets
  - integrating with food-logging APIs
  - multilingual support

---

## 🛠️ Tech Stack

| Component | Technology / Framework |
| :--- | :--- |
| **Backend** | Python + Flask (or similar) |
| **Frontend / UI** | HTML, CSS, JavaScript, Templates |
| **Machine Learning** | TensorFlow / PyTorch / Keras |
| **Deployment** | Heroku / AWS / any cloud host |
| **Others** | Image processing (OpenCV etc.), API endpoints |


## 📁 Repository Structure

```

Pic2Cal/
│
├── api/ \# Backend API code (handling requests, model inference)
├── static/ \# Static files (CSS, JS, images)
├── templates/ \# HTML templates for UI
├── models/ \# Trained model files
├── app.py \# Main application server
└── requirements.txt \# Python dependencies
└── README.md \# this file

```

---

## ⚙️ Installation & Setup

1.  Clone the repo:
    ```bash
    git clone [https://github.com/Taiyabakhan/Pic2Cal.git](https://github.com/Taiyabakhan/Pic2Cal.git)
    cd Pic2Cal
    ```
2.  Create a virtual environment and activate it:
    ```bash
    python3 -m venv venv
    source venv/bin/activate        # on Linux / macOS
    venv\Scripts\activate          # on Windows
    ```
3.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4.  Place your trained model file in the `models/` directory (name it appropriately, e.g., `model.h5`).
5.  Run the application:
    ```bash
    python app.py
    ```
6.  Open your browser and go to: `http://localhost:5000` (or whatever port is set).

---

## 🔬 Usage

1.  Go to the upload page, select or drag a food image.
2.  The image is preprocessed and passed to the ML model.
3.  Receive an estimated calorie count and nutritional breakdown.
4.  Optional: upload more images for testing / demonstration.

---

## 🤝 Contribution

Contributions are welcome! If you want to contribute, please:

1.  Fork the repo.
2.  Create your feature branch (`git checkout -b feature/YourFeature`).
3.  Commit your changes (`git commit -m "Add some feature"`).
4.  Push to your branch (`git push origin feature/YourFeature`).
5.  Open a Pull Request describing your changes.

---

## 📝 License

*(Specify a license here if you have one, e.g., MIT, Apache 2.0. Otherwise, you can note that it's for academic or personal use.)*

---

## 📌 Contact

**Taiyaba Khan**
Bareilly, Uttar Pradesh
Email: khantaiyaba610@gmail.com
GitHub: [github.com/Taiyabakhan](https://github.com/Taiyabakhan)
````
