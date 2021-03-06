#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import subprocess
import time
import sys
from files.tools.colorify import colorify


def terminal_size():
	import fcntl
	import termios
	import struct
	h, w, hp, wp = struct.unpack('HHHH', fcntl.ioctl(
		0, termios.TIOCGWINSZ, struct.pack('HHHH', 0, 0, 0, 0)))
	return w, h


print("\033[2J" + "\033[H", end="")

for x in range(terminal_size()[0]):
	print("\u2500", end="")

print(colorify("cyan", True, "screenmanager-setup / setup"))

for x in range(terminal_size()[0]):
	print("\u2500", end="")
print(colorify("green_bold", True, "Nachfolgend wird Ihr Raspberry Pi aktualisiert. \nAußerdem wird Ihr System konfiguriert und wichtige Programme werden installiert.\nDies dauert in der Regel einige Minuten (3-15). Am Ende wird der Raspberry Pi neugestartet."))
input("Zum Fortfahren drücken Sie bitte die Eingabetaste, zum Abbrechen Strg + C...")
print("Bitte warten...\n")

returncode = 0

commands_to_run = [
	["sudo", "apt-get", "update", "-qq"],
	["sudo", "apt-get", "dist-upgrade", "-qq"],
	["sudo", "timedatectl", "set-timezone", "Europe/Berlin"],
	["sudo", "apt-get", "install", "cec-utils", "libcec-dev", "python3-pip", "-qq"],
	["pip3", "install", "python-crontab", "cec"],
	["sudo", "apt", "autoremove", "-y"]
]

for index, command in enumerate(commands_to_run, start=1):
	if returncode == 0:
		cmd = subprocess.run(command)
		returncode = cmd.returncode
		print(colorify("magenta_bold", True, "Schritt " + str(index) +
                 "/" + str(len(commands_to_run)) + " abgeschlossen."))

if returncode == 0:
	print(colorify("green_bold", True,
                "Raspberry Pi wurde erfolgreich eingerichtet. Starte in 5 Sekunden neu..."))
	subprocess.run(["sudo", "reboot"])
else:
	print(returncode)
	sys.exit(colorify("red_bold", True,
                   "Es ist mindestens ein Fehler aufgetreten und die Einrichtung wurde nicht abgeschlossen."))
