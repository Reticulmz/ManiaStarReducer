# ManiaStarReducer
Takes an osu!mania beatmap and fixes any found star rating inflated patterns.

When calculating star rating, osu!mania considers the density of notes to be a huge factor of difficulty. However, this can easily be abused by short and close LN (Mania Hold) patterns. It does not correctly reflect the difficulty of the map, causing the star rating to be heavily inflated.

**What exactly do you consider an inflated pattern?**

* The start times of LNs are too close together, but not directly on top of each other. In this case, if the player is hitting LNs on 1/8th notes, consider that partially inflated.
* If the LNs have a small and less than 1/4th per beat hold time.

If both of these cases are true, it will replace the current LN patterns with a normal note, thus making it the same beatmap playability wise, while reducing the star rating to its **REAL** value

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

# Media
Here, you can see exactly what it does. 

* The image on the **left** is a pattern that **inflates** the star rating of: **14.46 Stars**
* The image on the **right** is a pattern that plays exactly the same but **deflates** the star rating to: **8.77 Stars**

![alt text](https://juicy.eggplants.org/5vs435.png)
![alt text](https://juicy.eggplants.org/it32d1.png)

# Data
The following PP & difficulty calculations are from semyon422's [omppc](https://github.com/semyon422/omppc).

**First Beatmap Data (Left Image)**
```
Mods info
 modsString   none
 scoreMult    1
 timeRate     1
 odMult       1
Beatmap info:
 starRate     14.464003375837
 noteCount    1207
 scaled OD    0
 real OD      0
 scaled HP    6
 real HP      6
Play info
 scaled score 1000000
 real score   1000000.0
 accuracy     100.0
 strainValue  6526.3997063184
 accValue     10.850884109379
 PP           7184.7614017897
```

**Second Beatmap Data (Right Image)**
```
Mods info
 modsString   none
 scoreMult    1
 timeRate     1
 odMult       1
Beatmap info:
 starRate     8.7766056821245
 noteCount    1207
 scaled OD    0.0
 real OD      0.0
 scaled HP    6.0
 real HP      6.0
Play info
 scaled score 1000000
 real score   1000000.0
 accuracy     100.0
 strainValue  1445.1466416127
 accValue     10.850884109379
 PP           1596.3129606526
```

# MIT
All the code in this repository is licensed under [MIT](https://github.com/Swan/ManiaStarReducer/blob/master/LICENSE)
