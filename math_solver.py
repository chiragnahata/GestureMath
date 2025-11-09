import cvzone
import cv2
from cvzone.HandTrackingModule import HandDetector
import numpy as np
import google.generativeai as genai
from PIL import Image
import re

# Set your API key directly in the script
API_KEY = "AIzaSyBj0NVO43NcnMElpvJRdR8oLredTqstaQ0"

# Configure the generative AI model
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash-latest')

# Initialize webcam
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)
detector = HandDetector(staticMode=False, maxHands=2, modelComplexity=1, detectionCon=0.7, minTrackCon=0.5)

def get_hand_info(img):
    hands, img = detector.findHands(img, draw=True, flipType=True)
    if hands:
        hand = hands[0]
        lmList = hand["lmList"]
        fingers = detector.fingersUp(hand)
        return fingers, lmList
    return None

def draw(info, prev_pos, canvas):
    fingers, lmList = info
    current_pos = None
    if fingers == [0, 1, 0, 0, 0]:
        current_pos = lmList[8][0:2]
        if prev_pos is None:
            prev_pos = current_pos
        cv2.line(canvas, tuple(current_pos), tuple(prev_pos), (255, 0, 255), 10)
    elif fingers == [1, 0, 0, 0, 0]:
        canvas[:] = 0  # Clear the canvas
    return current_pos, canvas

def send_to_ai(model, canvas, fingers):
    if fingers == [0, 0, 1, 1, 1]:
        pil_image = Image.fromarray(canvas)
        response = model.generate_content([
            """
            Solve this handwritten math problem. 
            Only provide the final answer without any steps.
            For equations, just give the value of the variable (e.g., x = 2).
            For calculations, just give the final result.
            Keep your response very brief - just the answer itself.
            """, 
            pil_image
        ])
        if response and response.text:
            return response.text.strip()
        else:
            return "Error: No response from AI model."
    return None

def extract_final_answer(text):
    """Extract just the final answer from the solution text"""
    # Try to find "Final Answer" or similar patterns
    final_answer_match = re.search(r'(Final Answer|Answer|Therefore|Thus|∴).*?([^\.]+)', text, re.IGNORECASE)
    if final_answer_match:
        return final_answer_match.group(2).strip()
    
    # Look for variable = value pattern
    var_value_match = re.search(r'([a-z])\s*=\s*(-?\d+\.?\d*)', text, re.IGNORECASE)
    if var_value_match:
        return f"{var_value_match.group(1)} = {var_value_match.group(2)}"
    
    # If no patterns match, return the last non-empty line
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    if lines:
        return lines[-1]
    
    return text

def draw_centered_text(img, text, font=cv2.FONT_HERSHEY_SIMPLEX, font_scale=1.2, color=(0, 255, 0), thickness=2):
    """Draw text centered on the image with a contrasting background"""
    # Get text size
    text_size = cv2.getTextSize(text, font, font_scale, thickness)[0]
    
    # Calculate position to center text
    text_x = (img.shape[1] - text_size[0]) // 2
    text_y = img.shape[0] // 2
    
    # Create a dark background for better visibility
    padding = 20
    cv2.rectangle(img, 
                 (text_x - padding, text_y - text_size[1] - padding),
                 (text_x + text_size[0] + padding, text_y + padding),
                 (0, 0, 0), -1)
    
    # Draw the text
    cv2.putText(img, text, (text_x, text_y), font, font_scale, color, thickness, cv2.LINE_AA)

def main():
    prev_pos = None
    canvas = None
    ai_result = ""
    solution_displayed = False
    
    # Create background image for gesture instructions
    gesture_instructions = np.zeros((150, 400, 3), dtype=np.uint8)
    cv2.putText(gesture_instructions, "Index finger: Draw", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 1)
    cv2.putText(gesture_instructions, "Thumb only: Clear", (20, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 1)
    cv2.putText(gesture_instructions, "Three fingers: Solve", (20, 110), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 1)

    while True:
        success, img = cap.read()
        img = cv2.flip(img, 1)
        if canvas is None:
            canvas = np.zeros_like(img)
        
        info = get_hand_info(img)
        if info:
            fingers, lmList = info
            prev_pos, canvas = draw(info, prev_pos, canvas)
            result = send_to_ai(model, canvas, fingers)
            if result:
                ai_result = extract_final_answer(result)
                solution_displayed = True
            elif fingers == [1, 0, 0, 0, 0]:
                ai_result = ""  # Clear AI result when canvas is cleared
                solution_displayed = False

        # Combine webcam feed with canvas
        image_combined = cv2.addWeighted(img, 0.7, canvas, 0.3, 0)
        
        # Display title at the top
        cv2.putText(image_combined, "Draw the math problem here", 
                   (image_combined.shape[1]//4, 50), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 2, cv2.LINE_AA)
        
        # Show small gesture instructions in bottom-left corner
        h, w = gesture_instructions.shape[:2]
        image_combined[image_combined.shape[0]-h-10:image_combined.shape[0]-10, 10:10+w] = gesture_instructions
        
        # Display solution if available
        if solution_displayed and ai_result:
            draw_centered_text(image_combined, f"Answer: {ai_result}")

        cv2.imshow("Math Problem Solver", image_combined)
        
        # Exit the loop when 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()