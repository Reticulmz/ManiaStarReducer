# ManiaStarReducer
Takes an osu!mania beatmap and fixes any found star rating inflated patterns.

When calculating star rating, osu!mania considers the density of notes to be a huge factor of difficulty. However, this can easily be abused by short and close LN (Mania Hold) patterns. It does not correctly reflect the difficulty of the map, causing the star rating and performance points to be heavily inflated.

**What exactly do you consider an inflated pattern?**

* The start times of two LNs are too close together, but not directly on top of each other. For example, if the player has to hit LNs on 1/8th notes, consider that inflated.
* If the two LNs have a less than 1/4th beat hold time. (LN can be tapped instead of held to get a 300)

If one or more of these cases are true, it will replace the current LN patterns with a normal note, thus making it the same beatmap playability wise, while reducing the star rating to its **REAL** value

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

* The image on the **left** is a pattern that **inflates** the star rating to: **14.46 Stars | 7184 PP**
* The image on the **right** is a pattern that plays exactly the same but **deflates** the star rating to: **8.77 Stars | 1596 PP**

![alt text](https://juicy.eggplants.org/5vs435.png)
![alt text](https://juicy.eggplants.org/it32d1.png)

# Data
The following PP & difficulty calculations are from semyon422's [omppc](https://github.com/semyon422/omppc).

**Original Beatmap Data (Left Image)**
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

**Fixed Beatmap Data (Right Image)**
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

**New Total PP**
Since [Ripple](https://ripple.moe), an osu! private server has an issue with ranked inflated vibro maps, here's a comparison between a few top player's performance points total for the old maps vs. the deflated ones:

Statistically, the amount of deflated PP

[arpia97](https://ripple.moe/u/3313) #3 (Vibro Player)
```
-----------------------------
Deflated Top 50 Performance Data

User: arpia97
Old Total: 265,906.65pp
Deflated Total: 98,133.10pp
---------------------------------
```

[Jakads](https://ripple.moe/u/3325) #26 (7k Player)
```
-----------------------------
Deflated Top 50 Performance Data

User: Jakads
Old Total: 162,926.55pp
Deflated Total: 94,057.14pp
---------------------------------
```

[Swan](https://ripple.moe/u/1298) #18 (Vibro Player)
```
-----------------------------
Deflated Top 50 Performance Data

User: Swan
Old Total: 177,014.69pp
Deflated Total: 64,281.80pp
---------------------------------
```


# MIT
All the code in this repository is licensed under [MIT](https://github.com/Swan/ManiaStarReducer/blob/master/LICENSE)
