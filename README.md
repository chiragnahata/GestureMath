# Hand Gesture Math Solver

An interactive real-time hand gesture recognition system that allows you to draw math problems in the air and get instant solutions powered by Google's Gemini AI.

## 📋 Overview

This project demonstrates a real-time hand gesture recognition system using Python, OpenCV, and Gemini AI. Draw mathematical expressions using hand gestures, and the AI will solve them instantly!

## ✨ Features

- **Real-time Hand Detection**: Tracks your hand movements using OpenCV and cvzone
- **Gesture-Based Drawing**: Draw math problems in the air with simple finger gestures
- **AI-Powered Solutions**: Leverages Google's Gemini AI to solve handwritten math problems
- **Interactive Canvas**: Clear and redraw as many times as needed
- **Step-by-Step Solutions**: View detailed solution steps for complex problems

## 🎯 Hand Gestures

| Gesture | Action |
|---------|--------|
| ☝️ Index Finger Only | Draw on canvas |
| 👍 Thumb Only | Clear the canvas |
| ✋ Last 3 Fingers (Middle, Ring, Pinky) | Solve the problem |

## 🛠️ Technologies & Requirements

### Required Software
* **Python 3.10** (Recommended) or Python 3.11
* **Visual Studio C++ Build Tools** (for Windows) - [Download here](https://visualstudio.microsoft.com/downloads/)

### Python Packages
* `opencv-python` - Computer vision and image processing
* `cvzone` - Simplified computer vision tasks
* `mediapipe` - Hand tracking and gesture recognition
* `numpy` - Numerical computing
* `pillow` - Image processing
* `google-generativeai` - Google Gemini AI integration
 
![Python](https://img.shields.io/badge/python-3670A0?logo=python&logoColor=FFFF00)
![cvzone](https://img.shields.io/badge/cvzone_-orange)
![OpenCV](https://img.shields.io/badge/opencv-%23white.svg?logo=opencv&logoColor=white)
![Gemini AI](https://img.shields.io/badge/Gemini%20AI_-%238E75B2?logo=googlegemini&logoColor=white)
![NumPy](https://img.shields.io/badge/numpy-%23013243.svg?logo=numpy&logoColor=white)
![pillow](https://img.shields.io/badge/pillow_-blue)

## 📦 Installation

### Step 1: Install Python 3.10

**Windows:**
1. Download Python 3.10 from [python.org](https://www.python.org/downloads/release/python-31011/)
2. During installation, make sure to check "Add Python to PATH"
3. Verify installation:
   ```bash
   python --version
   # Should show: Python 3.10.x
   ```

**Alternative**: If you have multiple Python versions, use `py -3.10` to run Python 3.10 specifically.

### Step 2: Clone the Repository

```bash
git clone https://github.com/chiragnahata/GestureMath.git
cd GestureMath
```

### Step 3: Create Virtual Environment

**IMPORTANT**: Create a fresh virtual environment with Python 3.10:

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Or if you have multiple Python versions:
py -3.10 -m venv venv
venv\Scripts\activate
```

### Step 4: Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Note**: If you encounter errors with `mediapipe` or binary packages, ensure you have:
- Python 3.10 (not 3.11 or 3.13)
- Visual Studio C++ Build Tools installed
- 64-bit Python version

## 🚀 Usage

### Step 1: Get Gemini API Key

1. Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Click "Create API Key"
3. Copy your API key

### Step 2: Configure API Key

Open `math_solver.py` and replace the API key on line 10:

```python
API_KEY = "your-api-key-here"
```

### Step 3: Run the Application

```bash
python math_solver.py
```

### Step 4: Interact with the Application

1. **Allow Camera Access**: When prompted, allow the application to access your webcam
2. **Draw Your Math Problem**: Use your index finger to draw mathematical expressions
3. **Clear if Needed**: Show only your thumb to clear the canvas
4. **Get Solution**: Show your last 3 fingers (middle, ring, pinky) to solve
5. **Exit**: Press 'q' to quit the application

### Example Workflow

```
1. Show index finger → Draw "2 + 2"
2. Show last 3 fingers → AI solves it → Displays "Answer: 4"
3. Show thumb → Clear canvas → Draw new problem
```

## 🐛 Troubleshooting

### Common Issues

**1. ModuleNotFoundError: No module named 'mediapipe'**
```bash
pip install mediapipe
```

**2. Camera not detected**
- Ensure your webcam is connected
- Close other applications using the camera
- Try changing the camera index in code: `cap = cv2.VideoCapture(1)`

**3. ImportError with binary packages (numpy, mediapipe, etc.)**
- **Solution**: Use Python 3.10 (not 3.11+)
- Recreate virtual environment with Python 3.10:
  ```bash
  # Remove old environment
  rmdir /s venv  # Windows
  # or: rm -rf venv  # Linux/Mac
  
  # Create new with Python 3.10
  py -3.10 -m venv venv
  venv\Scripts\activate
  pip install -r requirements.txt
  ```

**4. "No Python at..." error**
- Your virtual environment's base Python path is invalid
- Delete the `venv` or `py3.10-env` folder
- Recreate the environment with the correct Python version

**5. API Key Issues**
- Ensure you've replaced the API key in `math_solver.py`
- Check if your API key is valid at [Google AI Studio](https://aistudio.google.com/app/apikey)
- Make sure you have internet connectivity

## 📝 Code Explanation

### Key Functions

**1. `get_hand_info(img)`**
- **Purpose**: Detects and tracks the user's hand in each frame
- **Returns**: Finger states and landmark positions
- **Uses**: MediaPipe's HandTrackingModule for accurate hand detection

**2. `draw(info, prev_pos, canvas)`**
- **Purpose**: Draws on the canvas based on detected hand gestures
- **Parameters**:
  - `info`: Hand gesture information (finger positions)
  - `prev_pos`: Previous drawing position for smooth lines
  - `canvas`: Drawing canvas overlay
- **Logic**: 
  - Index finger up → Draw line
  - Thumb only → Clear canvas

**3. `send_to_ai(model, canvas, fingers)`**
- **Purpose**: Sends the drawn math problem to Gemini AI for solving
- **Parameters**:
  - `model`: Gemini AI model instance
  - `canvas`: Image containing the drawn math problem
  - `fingers`: Current finger state to trigger solving
- **Returns**: Solution text with answer and steps

**4. `preprocess_image(canvas)`**
- **Purpose**: Enhances the drawn image for better AI recognition
- **Process**: Converts to grayscale and applies thresholding

**5. `parse_ai_response(response)`**
- **Purpose**: Extracts the final answer and solution steps from AI response
- **Returns**: Formatted answer and step-by-step solution



## Hand Detection Concept

<img src="https://github.com/LasithaAmarasinghe/Hand-Gesture-Math-Solver/assets/106037441/196a14ec-6067-494c-8e06-69873fa418f3" >

___

**Left-Right Hand Detection**

<img src="https://github.com/LasithaAmarasinghe/Hand-Gesture-Math-Solver/assets/106037441/c0eaf562-bb89-4b47-b9f8-4bb96ec3e442" width="400" height="240">
<img src="https://github.com/LasithaAmarasinghe/Hand-Gesture-Math-Solver/assets/106037441/a7c1a542-8b85-42a2-87fa-bb20ff280a1e" width="400" height="240">

___

**Hand Gesture Detection**

<img src="https://github.com/LasithaAmarasinghe/Hand-Gesture-Math-Solver/assets/106037441/56434be0-8338-41e2-b060-5b14e69f6325" width="400" height="280">
<img src="https://github.com/LasithaAmarasinghe/Hand-Gesture-Math-Solver/assets/106037441/b66a3d35-f7f7-4b75-b7db-c93ee40d6841" width="400" height="280">

## 📊 Project Structure

```
Hand-Gesture-Math-Solver/
├── app.py                  # Enhanced version with detailed steps
├── math_solver.py          # Main application (simple version)
├── app2.py                 # Alternative implementation
├── app3.py                 # Another variant
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── LICENSE                # MIT License
└── py3.10-env/            # Virtual environment (create this)
```

## 🎬 Demo & Results

**Math Expression Detection & Canvas**

<img src="https://github.com/LasithaAmarasinghe/Hand-Gesture-Math-Solver/assets/106037441/e9558800-a17f-432d-a4f5-d00d0a352cfb" width="400" height="240">
<img src="https://github.com/LasithaAmarasinghe/Hand-Gesture-Math-Solver/assets/106037441/64664179-a2cc-43a2-af2b-409a6beb4325" width="400" height="240">

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Chirag Nahata**
- GitHub: [@chiragnahata](https://github.com/chiragnahata)
- Repository: [GestureMath](https://github.com/chiragnahata/GestureMath)

## 🙏 Acknowledgments

- Google Gemini AI for the powerful AI capabilities
- MediaPipe for robust hand tracking
- cvzone for simplified computer vision tasks
- Original inspiration from various hand gesture recognition projects

## ⚠️ Important Notes

1. **Python Version**: This project works best with **Python 3.10**. Using Python 3.11+ may cause binary compatibility issues with mediapipe.

2. **API Key Security**: Never commit your actual API key to version control. Use environment variables in production:
   ```python
   import os
   API_KEY = os.getenv('GEMINI_API_KEY')
   ```

3. **Camera Requirements**: Requires a working webcam with decent lighting for optimal hand detection.

4. **Performance**: First run may be slower as models are loaded. Subsequent runs will be faster.

---

**Made with ❤️ by Chirag Nahata**

