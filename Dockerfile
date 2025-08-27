# Base image with Android tools
FROM ubuntu:22.04

# Install dependencies
RUN apt-get update && apt-get install -y \
    openjdk-11-jdk \
    curl \
    wget \
    unzip \
    nodejs \
    npm \
    libgl1-mesa-glx \
    libpulse0

# Set environment variables for Android SDK
ENV ANDROID_HOME=/opt/android-sdk
ENV PATH="$ANDROID_HOME/emulator:$ANDROID_HOME/tools:$ANDROID_HOME/tools/bin:$ANDROID_HOME/platform-tools:$PATH"

# Install Android SDK and Emulator
RUN mkdir -p $ANDROID_HOME && \
    curl -o sdk-tools.zip https://dl.google.com/android/repository/commandlinetools-linux-9477386_latest.zip && \
    unzip sdk-tools.zip -d $ANDROID_HOME && \
    rm sdk-tools.zip && \
    yes | $ANDROID_HOME/cmdline-tools/bin/sdkmanager --sdk_root=$ANDROID_HOME "platform-tools" "platforms;android-34" "system-images;android-34;google_apis_playstore;x86_64" "emulator"

# Accept licenses
RUN yes | $ANDROID_HOME/cmdline-tools/bin/sdkmanager --licenses

# Install Appium
RUN npm install -g appium

# Base image for Android AVD
FROM budtmo/docker-android-x86-14.0

# Set environment variables for the Android SDK
ENV ANDROID_SDK_ROOT=/opt/android-sdk-linux

# Copy AVD configuration files (from the test project root)
COPY avd_config.ini /root/.android/avd/custom_device_1.avd/config.ini
COPY avd_config_2.ini /root/.android/avd/custom_device_2.avd/config.ini

# Create the first AVD (custom_device_1)
RUN echo "no" | avdmanager create avd \
    -n custom_device_1 \
    -k "system-images;android-34;google_apis_playstore;x86_64" \
    --device "pixel_9_1" && \
    mkdir -p /root/.android/avd/custom_device_1.avd && \
    cp /root/.android/avd/custom_device_1.avd/config.ini /root/.android/avd/custom_device_1.avd/config.ini

# Create the second AVD (custom_device_2)
RUN echo "no" | avdmanager create avd \
    -n custom_device_2 \
    -k "system-images;android-34;google_apis_playstore;x86_64" \
    --device "pixel_9_2" && \
    mkdir -p /root/.android/avd/custom_device_2.avd && \
    cp /root/.android/avd/custom_device_2.avd/config.ini /root/.android/avd/custom_device_2.avd

# Copy additional resources (pictures, contacts, etc.)
COPY src/pictures/picture_1.png /root/pictures/picture_1.png
COPY src/pictures/picture_2.png /root/pictures/picture_2.png

# Expose ports for Appium and emulator communication
EXPOSE 5554 5556 4723

# Start script (you can add your script to save contacts/pictures)
COPY save_contacts_and_pictures.sh /root/save_contacts_and_pictures.sh
RUN chmod +x /root/save_contacts_and_pictures.sh

# Start the script when the container is run
CMD ["bash", "/root/save_contacts_and_pictures.sh"]
