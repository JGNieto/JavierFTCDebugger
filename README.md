# Javier's Debugging for FTC

Developed by Javier García Nieto for The OHM Raiders (#11468)

The purpose of this simple program is to serve as a screen to monitor the location of an FTC robot in the field during testing. It receives information through TCP and displays it on the screen.

Note: only tested on a Control Hub.

## Set up your laptop:
- Install [Anaconda](https://docs.anaconda.com/anaconda/install/index.html)
- Clone this repository `git clone https://github.com/JGNieto/JavierFTCDebugger.git && cd JavierFTCDebugger`
- Create the environment: `conda env create --file=environment.yml`
- Activate environment: `conda activate javierdebug`
- Connect to your robot's wifi network.
- You need to set up a custom IP address for your laptop on the robot's network. This depends on your device and might be done differently in the future, but some useful tutorials can be: [windows](https://www.trendnet.com/press/resource-library/how-to-set-static-ip-address) or [mac](https://www.macinstruct.com/tutorials/how-to-set-a-static-ip-address-on-a-mac/). I recommend you set it to our default, `192.168.43.97`, but you may choose whichever you like.
- If you have set an IP address different than `192.168.43.97`, change the HOST variable in screen.py to match (the one that says "change this").
- Reboot your robot and laptop, for good measure. This is not strictly necessary but may save you some headaches.
- You may need to run `conda activate javierdebug` again after the reboot, or even if you close the terminal and open it again.
- Run `python3 main.py` in the directory where you cloned this repository.

## Set up your code:
- Add the class DebuggingClient.java (provided in this repository) to your project. You may need to add a package field at the top of the file as specified.
- We assume that you have written code that updates the position of the robot one way or another (maybe using dead wheel odometry, the images on the field, ORB-SLAM or something else). At the end of that code, you need to add the following:
```java
// We assume that your code declares three integers: x, y and heading.
// You may need to adapt the following code to your variable names.
DebuggingClient debug = DebuggingClient.getInstance();
debug.setX(x);
debug.setY(y);
debug.setHeading(heading);
debug.update();
```
Note: this app assumes you use the [official coordinate system](https://github.com/FIRST-Tech-Challenge/FtcRobotController/blob/master/FtcRobotController/src/main/java/org/firstinspires/ftc/robotcontroller/external/samples/FTC_FieldCoordinateSystemDefinition.pdf)
- The DebuggingClient class automatically handles cases were new information comes in before the last one has finished sending.

<!--
TODO
## How it works
The laptop is on the same Wi-Fi network as the robot controller, which allows for communication.
-->