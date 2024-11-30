#!/bin/bash

# Change to the /opt directory
cd /opt

# Clone the EvilPiG repository
git clone https://github.com/Pasch0/EvilPiG

cd EvilPiG

# Update the package list and install necessary packages
apt update -y

#apt install linux-firmware -y

apt install -y curl gcc git m4 autoconf htop python3-pip \
    python3-setuptools python3-bluez python3-pydbus python3-psutil \
    psutils python3-dbus reaver tshark hashcat hcxdumptool macchanger \
    tmux speedtest-cli autoconf automake libtool pkg-config m4 \
    autoconf-archive libcurl4-openssl-dev libpcap-dev libssl-dev \
    build-essential sqlite3 libsqlite3-dev pixiewps python3-scapy \
    neofetch libncurses5-dev libgdbm-dev libbz2-dev \
    libblas-dev libatlas-base-dev libpq-dev libffi-dev zlib1g-dev \
    libxml2-dev libxslt1-dev lm-sensors dirmngr sqlcipher libnl-3-dev \
    libnl-genl-3-dev ethtool shtool rfkill zlib1g-dev libpython3-dev

# Copy configuration files
cp ./wpa_supplicant.conf /etc/wpa_supplicant/wpa_supplicant.conf
cp ./wpa_supplicant.conf /etc/wpa_supplicant/wpa_supplicant-attack.conf
cp ./interfaces /etc/network/interfaces
cp ./evilpig.service /etc/systemd/system/
cp ./hci-eye.service /etc/systemd/system/

# Install Python packages
pip install scapy psycopg2-binary pysqlcipher3 testresources --break-system-packages

# Install Aircrack-ng
wget https://download.aircrack-ng.org/aircrack-ng-1.7.tar.gz
tar -zxvf aircrack-ng-1.7.tar.gz
cd aircrack-ng-1.7
autoreconf -i
./configure --with-experimental
make
make install
ldconfig
cd ../
rm -rf aircrack-ng-1.7

# Install Hcxtools
git clone https://github.com/ZerBea/hcxtools.git
cd hcxtools
make -j $(nproc)
make install
cd ../
rm -rf hcxtools

# Install Hcxdumptool
git clone https://github.com/ZerBea/hcxdumptool.git
cd hcxdumptool
make
make install
cd ../
rm -rf hcxdumptool

# Install Cowpatty
git clone https://github.com/joswr1ght/cowpatty.git
cd cowpatty
make
make install
cd ../
rm -rf cowpatty

# Install Bully
git clone https://github.com/aanarchyy/bully.git
cd bully/src
make
make install
cd ../../
rm -rf bully

# Install Wifite3
git clone https://github.com/4k4xs4pH1r3/wifite3

# Reload systemd daemon and enable/start the evilpig service
systemctl daemon-reload
systemctl enable evilpig
systemctl start evilpig

systemctl enable hci-eye
systemctl start hci-eye

# Restart networking service
systemctl restart networking

# Install Streamlit and Bleak
python3 -m pip install streamlit --break-system-packages

# Create a symbolic link for hcxpcaptool
sudo ln -s $(which hcxpcapngtool) /usr/local/bin/hcxpcaptool

curl -fsSL https://tailscale.com/install.sh | sh