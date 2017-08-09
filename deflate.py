# We'll consider an LN mania pattern as inflated if:
# The start times of LNs are too close together -  Milliseconds per beat / Difference in milliseconds of two closest LN's is >= 8 (1/8th notes)
# The LNs have a small and less than 1/4th hold time

# If that's the case, we'll replace the LN at that start time with a normal hit object (Reduces star rating)
from beatmap import parse_beatmap

def fix_star_rating(beatmap_path, diff_name, output_path):
    beatmap = parse_beatmap(beatmap_path)

    # Set new beatmap difficulty name
    beatmap.version = diff_name
    detected_inflations = 0 

    # Create a list of all of the RED Line timing sections (Actual timing)
    timing_sections = []
    for timing_point in beatmap.timing_points:
        if timing_point['inherited'] == 1:
            timing_sections.append(timing_point)
    
    # Loop through all of the hit objects and timing points and find out
    # which timing point the hit object is in range of.
    for i in range(len(beatmap.hit_objects)):
        current_timing_point = None
        for j in range(len(timing_sections)):
            try:
                # If the hit object is greater or on the same tick as the current timing section,
                # and NOT before. 
                if beatmap.hit_objects[i]['start_time'] >= timing_sections[j]['offset']:
                    # If the hit object's start time is less than the next red timing point, it must be in range
                    # Current Timing Point -> Hit Object <- Next Timing Point
                    if beatmap.hit_objects[i]['start_time'] < timing_sections[j + 1]['offset']:
                        current_timing_point = timing_sections[j]
                        break
            # In the event that there aren't any timing points left and the current one is the last one 
            except IndexError:
                current_timing_point = timing_sections[j]
                break

        try:
            # The difference in milliseconds between the start times of two LNs - Density check
            if beatmap.hit_objects[i]['is_long_note'] and beatmap.hit_objects[i + 1]['is_long_note']:
                start_time_difference = beatmap.hit_objects[i + 1]['start_time'] - beatmap.hit_objects[i]['start_time']

                # If two LNS are at the same start time, we'll just skip to the next object
                # As we don't consider them as inflated
                if start_time_difference == 0:
                    continue

                object_note_difference = current_timing_point['milliseconds_per_beat'] / start_time_difference

                # If the object's start times are too close together (1/8ths)
                # this means it the objects are partially inflating the star rating.
                if object_note_difference >= 8:
                    # We'll lastly want to check if the current and next object's hold time are less than 1/4th notes
                    # Star rating inflation is obvious here with this last check.
                    current_object_hold_time = current_timing_point['milliseconds_per_beat'] / (beatmap.hit_objects[i]['end_time'] - beatmap.hit_objects[i]['start_time'])
                    next_object_hold_time = current_timing_point['milliseconds_per_beat'] / (beatmap.hit_objects[i + 1]['end_time'] - beatmap.hit_objects[i + 1]['start_time'])

                    # Difficulty inflated pattern detected
                    if current_object_hold_time >= 4 and next_object_hold_time >= 4:
                        # Change the LN to a normal note
                        beatmap.hit_objects[i] = {
                            'x': beatmap.hit_objects[i]['x'],
                            'y': beatmap.hit_objects[i]['y'],
                            'start_time': beatmap.hit_objects[i]['start_time'],
                            'type': 1,
                            'hitsound': beatmap.hit_objects[i]['hitsound'],
                            'sample_set': 0,
                            'additions': 0,
                            'custom_index': 0,
                            'sample_volume': 0,
                            'is_long_note': False
                        }

                        detected_inflations += 1
        except:
            pass

    if detected_inflations > 0:
        print("Beatmap has " + str(detected_inflations) + " inflated LN patterns. Changed them to normal notes.")
    else:
        print("Beatmap does not have any inflated patterns.")
    
    # Save new beatmap
    beatmap.save_beatmap(output_path)