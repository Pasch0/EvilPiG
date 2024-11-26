#!/bin/bash

cd /opt

git clone https://github.com/Pasch0/EvilPiG

cd /opt/EvilPiG

## Aqui vai o Git Clone quando estiver no git

apt update -y

apt install curl gcc git linux-firmware m4 libtool automake autoconf htop libcurl4-openssl-dev -y

#apt install wpasupplicant bluez-tools bluez-hcidump libbluetooth-dev \
#                    git gcc python3-pip python3-setuptools python3-bluez \
#                    python3-pydbus htop python3-psutil psutils python3-dbus \
#                    linux-firmware reaver tshark hashcat hcxdumptool \
#                    macchanger tmux speedtest-cli autoconf automake libtool \
#                    pkg-config m4 autoconf-archive libcurl4-openssl-dev \
#                    libpcap-dev libssl-dev build-essential libpcap-dev \
#                    sqlite3 libsqlite3-dev pixiewps python3-scapy python3.12-venv -y

cd /opt/EvilPiG/

cp ./wpa_supplicant.conf /etc/wpa_supplicant/wpa_supplicant.conf
cp ./wpa_supplicant.conf /etc/wpa_supplicant/wpa_supplicant-attack.conf

cp ./interfaces /etc/network/interfaces

cp ./evilpig.service /etc/systemd/system/

apt install build-essential autoconf automake libtool pkg-config libnl-3-dev libnl-genl-3-dev libssl-dev ethtool shtool rfkill zlib1g-dev libpcap-dev libsqlite3-dev libpython3-dev -y

python3 -m pip install streamlit bleak --break-system-packages

### Aircrack-ng
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

## Hcxtools
git clone https://github.com/ZerBea/hcxtools.git
cd hcxtools
make -j $(nproc)
make install
cd ../
rm -rf hcxtools

#apt update -y && apt install dirmngr sqlcipher aptitude -y && apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 7638D0442B90D010 04EE7237B7D453EC EF0F382A1A7B6500 &&>
#v libncurses5-dev libgdbm-dev libbz2-dev libssl-dev libdb-dev libssl-dev build-essential libssl-dev libblas-dev libatlas-base-dev libpq-dev libffi-
#dev zlib1g-dev libxml2-dev libxslt1-dev zlib1g-dev libpcap-dev libpcap-dev -y && pip install psycopg2-binary pysqlcipher3 psycopg2 testresources &&
# pip install --upgrade wheel pip install scapy && aptitude install && pip list --outdated && pip install --upgrade wheel && pip install --upgrade s
#etuptools && sudo apt-get update -y && sudo apt-get install python2-dev libssl-dev libpcap-dev python3-scapy -y && cd /usr/share/ && git clone http
#s://github.com/JPaulMora/Pyrit.git --depth=1 && sed -i "s/COMPILE_AESNI/COMPILE_AESNIX/" Pyrit/cpyrit/_cpyrit_cpu.c && cd Pyrit && python2 setup.py
# clean && python2 setup.py build && sudo python2 setup.py install && cd .. && pip install psycopg2-binary && pip install psycopg2 && pip install vi
#rtualenvwrapper && aptitude install neofetch git make clang libpcap-dev reaver tshark wireshark aircrack-ng pixiewps libssl-dev libcurl4-openssl-de
#v libpcap0.8-dev libcurl4-doc libidn11-dev libkrb5-dev libldap2-dev librtmp-dev libssh2-1-dev libssl-doc -y && cd /usr/share/ && git clone https://
#github.com/ZerBea/hcxtools.git && cd hcxtools && make && make install && cd /usr/share && git clone https://github.com/ZerBea/hcxdumptool.git  && c
#d hcxdumptool && make && make install && cd /usr/share && git clone https://github.com/joswr1ght/cowpatty.git && cd cowpatty && make && make instal
#l && cd /usr/share && git clone https://github.com/aanarchyy/bully.git && cd bully/src && make && make install && neofetch && cd /usr/share && neof
#etch && cd && pip --version && python --version && sudo ln -s $(which hcxpcapngtool) /usr/local/bin/hcxpcaptool

cd /opt/EvilPiG/

#wifite3
git clone https://github.com/4k4xs4pH1r3/wifite3

systemctl daemon-reload

systemctl enable evilpig
#systemctl enable evilpig-wifi

systemctl start evilpig
#systemctl start evilpig-wifi

systemctl restart networking

### Thanks for WPA Supplicant
### https://wiki.archlinux.org/index.php/WPA_supplicant - Link ficticio
### Thanks for hi_my_name_is_keyboard
### https://github.com/marcnewlin/hi_my_name_is_keyboard