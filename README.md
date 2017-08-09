# ManiaStarReducer
Takes an osu!mania beatmap and fixes any found star rating inflated patterns.

# Example
```py
from deflate import fix_star_rating

beatmap_path = "./Chip Skylark - Shiny Teeth (Of Mass M Remix) (Swan) [Vibro Teeth].osu"
new_difficulty_name = "fixed"
output_path = "./Chip Skylark - Shiny Teeth (Of Mass M Remix) (Swan) [fixed].osu"

fix_star_rating(beatmap_path, new_difficulty_name, output_path)
```

