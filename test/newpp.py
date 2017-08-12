# This example file will go through a Ripple user's scores and will check and compare their new performance points
# with all the maps deflated. In order to run this, you'll need semyon422's omppc. https://github.com/semyon422/omppc
import sys
import os
import errno
import shutil
import subprocess
from pprint import pprint
import json, requests
sys.path.append("..")
from deflate import fix_star_rating


ripple_username = sys.argv[1]
url = 'http://ripple.moe/api/v1/users/scores/best?name={0}&mode=3'.format(ripple_username)
resp = requests.get(url=url)

data = json.loads(resp.text)
if data['scores'] == None:
    print("Could not find data for user: {0}".format(ripple_username))
    sys.exit()
else:
    print("Found scores for user: {0}".format(ripple_username))

# Create a directory that will store the .osu files
try:
    os.makedirs("./osu_files")
except OSError as e:
    if e.errno != errno.EEXIST:
        raise

# Download all .osu files for beatmap
print("Downloading all beatmaps...")
for score in data['scores']:
    # Download beatmap .osu file
    beatmap_id = score['beatmap']['beatmap_id']
    print("{0}: " .format(beatmap_id), end="")
    url = "https://osu.ppy.sh/osu/{0}".format(beatmap_id)
    resp = requests.get(url=url)

    
    # Deflate current beatmap
    beatmap_path = "./osu_files/{0}.osu".format(beatmap_id)
    f = open(beatmap_path, 'w')
    f.write(resp.text)
    fix_star_rating(beatmap_path, "fixed", beatmap_path)
    f.close()

    # Get Deflated Beatmap Data
    try: 
        result = subprocess.check_output([
            'lua', 'omppc.lua', 
            '--beatmap', beatmap_path,
            '--score', str(score['score']), 
            '--accuracy', "%.2f" % score['accuracy'],
            '--mods', 'none'
            '--debug',
            ])

        # Replace all weird characters in string and add it to the score object
        result = result.decode("utf-8")
        result = result.replace("\n", "")
        result = result.replace("\'", "")
        result = float(result)
        score['new_pp'] = float(result)
    except:
        score['new_pp'] = 0
        print("Beatmap: " + str(beatmap_id) + " could not be checked. Is it deleted from osu?")
        continue

# Compare total pp vs new pp
old_total = 0
new_total = 0
for score in data['scores']:
    old_total += score['pp']
    new_total += score['new_pp']

print("\n\n-----------------------------")
print("Deflated Top 50 Performance Data")
print()
print("User: {0}".format(ripple_username))
print("Old Total: " + str(old_total) + "pp")
print("Deflated Total: " + str(new_total) + "pp")
print("---------------------------------")

# Delete the osu_files directory
shutil.rmtree(os.getcwd() + "/osu_files")