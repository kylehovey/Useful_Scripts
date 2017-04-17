# Generalized Backup Script
# See backup.json (in same dir) for config options
# Author: Kyle Hovey (https://github.com/kylehovey)

import json, zipfile, os
from datetime import datetime

# Load a JSON file into a python variable
def load_json(save_file):
	state = open(save_file, "r")
	contents = json.load(state)
	state.close()

	return contents

# Load a JSON file into a python variable
def save_json(save_file, contents):
	out = open(save_file, "w")
	json.dump(contents, out)
	out.close()

# ZIP FUNCTIONALITY FROM http://stackoverflow.com/a/1855118/5457490 #
# Zip a directory into a zip file handler (zipfile.ZipFile)
def zip_dir(path, zipf):
    for root, dirs, files in os.walk(path):
        for file in files:
            zipf.write(os.path.join(root, file))

if __name__ == "__main__":
    # Get config
    config = load_json("backup.json")
    print "Loaded Config"

    # Get timestamp
    tstamp = datetime.now().strftime("-%m-%Y-%H:%M")

    # Unpack options
    storage_dir = os.path.expanduser(config["storage_dir"])
    name = storage_dir + config["label"] + tstamp + ".zip"
    files = config["files"]
    directories = config["directories"]
    print "Built Options"

    # Change to storage dir (files for backup)
    os.chdir(storage_dir)
    print "Beginning Backup"

    # Open zipfile
    with zipfile.ZipFile(name, 'w') as zipf:
        print "Compressing Files"
        for file in files:
            zipf.write(file)
        for directory in directories:
            zip_dir(directory, zipf)

    # Close the zip file
    zipf.close()
    print "Backup completed."
    print "File created: {}".format(name) 
