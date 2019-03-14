#!/usr/bin/env python3

import fileinput
import os
import glob
import sys
import subprocess
from shutil import copyfile

# Parse arguments
def query_user_data (data = {}):
    cyanColor = "\033[36m"
    resetColor = "\033[39m"

    for key, value in data.items ():
        print ("> {}{}:{}".format (cyanColor, value, resetColor), end=" ")
        user_input = input ()
        data [key] = user_input

    return data

# Grab all files
def get_files (exclude = []):
    current_path = os.path.dirname(os.path.abspath(__file__))
    files_found = []

    for (parent, subdirs, files) in os.walk(current_path, topdown=True):
        subdirs[:] = [d for d in subdirs if d not in exclude]
        files[:] = [f for f in files if f not in exclude]
        files_found.extend (map (lambda x: os.path.join (parent, x), files))

    return files_found

# Replace file contents
def replace_in_file (filename, text, replacement_text):
    with fileinput.FileInput(filename, inplace=True) as lines:
        for line in lines:
            print(line.replace(text, replacement_text), end='')

# Print steps
def step (number, text, end="..."):
    grayColor = "\033[90m"
    resetColor = "\033[39m"
    startText = ("\n" if number>1 else "")
    print ("{}{}{}. {}{}{}".format (startText, grayColor, number, text, end, resetColor))

# Copy env file
step(1, "Creating .env file")
current_path = os.path.dirname(os.path.abspath(__file__))
copyfile(os.path.join (current_path, ".env.example"), os.path.join (current_path, ".env"))

# Insert template data
step (2, "Filling template data")

# Grab all files
files = get_files (exclude=[
    ".git",
    "install.py",
    "README.md",
    ".env.example"
])

# Grab all necessary data
params = query_user_data(data={
    "name": "Name of this project (lowercase & dashed)",
    "namespace": "PHP project namespace",
    "author_name": "Name of the author",
    "author_email": "EMail address of the author",
    "db_host": "Database host",
    "db_user": "Database user",
    "db_pass": "Database password",
    "db_name": "Database name"
})

# Replace variables
for param, value in params.items():
    text = ("{{" + param + "}}")
    for file in files:
        replace_in_file (filename=file, text=text, replacement_text=value)

# Install composer dependencies
step (3, "Installing composer dependencies")
subprocess.check_output(["composer", "install"])

# Install NPM dependencies
step (4, "Installing NPM dependencies")
subprocess.check_output(["npm", "install"])

# Done
step (5, "You're all set!\nPlease verify the integrity of the created system before proceeding.\nRun 'npm run watch' from here.", end="")

# Self-destruct
os.remove (sys.argv [0])