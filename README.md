
# Garbage Goober 🤖💧🧴

**Garbage Goober** is a whimsical yet hardworking recycling robot designed to help keep our planet clean, one bottle at a time. With sensors, AI, and a love for litter, Garbage Goober identifies, collects, and properly disposes of water bottles to make sure they’re recycled. This project is a tribute to the beloved *Rick and Morty* character with a mission to tackle plastic waste!

## Features

- **Bottle Detection**: Uses state-of-the-art object detection to identify water bottles in the environment.
- **Navigation**: Autonomous navigation to seek and collect plastic bottles.
- **Friendly & Efficient**: Garbage Goober loves doing his job, never misses a bottle, and never complains.
- **Real-Time Notifications**: Keeps you updated on its collection stats and progress.

## Getting Started

### Prerequisites

- **Hardware**: Raspberry Pi, NVIDIA GPU for image processing (optional), sensors for bottle detection.
- **Software**: Python, OpenCV, TensorFlow (or other detection libraries).
- **Other Requirements**: Basic understanding of Git for version control.

### Installation

1. **Clone the Repository**
   ```bash
   sudo git clone https://github.com/SiposIosfi/Garbage_goober.git
   ```
   AND
   ```bash
   git clone https://github.com/AlexandruARV/robocop.git
   ```
2. **Navigate to the Directory**
   ```bash
   cd Garbage-goober
   ```
3. **Install Dependencies for Command Center**
   ```bash
   pip install -r requirements_command_center.txt --break-system-packages
   ```
4. **Install Dependencies for Robot**
    ```bash
   pip install -r requirements_robot.txt --break-system-packages
   ```
5. **Set Up Configuration Files** (if necessary):
   - Ensure all API keys, device IPs, and settings are configured properly.
6. **3d Desighn in OnShape**:
   -https://cad.onshape.com/documents/f3c4ef143a5cdcfd55159fe6/w/ba8dfa80169bced1aa6ce4df/e/ea9f4c2c1d49a9316b781902?renderMode=0&uiState=672e70436bdd0a33510a0164
## Usage

1. **Start the Bottle Detector**:
   ```bash
   python detector.py
   ```
2. **Monitor Goober's Progress**:
   - Watch the live feed to see Garbage Goober in action as it hunts for bottles!
3. **Access Reports**:
   - Check collected bottle count, recycling efficiency, and more.

## Project Structure

- **/src**: Main codebase, including detection, navigation, and control modules.
- **/config**: Configuration files for hardware and detection settings.
- **/data**: Logs and statistics on collection activity.
- **README.md**: Project documentation (you're here!).

## Contributing

Contributions are welcome! Feel free to submit pull requests with new features, bug fixes, or improvements.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -m 'Add some feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

Enjoy using **Garbage Goober** and feel good knowing that every bottle collected is a step toward a cleaner world! 🌍💧
