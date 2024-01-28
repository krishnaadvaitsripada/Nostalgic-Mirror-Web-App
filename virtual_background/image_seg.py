import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import cv2

model_path = 'selfie_segmenter_landscape.tflite'

BaseOptions = mp.tasks.BaseOptions
ImageSegmenter = mp.tasks.vision.ImageSegmenter
ImageSegmenterOptions = mp.tasks.vision.ImageSegmenterOptions
VisionRunningMode = mp.tasks.vision.RunningMode

base_options = BaseOptions(model_asset_path=model_path)

# Create a image segmenter instance with the live stream mode:
def print_result(result: List[Image], output_image: Image, timestamp_ms: int):
    print('segmented masks size: {}'.format(len(result)))
    
options = ImageSegmenterOptions(
    base_options=BaseOptions(model_asset_path=model_path),
    running_mode=VisionRunningMode.LIVE_STREAM,
    output_category_mask=True)
with ImageSegmenter.create_from_options(options) as segmenter:
    cap = cv2.VideoCapture(0)    
    
    # Load a replacement background image for each frame
    replacement_background = cv2.imread("virtual_background/nostalgia.jpg")  # Replace with your replacement background image path
    
    while True:
        ret, frame = cap.read()

        if not ret:
            print("Failed to capture frame")
            break
        
        # Convert the frame received from OpenCV to a MediaPipe’s Image object.
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
    
    
    