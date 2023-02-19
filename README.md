# Install i2s Mic & Speaker

Installing dependencies
```
sudo apt install -y python3-pip
sudo pip install -y adafruit-python-shell
```

Install audio driver
```
git clone https://github.com/IshantPundir/audio-driver
cd audio-driver
sudo python install.py
```

Test audio driver
```
arecord -D osmos_mic -c2 -r 16000 -f S16_LE -t wav -V mono -v recording.wav
aplay recording.wav

alsamixer # adjust mic volume

arecord -D osmos_mic -c2 -r 16000 -f S16_LE -t wav -V mono -v recording.wav
aplay recording.wav
```

It is important to run arecord before being able to increase its volume inside alsamamixer.
Once we have accessed osmos_mic, we can edit its volume inside alsamixer.
