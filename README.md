# web_insp.py

Program name: Web Page Inspector
Program Creator: promontorycoder

Purpose of Program: 
    Assist with examination of web site data.
            
    Creator used to help with python and tkinter learning.

Credits:
    Online world for all of the training and information the author has
    received.        

________________________________________________________________________________

# REQUIREMENTS FOR UBUNTU 20.04
________________________________________________________________________________

1. python3:
    sudo apt-get install -y python3
    
2. tkinter: 
    sudo apt-get install -y python3-tk
    
3. PIL:
    python3 -m pip install Pillow

________________________________________________________________________________

# GIT CLONE LINK
________________________________________________________________________________

To git clone into the repository folder, enter the following command into 
Terminal after navigating from within Terminal to the folder you'd like the
program folder to be cloned to.

git clone https://github.com/promontorycoder/web_insp.git
________________________________________________________________________________

# INSTALLATION INSTRUCTIONS FOR UBUNTU 20.04
________________________________________________________________________________

#### Step 1: Acquire program files
    Copy files via git clone or other method to chosen install folder

#### Step 2: Make program files executable
    Open gnome-terminal and navigate to folder with downloaded program files
    Enter the following commands into gnome-terminal:
        chmod +x web_insp.py
        chmod +x web_insp_start.desktop
        
#### Step 3: Edit files to reflect your directory structure
- Open csv_insp_start.desktop into text editor and change lines 5, 6 and 7 to 
match your file structure
    - Save and exit file
    
#### Step 4: Install tkinter if you do not already have it installed.
    Open gnome-terminal and execute the following commands:
* sudo apt-get install -y python3-tk
* python3 -m pip install Pillow
        
        
#### Step 5: Copy .desktop file to /usr/share/applications
    Open gnome-terminal and enter the following command:
* sudo cp web_insp.desktop /usr/share/applications
________________________________________________________________________________

![Screenshot](web_insp_scrn01.png)
