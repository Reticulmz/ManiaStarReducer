# beatmap.py
# Parses a mania .osu file and returns an object of the beatmap class
# from pprint import pprint
import operator
import textwrap

class Beatmap(object):
    def __init__(self, beatmap_path):
        self.file_format = None

        # [General]
        self.audio_file_name = None
        self.audio_lead_in = None
        self.preview_time = None
        self.countdown = None
        self.sample_set = None
        self.stack_leniency = None
        self.mode = None
        self.letterbox_in_breaks = None
        self.special_style = None
        self.widescreen_storyboard = None

        # [Editor]
        self.bookmarks = []
        self.distance_spacing = None
        self.beat_divisor = None
        self.grid_size = None
        self.timeline_zoom = None

        # [Metadata]
        self.title = None
        self.title_unicode = None
        self.artist = None
        self.artist_unicode = None
        self.creator = None
        self.version = None
        self.source = None
        self.tags = []
        self.beatmap_id = None
        self.beatmap_set_id = None

        # [Difficulty]
        self.hp_drain_rate = None
        self.circle_size = None
        self.overall_difficulty = None
        self.approach_rate = None
        self.slider_multiplier = None
        self.slider_tick_rate = None

        # [Events]
        # Sigh, who even uses storyboards - I'll do this later.
        self.events = []

        # [TimingPoints]
        self.timing_points = []

        # [HitObjects]
        self.hit_objects = []

        # Parse the beatmap
        self.parse_beatmap(beatmap_path)

    # Responsible for parsing a single beatmap
    def parse_beatmap(self, beatmap_path):
        with open(beatmap_path) as f:
            # This will keep track of which section of the file we are on, while reading the file line by line
            file_section = None

            for line in f:
                line = line.strip()

                # Get osu! file format
                if line.startswith("osu file format"):
                    self.file_format = int(line.split("v")[1])
                
                # Does python not have a switch? I don't usually work with this shit, so meme.
                if line.startswith("[General]"):
                    file_section = "[General]"
                elif line.startswith("[Editor]"):
                    file_section = "[Editor]"
                elif line.startswith("[Metadata]"):
                    file_section = "[Metadata]"
                elif line.startswith("[Difficulty]"):
                    file_section = "[Difficulty]"
                elif line.startswith("[Events]"):
                    file_section = "[Events]"
                elif line.startswith("[TimingPoints]"):
                    file_section = "[TimingPoints]"
                elif line.startswith("[HitObjects]"):
                    file_section = "[HitObjects]"
                elif line.startswith("[Colours]"):
                    file_section = "[Colours]"

                # Parse [General] Beatmap Data
                if file_section == "[General]":
                    if line.startswith("AudioFilename"):
                        self.audio_file_name = self.parse_string(line)
                    elif line.startswith("AudioLeadIn"):
                        self.audio_lead_in = self.parse_int(line)
                    elif line.startswith("PreviewTime"):
                        self.preview_time = self.parse_int(line)
                    elif line.startswith("Countdown"):
                        self.countdown = self.parse_int(line)
                    elif line.startswith("SampleSet"):
                        self.sample_set = self.parse_string(line)
                    elif line.startswith("StackLeniency"):
                        self.stack_leniency = self.parse_float(line)
                    elif line.startswith("Mode"):
                        self.mode = self.parse_int(line)
                    elif line.startswith("LetterboxInBreaks"):
                        self.letterbox_in_breaks = self.parse_int(line)
                    elif line.startswith("SpecialStyle"):
                        self.special_style = self.parse_int(line)
                    elif line.startswith("WidescreenStoryboard"):
                        self.widescreen_storyboard = self.parse_int(line)

                # Parse [Editor] Beatmap Data
                if file_section == "[Editor]":
                    if line.startswith("Bookmarks"):
                        # Bookmarks is an integer list separated by commas, so we'll have to push all of them into self.bookmarks as integers
                        line = self.parse_string(line)
                        self.bookmarks = [int(n) for n in line.split(",")]
                    elif line.startswith("DistanceSpacing"):
                        self.distance_spacing = self.parse_float(line)
                    elif line.startswith("BeatDivisor"):
                        self.beat_divisor = self.parse_int(line)
                    elif line.startswith("GridSize"):
                        self.grid_size = self.parse_int(line)
                    elif line.startswith("TimelineZoom"):
                        self.timeline_zoom = self.parse_float(line)

                # Parse [Metadata] Beatmap Data
                if file_section == "[Metadata]":
                    if line.startswith("Title:"):
                        self.title = self.parse_string(line)
                    elif line.startswith("TitleUnicode"):
                        self.title_unicode = self.parse_string(line)
                    elif line.startswith("Artist:"):
                        self.artist = self.parse_string(line)
                    elif line.startswith("ArtistUnicode"):
                        self.artist_unicode = self.parse_string(line)
                    elif line.startswith("Creator"):
                        self.creator = self.parse_string(line)
                    elif line.startswith("Version"):
                        self.version = self.parse_string(line)
                    elif line.startswith("Source"):
                        self.source = self.parse_string(line)
                    elif line.startswith("Tags"):
                        line = self.parse_string(line)
                        self.tags = [str(tag) for tag in line.split(" ")]
                    elif line.startswith("BeatmapID"):
                        self.beatmap_id = self.parse_int(line)
                    elif line.startswith("BeatmapSetID"):
                        self.beatmap_set_id = self.parse_int(line)
                    
                # Parse [Difficulty] Beatmap Data
                if file_section == "[Difficulty]":
                    if line.startswith("HPDrainRate"):
                        self.hp_drain_rate = self.parse_float(line)
                    elif line.startswith("CircleSize"):
                        self.circle_size = self.parse_float(line)
                    elif line.startswith("OverallDifficulty"):
                        self.overall_difficulty = self.parse_float(line)
                    elif line.startswith("ApproachRate"):
                        self.approach_rate = self.parse_float(line)
                    elif line.startswith("SliderMultiplier"):
                        self.slider_multiplier = self.parse_float(line)
                    elif line.startswith("SliderTickRate"):
                        self.slider_tick_rate = self.parse_float(line)

                # Parse [Events] Beatmap Data - Didn't bother, as no one uses this.
                # Not really important for our purpose.
                if file_section == "[Events]":
                    if "," in line:
                        event_data = line.split(",")
                        self.events.append({ 
                            'sprite': 0,
                            'centre': 0,
                            'background': event_data[2],
                            'x': 0,
                            'y': 0
                        })

                # Parse [TimingPoints] Beatmap data
                if file_section == "[TimingPoints]":
                    if "," in line:
                        timing_data = line.split(",")
                        timing_point_obj = {
                            'offset': float(timing_data[0]),
                            'milliseconds_per_beat': float(timing_data[1]),
                            'meter': int(timing_data[2]),
                            'sample_type': int(timing_data[3]),
                            'sample_set': int(timing_data[4]),
                            'volume': int(timing_data[5]),
                            'inherited': int(timing_data[6]),
                            'kiai_mode': int(timing_data[7])
                        }
                        # Add BPM to timing point if meme
                        if timing_point_obj['milliseconds_per_beat'] != -100:
                            timing_point_obj['bpm'] = int(round(60000 / timing_point_obj['milliseconds_per_beat']))
                        self.timing_points.append(timing_point_obj)

                # Parse [HitObjects] Beatmap Data
                if file_section == "[HitObjects]":
                    if ":" in line:
                        line = line.replace(":", ",")
                        # Parse LNs first
                        if "128" in line:
                            hitobject_data = line.split(",")
                            self.hit_objects.append({
                                'x': int(hitobject_data[0]),
                                "y": int(hitobject_data[1]),
                                'start_time': int(hitobject_data[2]),
                                'type': int(hitobject_data[3]), # 1 is normal - 128 is LN
                                'hitsound': int(hitobject_data[4]),
                                'end_time': int(hitobject_data[5]),
                                'sample_set': 0,
                                'additions': 0,
                                'custom_index': 0,
                                'sample_volume': 0,
                                'is_long_note': True
                            })
                        # Parse regular hit objects
                        elif "128" not in line:
                            hitobject_data = line.split(",")
                            self.hit_objects.append({
                                'x': int(hitobject_data[0]),
                                'y': int(hitobject_data[1]),
                                'start_time': int(hitobject_data[2]),
                                'type': int(hitobject_data[3]),
                                'hitsound': int(hitobject_data[4]),
                                'sample_set': 0,
                                'additions': 0,
                                'custom_index': 0,
                                'sample_volume': 0,
                                'is_long_note': False
                            })

            # Sort hit objects by their start_time                
            self.hit_objects.sort(key=operator.itemgetter("start_time")) 
            #print("SAMPLE TIMING POINT")
            #pprint(self.timing_points[0])
            #print("\nSAMPLE HIT OBJECT")
            #pprint(self.hit_objects[0])
            #pprint(vars(self))
    
    # Takes a the current beatmap object and creates a new .osu file with it
    # This is especially useful if you want to change certain things about the
    # beatmap and quickly save it.
    def save_beatmap(self, path):
        f = open(path, "w+")
        map_content = (
            "osu file format v{0}\n"
            "\n"
            "[General]\n"
            "AudioFilename: {1}\n"
            "AudioLeadIn: {2}\n"
            "PreviewTime: {3}\n"
            "Countdown: {4}\n"
            "SampleSet: {5}\n"
            "StackLeniency: {6}\n"
            "Mode: {7}\n"
            "LetterboxInBreaks: {8}\n"
            "SpecialStyle: {9}\n"
            "WidescreenStoryboard: {10}\n"
            "\n"
            "[Editor]\n" 
            "Bookmarks: {11}\n"
            "DistanceSpacing: {12}\n"
            "BeatDivisor: {13}\n"
            "GridSize: {14}\n"
            "TimelineZoom: {15}\n"
            "\n"
            "[Metadata]\n"
            "Title:{16}\n"
            "TitleUnicode:{17}\n"
            "Artist:{18}\n"
            "ArtistUnicode:{19}\n"
            "Creator:{20}\n"
            "Version:{21}\n"
            "Source:{22}\n"
            "Tags:{23}\n"
            "BeatmapID:{24}\n"
            "BeatmapSetID:{25}\n"
            "\n"
            "[Difficulty]\n"
            "HPDrainRate:{26}\n"
            "CircleSize:{27}\n"
            "OverallDifficulty:{28}\n"
            "ApproachRate:{29}\n"
            "SliderMultiplier:{30}\n"
            "SliderTickRate:{31}\n"
            "\n"
            "[Events]\n"
            "//Background and Video events\n"
            "0,0,\"RandomBGName.jpg\",0,0\n"
            "//Break Periods\n"
            "//Storyboard Layer 0 (Background)\n"
            "//Storyboard Layer 1 (Fail)\n"
            "//Storybard Layer 2 (Pass)\n"
            "//Storyboard Layer 3 (Foreground)\n"
            "//Storyboard Sound Samples\n"
            "\n"
            "[TimingPoints]\n"
        ).format(
            str(self.file_format),
            self.audio_file_name,
            str(self.audio_lead_in),
            str(self.preview_time),
            str(self.countdown),
            str(self.sample_set),
            str(self.stack_leniency),
            str(self.mode),
            str(self.letterbox_in_breaks),
            str(self.special_style),
            str(self.widescreen_storyboard),
            ",".join([str(x) for x in self.bookmarks]),
            str(self.distance_spacing),
            str(self.beat_divisor),
            str(self.grid_size),
            str(self.timeline_zoom),
            self.title,
            self.title_unicode,
            self.artist,
            self.artist_unicode,
            self.creator,
            self.version,
            self.source,
            " ".join(x for x in self.tags),
            str(self.beatmap_id),
            str(self.beatmap_set_id),
            str(self.hp_drain_rate),
            str(self.circle_size),
            str(self.overall_difficulty),
            str(self.approach_rate),
            str(self.slider_multiplier),
            str(self.slider_tick_rate)
            )

        # Iterate over the timing points and add them to the string
        for tp in self.timing_points:
            content = "{0},{1},{2},{3},{4},{5},{6},{7}\n".format(
                tp['offset'], 
                tp['milliseconds_per_beat'],
                tp['meter'],
                tp['sample_type'],
                tp['sample_set'],
                tp['volume'],
                tp['inherited'],
                tp['kiai_mode']
            )
            map_content += content

        map_content += "\n[HitObjects]\n"

        # Iterate over the hit objects and add them to the string
        for obj in self.hit_objects:
            # Long notes have different syntax than normal hit objects
            # so we add two cases here for them.
            if obj['is_long_note']:
                content = "{0},{1},{2},{3},{4},{5}:0:0:0:0:\n".format(
                    obj['x'],
                    obj['y'],
                    obj['start_time'],
                    obj['type'],
                    obj['hitsound'],
                    obj['end_time']
                )
                map_content += content
            else:
                # Else, it must be a normal hit object, so we'll add them here
                content = "{0},{1},{2},{3},{4},0:0:0:0:\n".format(
                    obj['x'],
                    obj['y'],
                    obj['start_time'],
                    obj['type'],
                    obj['hitsound']
                )
                map_content += content

        # Write to file
        f.write(textwrap.dedent(map_content))
        f.close()

    def parse_string(self, line):
        try:
            return line.split(": ")[1]
        except IndexError:
            pass
        try:
            return line.split(":")[1]
        except IndexError:
            return None
    

    def parse_int(self, line):
        try:
            return int(line.split(": ")[1])
        except IndexError:
            pass
        try:
            return int(line.split(":")[1])
        except IndexError:
            return None

    def parse_float(self, line):
        try:
            return float(line.split(": ")[1])
        except IndexError:
            pass
        try:
            return float(line.split(":")[1])
        except IndexError:
            return None


# Function that returns a beatmap object
def parse_beatmap(beatmap_file_path):
    return Beatmap(beatmap_file_path)
