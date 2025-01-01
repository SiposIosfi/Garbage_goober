import cv2
import socket
import serial
import subprocess
import time

# Serial connection for sending G-code
serial_port = '/dev/ttyUSB0'  # Adjust this to your serial port
baud_rate = 115200

try:
    ser = serial.Serial(serial_port, baud_rate, timeout=1)
    print(f"Serial connection established on {serial_port} at {baud_rate} baud.")
except serial.SerialException as e:
    print(f"Failed to connect to serial port {serial_port}. Error: {e}")
    exit(1)

# Setup UDP listener for movement commands
HOST = '0.0.0.0'  # Listen on all interface
PORT = 65432
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((HOST, PORT))
print(f"Listening for commands on {HOST}:{PORT}")

# Start video feed streaming using FFmpeg
ffmpeg_command = [ 
    "ffmpeg",
    "-f", "v4l2",  # Use Video4Linux2 for camera input
    "-framerate", "60",  # Set frame rate
    "-video_size", "640x360",  # Set resolution to 640x360
    "-i", "/dev/video0",  # Camera device
    "-c:v", "libx264",  # Video codec
    "-preset", "ultrafast",  # Faster encoding
    "-tune", "zerolatency",  # Optimize for low-latency streaming
    "-b:v", "10000k",  # Set video bitrate
    "-f", "mpegts", "udp://192.168.0.101:5000"  # Target UDP stream
]

print("Starting video stream...")
stream_process = subprocess.Popen(ffmpeg_command)

try:
    # Send G91 to set the printer to relative positioning mode
    ser.write(b'G91\n')
    time.sleep(0.1)

    while True:
        # Receive movement commands
        data, addr = server_socket.recvfrom(1024)
        gcode_command = data.decode().strip()
        
        # Send the G-code command to the 3D printer via serial
        ser.write((gcode_command + '\n').encode())
        print(f"Received command from {addr}: {gcode_command}")

except KeyboardInterrupt:
    print("Shutting down...")
finally:
    ser.close()
    server_socket.close()
    stream_process.terminate()
