# Keyboard Overlay App

## Overview
**MapleStory Keyboard Overlay** is a customizable on-screen keyboard display.
It helps visualize keybindings, track skill usage, and enhance gameplay efficiency.  

## Demo
![Demo](https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExdGptcDBsemJlZmQzbWFndGVoNmt6OWl4YmMya3RpYnJ1cGF5ZmgyaCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/xbLfDwJortkei5pvzr/giphy.gif)

## Features
- **Skill Icons Display** – Matches your in-game key bindings.  
- **Transparent Overlay** – View key presses without obstructing gameplay (optimized for OBS).  
- **Key Press Tracking** – Monitor skill usage in real time.  

## Instructions

### ⚠️ Important Warning  
As with all keyboard overlays, **be cautious** not to type sensitive information while the overlay is running.  

### 📌 How to Use with OBS Studio

#### **1️⃣ Setup**
1. **Download & Extract**    

2. **Capture Key Bindings:**  
   - Take a screenshot of your **key bindings** in-game.  
   - **Resolution Requirement:** `1366x768`  
   - **File Format:** PNG (Rename it to `bindings.png`).
   - BINDINGS_FILE in overlay.py is mapped to the name of your keybindings.
   - Save it in the same folder as `overlay.py`.  

3. **Install Python:**  
   - Download and install the latest **Python version**.  
   - During installation, **add Python to PATH**.  

4. **Verify Python Installation:**  
   - Open Command Prompt and run:  
     ```sh
     python --version
     ```
   
5. **Install Dependencies:**  
   - Open Command Prompt and run:  
     ```sh
     pip3 install numpy opencv-python pillow pynput
     ```
   - Press `Y` when prompted to confirm installation.  

#### **2️⃣ Running the Overlay**
6. **Run Command Prompt as Administrator:**  
   - Press the **Windows key**, search for **Command Prompt**, right-click it, and select **Run as administrator**.  

7. **Navigate to the Overlay Folder:**  
   - In the admin Command Prompt, change directory (`cd`) to the folder containing `overlay.py`.  
   - Example (if saved in Downloads):  
     ```sh
     cd C:\Users\%USERNAME%\Downloads
     ```

8. **Run the Overlay:**  
   ```sh
   python3 overlay.py
