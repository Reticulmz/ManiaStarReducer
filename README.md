# ManiaStarReducer
Takes an osu!mania beatmap and fixes any found star rating inflated patterns.

# Example
```py
from deflate import fix_star_rating

# The beatmap that you are checking and fixing inflated patterns for
beatmap_path = "./Chip Skylark - Shiny Teeth (Of Mass M Remix) (Swan) [Vibro Teeth].osu"

# The new difficulty name (Version) of the beatmap
new_difficulty_name = "fixed"

# The output file path of the beatmap
output_path = "./Chip Skylark - Shiny Teeth (Of Mass M Remix) (Swan) [fixed].osu"

fix_star_rating(beatmap_path, new_difficulty_name, output_path)
```

