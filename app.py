import streamlit as st

pages = {
    "Attacks": [
        st.Page("pages/evilpig.py", title="EvilPig"),
        #st.Page("pages/blueducky.py", title="BlueDucky"),
        st.Page("pages/bluetooth-dos.py", title="Bluetooth DoS"),
        st.Page("pages/wifite.py", title="Wifite3"),
        #st.Page("pages/wifiphishing.py", title="Wifi Phishing"),
        st.Page("pages/recon.py", title="Recon Tools"),
        #st.Page("pages/scan.py", title="Vulnerability Scanner"),
        #st.Page("pages/exploitcasts.py", title="Exploit Casts"),
        #st.Page("pages/rokuismine.py", title="Roku_is_mine"),
        #st.Page("pages/433jammer.py", title="433MHz Jammer"),
        #st.Page("pages/fmhijack.py", title="FM Hijack"),
    ],
    "Administration": [
        st.Page("pages/wificonfig.py", title="wpa_supplicant"),
        st.Page("pages/shell.py", title="Shell"),
    ],
}

pg = st.navigation(pages)
pg.run()