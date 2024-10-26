import cv2

# Open a connection to the webcam (0 is usually the built-in webcam)
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()
image_counter = 0
frame_number = 0
frame_skip = 5
while True:
    ret, frame = cap.read()

    if not ret:
        print("Error: Could not read frame.")
        break
    
    if(frame_number % frame_skip == 0):
        output_dir = f'pictures_webcam'
        cv2.imwrite(f'{output_dir}/frame_v1.0.0_{image_counter}.jpg', frame)
        image_counter += 1        
        print("next itera")
    frame_number += 1

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
