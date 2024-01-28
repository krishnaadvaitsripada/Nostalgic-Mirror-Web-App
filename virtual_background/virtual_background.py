import cv2
import numpy as np

def process_frame(frame, replacement_background):
    # Convert the frame to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define the range for the color you want to replace
    lower_color = np.array([40, 40, 40])  # Adjust these values based on your specific color
    upper_color = np.array([80, 255, 255])

    # Create a mask for the color
    mask = cv2.inRange(hsv, lower_color, upper_color)

    # Invert the mask to get non-colored areas
    mask_inv = cv2.bitwise_not(mask)

    # Extract the region of interest (ROI) from the frame
    fg = cv2.bitwise_and(frame, frame, mask=mask)

    # Extract the background region from the replacement background
    
    # Ensure mask_inv is a grayscale image
    if len(mask_inv.shape) > 2:  # if mask_inv is not grayscale
        mask_inv = cv2.cvtColor(mask_inv, cv2.COLOR_BGR2GRAY)

    # Ensure mask_inv has the same size as replacement_background
    if mask_inv.shape != replacement_background.shape[:2]:  # if sizes don't match
        mask_inv = cv2.resize(mask_inv, (replacement_background.shape[1], replacement_background.shape[0]))

    bg = cv2.bitwise_and(replacement_background, replacement_background, mask=mask_inv)
    
    # Ensure fg is a grayscale image
    if len(fg.shape) > 2:  # if fg is not grayscale
        fg = cv2.cvtColor(fg, cv2.COLOR_BGR2GRAY)

    # Ensure fg has the same size as bg
    if fg.shape != bg.shape:  # if sizes don't match
        fg = cv2.resize(fg, (bg.shape[1], bg.shape[0]))


    # Combine the foreground and background to get the final frame
    result = cv2.add(fg, bg)

    return result

def main():
    cap = cv2.VideoCapture(0)  # 0 corresponds to the default webcam
    
    # Load a replacement background image for each frame
    replacement_background = cv2.imread("virtual_background/nostalgia.jpg")  # Replace with your replacement background image path

    while True:
        ret, frame = cap.read()

        if not ret:
            print("Failed to capture frame")
            break

        cv2.imshow("test", replacement_background)

        processed_frame = process_frame(frame, replacement_background)

        cv2.imshow('Virtual Background', processed_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
    