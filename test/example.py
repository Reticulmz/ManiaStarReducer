import sys
sys.path.append("..")

from deflate import fix_star_rating

# The beatmap that you are checking and fixing inflated patterns for
beatmap_path = "./gravity.osu"

# The new difficulty name (Version) of the beatmap
new_difficulty_name = "star rating fix"

# The output file path of the beatmap
output_path = "./gravity_fixed.osu"

fix_star_rating(beatmap_path, new_difficulty_name, output_path)