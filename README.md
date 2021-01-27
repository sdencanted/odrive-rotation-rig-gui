# ODriveTool GUI
A python script that provides a GUI and logging for an Odrive-based rotation rig

## Getting Started

### Installation
1. [Install ODriveTool](https://docs.odriverobotics.com/) on the host computer that will be directly controlling the ODrive.
2. Clone the repository on both the remote computer and the host computer.
`git clone https://github.com/sdencanted/odrive-rotation-rig-gui.git`

### Setting up the ODrive
1. Connect the ODrive and open `odrivetool` 
2. Enable calibration and close loop control on start-up.
```
odrv0.axis1.config.startup_motor_calibration=True
odrv0.axis1.config.startup_encoder_index_search=True
odrv0.axis1.config.startup_encoder_offset_calibration=True
odrv0.axis1.config.startup_closed_loop_control=True
odrv0.save_configuration()
odrv0.reboot()
```   
3. Exit `odrivetool` by pressing `CTRL`+`D` and pressing `y`.
### Running the script on a standalone computer
1. Run the script.
```
cd odrive-rotation-rig-gui
python3 odrv_standalone.py
```
### Running the script with a client and server
1. Server refers to the computer connected to the ODrive, and client refers to the computer that will display the GUI.
2. Ensure both the server and client computers have OdriveTool installed.
3. Run the server script.
`python3 odrv_server.py`
4. Run the client script with the IP address of the server as the argument. eg. `192.168.1.103`
`python3 odrv_client.py 192.168.1.103`

### Data
Time and rotational velocity ( in rotations per second ) will be output as a pickle when the exit button is pressed. It can be loaded as a list using the `pickle` module.
`pickle.load( open( "file.pickle", "rb" ) )`

### Controlling the Odrive manually
1. Launch `odrivetool`
2. #### Commands ( run in order)
    Limit rotational velocity ( in rotations per second )
    `odrv0.axis.controller.config.vel_limit = 6`
    
    Change the mode to velocity control
    `axis.controller.config.control_mode = CONTROL_MODE_VELOCITY_CONTROL`
    
    Change the rotational acceleration ( in rotations per second squared)
    `axis.controller.config.vel_ramp_rate = 2`
    
    Change the input mode to velocity ramped
    `axis.controller.config.input_mode = INPUT_MODE_VEL_RAMP`
    
    Enter the desired rotational velocity. ( limited by velocity limit )
    `axis.controller.input_vel = 5`
