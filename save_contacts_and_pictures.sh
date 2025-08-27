#!/bin/bash

# Start the first emulator
$ANDROID_HOME/emulator/emulator -avd phone1 -no-window -no-audio -gpu swiftshader_indirect &
# Start the second emulator
$ANDROID_HOME/emulator/emulator -avd phone2 -no-window -no-audio -gpu swiftshader_indirect &

# Wait for emulators to boot
sleep 30

# Save contacts and images to phone1
adb -s emulator-5554 wait-for-device
adb -s emulator-5554 shell content insert --uri content://contacts/people --bind name:s:1_Pervy --bind phone:s:9640110555
adb -s emulator-5554 shell content insert --uri content://contacts/people --bind name:s:2_Vtoroy --bind phone:s:9640220555
adb -s emulator-5554 shell content insert --uri content://contacts/people --bind name:s:3_Treti --bind phone:s:9640330555
adb -s emulator-5554 push /root/pictures/picture_1.png /sdcard/Pictures/
adb -s emulator-5554 push /root/pictures/picture_2.png /sdcard/Pictures/

# Save contacts and images to phone2
adb -s emulator-5556 wait-for-device
adb -s emulator-5556 shell content insert --uri content://contacts/people --bind name:s:1_Pervy --bind phone:s:9640110555
adb -s emulator-5556 shell content insert --uri content://contacts/people --bind name:s:2_Vtoroy --bind phone:s:9640220555
adb -s emulator-5556 shell content insert --uri content://contacts/people --bind name:s:3_Treti --bind phone:s:9640330555
adb -s emulator-5556 push /root/pictures/picture_1.png /sdcard/Pictures/
adb -s emulator-5556 push /root/pictures/picture_2.png /sdcard/Pictures/

# Start Appium
appium --relaxed-security &
tail -f /dev/null