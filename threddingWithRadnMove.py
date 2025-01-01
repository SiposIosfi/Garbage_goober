import cv2
import torch
import socket
import threading
import time
from collections import deque

ROBOT_IP = "192.168.0.231"
ROBOT_PORT = 65432

# Set up UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Load YOLOv5 model
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

# Open video stream
stream_url = "udp://192.168.0.231:5000"
cap = cv2.VideoCapture(stream_url, cv2.CAP_FFMPEG)
cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

if not cap.isOpened():
    print("Error: Unable to access video stream.")
    exit(1)

frame_width, frame_height = 640, 360
center_x, center_y = frame_width // 2, frame_height // 2
tolerance = 50

# Proportional control constant
k_p = 0.015  # Adjust this value for fine-tuning

# Shared data
frame_queue = deque(maxlen=1)  # Hold the most recent frame
stop_thread = False

# Detection timeout and search state
last_detection_time = time.time()
timeout_threshold = 2  # seconds
is_searching = False
rotation_angle = 10  # Incremental rotation angle
command_delay = 10  # Delay in seconds between commands

# Video reading thread
def read_frames():
    global stop_thread
    while not stop_thread:
        ret, new_frame = cap.read()
        if ret:
            frame_queue.append(new_frame)

# Start the frame reading thread
thread = threading.Thread(target=read_frames, daemon=True)
thread.start()

try:
    while True:
        if not frame_queue:
            continue

        # Get the latest frame
        current_frame = frame_queue.pop()

        # Perform object detection
        results = model(current_frame)
        detections = results.xyxy[0].cpu().numpy()

        largest_bottle = None
        max_area = 0
        for det in detections:
            x1, y1, x2, y2, conf, class_id = det
            class_id = int(class_id)
            label = model.names[class_id]
            color = (0, 255, 0) if label == "bottle" else (0, 0, 255)

            # Draw bounding box and label for all detected objects
            cv2.rectangle(current_frame, (int(x1), int(y1)), (int(x2), int(y2)), color, 2)
            cv2.putText(current_frame, f"{label} {conf:.2f}", (int(x1), int(y1) - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

            # Check if the detected object is a "bottle" and track the largest one
            if label == "bottle":
                area = (x2 - x1) * (y2 - y1)
                if area > max_area:
                    max_area = area
                    largest_bottle = (int(x1), int(y1), int(x2), int(y2))

        if largest_bottle:
            # Reset timeout and process detection
            last_detection_time = time.time()
            is_searching = False
            x1, y1, x2, y2 = largest_bottle
            bottle_center_x = (x1 + x2) // 2

            # Draw the vertical centerline of the bottle
            cv2.line(current_frame, (bottle_center_x, 0), (bottle_center_x, frame_height), (255, 0, 0), 2)
            cv2.putText(current_frame, "Bottle Centerline", (bottle_center_x + 5, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)

            # Draw the vertical centerline of the frame
            cv2.line(current_frame, (center_x, 0), (center_x, frame_height), (0, 255, 255), 2)
            cv2.putText(current_frame, "Frame Centerline", (center_x + 5, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)

            # Calculate movement to align bottle centerline with frame centerline
            distance_to_center = bottle_center_x - center_x
            move_x = int(k_p * distance_to_center)  # Proportional control

            # Ensure the step size is within a safe range
            if abs(move_x) > 10:  # Cap the step size to prevent large movements
                move_x = 10 if move_x > 0 else -10

            if abs(distance_to_center) > tolerance:
                gcode_command = f'G0 X{move_x} Y{move_x} F2000\n'
                sock.sendto(gcode_command.encode(), (ROBOT_IP, ROBOT_PORT))
                print(f"Aligning bottle centerline. Command: {gcode_command.strip()}")
        else:
            # Check if timeout has been exceeded
            if time.time() - last_detection_time > timeout_threshold:
                if not is_searching:
                    is_searching = True

                # Send incremental rotation command with delay
                gcode_command = f'G0 X{rotation_angle} F3000\n'
                sock.sendto(gcode_command.encode(), (ROBOT_IP, ROBOT_PORT))
                print(f"No bottle detected. Rotating: {gcode_command.strip()}")

                # Update rotation angle to continue 360-degree movement
                rotation_angle += 10
                if rotation_angle >= 360:
                    rotation_angle = 0  # Reset angle after a full rotation

                # Delay to allow the robot to execute the command
                time.sleep(command_delay)

        # Visualization
        cv2.line(current_frame, (center_x - tolerance, 0), (center_x - tolerance, frame_height), (255, 0, 0), 1)
        cv2.line(current_frame, (center_x + tolerance, 0), (center_x + tolerance, frame_height), (255, 0, 0), 1)
        cv2.line(current_frame, (0, center_y - tolerance), (frame_width, center_y - tolerance), (255, 0, 0), 1)
        cv2.line(current_frame, (0, center_y + tolerance), (frame_width, center_y + tolerance), (255, 0, 0), 1)

        cv2.imshow("Detection", current_frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    stop_thread = True
    thread.join()
    cap.release()
    cv2.destroyAllWindows()
