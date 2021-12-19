# reference
# https://matthewragan.com/2019/08/14/touchdesigner-python-and-the-subprocess-module/
#
import time
import sys
import socket
from argparse import ArgumentParser
import numpy as np
import librosa
import matplotlib.pyplot as plt

duration = 30
x_sr = 200
bpm_min, bpm_max = 60, 240

 
def msg_to_bytes(msg):
    return str(msg).encode('utf-8')

# reference
# https://www.wizard-notes.com/entry/music-analysis/compute-bpm
#
def detectBpm(port, filepath):
    upd_ip = "127.0.0.1"
    udp_port = int(port)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
 
    y, sr = librosa.load(filepath, offset=38, duration=duration, mono=True)
    x = np.abs(librosa.resample(y, sr, x_sr)) ** 2
    x_len = len(x)

    M = np.zeros((bpm_max, x_len), dtype=np.complex)
    for bpm in range(bpm_min, bpm_max): 
        thete = 2 * np.pi * (bpm/60) * (np.arange(0, x_len) / x_sr)
        M[bpm] = np.exp(-1j * thete)

    x_bpm = np.abs(np.dot(M, x))

    bpm = np.argmax(x_bpm)

    sock.sendto(msg_to_bytes(bpm), (upd_ip, udp_port))

if __name__ == '__main__':
    parser = ArgumentParser(description='Detect BPM')
    parser.add_argument("-p", "--port", dest="port", help="UDP port", required=True, default=1234)
    parser.add_argument("-f", "--filepath", dest="filepath", help="filepath", required=True, default="bpm.wav")
    args = parser.parse_args()
 
    detectBpm(args.port, args.filepath)
    pass

#example
#python C:\project-C\DJSystem\scripts\cmd_line_python_udp_msg_args.py -p="7000" -f="C:/project-C/DJSystem/music/12008909_Kaleidoscope_Original_Mix.wav"