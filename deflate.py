from beatmap import parse_beatmap

def fix_star_rating(beatmap_path, diff_name, output_path):
    beatmap = parse_beatmap(beatmap_path)
    beatmap.version = diff_name
    detected_inflations = 0 

    # Create a list of all the RED (Not Inherited) timing sections
    timing_sections = []
    for timing_point in beatmap.timing_points:
        if timing_point['inherited'] == 1:
            timing_sections.append(timing_point)
    
    for i in range(len(beatmap.hit_objects)):
        # Find the correct timing point the hit object is in range of.
        current_timing_point = None
        for j in range(len(timing_sections)):
            try:
                if beatmap.hit_objects[i]['start_time'] >= timing_sections[j]['offset']:
                    if beatmap.hit_objects[i]['start_time'] < timing_sections[j + 1]['offset']:
                        current_timing_point = timing_sections[j]
                        break
            # In the event that there aren't any timing points left and the current one is the last one 
            except IndexError:
                current_timing_point = timing_sections[j]
                break

        try:
            if beatmap.hit_objects[i]['is_long_note']:

                # Find the next long note in the beatmap
                next_long_note = None
                for hit_object in beatmap.hit_objects[i:]:
                    if hit_object['is_long_note']:
                        next_long_note = hit_object
                        break

                # If the LNs have a short, but not zero start time difference, we'll consider that inflated.
                short_start_times = False
                start_time_difference = next_long_note['start_time'] - beatmap.hit_objects[i]['start_time']
                if start_time_difference != 0 and current_timing_point['milliseconds_per_beat'] / start_time_difference >= 8:
                    short_start_times = True


                # If the two LNS both have short LN hold times (300-able just by tapping), We'll consider that inflated as well
                short_hold_times = False
                current_object_hold_time = current_timing_point['milliseconds_per_beat'] / (beatmap.hit_objects[i]['end_time'] - beatmap.hit_objects[i]['start_time'])

                if next_long_note != None:
                    next_object_hold_time = current_timing_point['milliseconds_per_beat'] / (next_long_note['end_time'] - next_long_note['start_time'])
                    if current_object_hold_time >= 4 and next_object_hold_time >= 4:
                        short_hold_times = True

                # Change the inflated LN to a normal note
                if short_start_times or short_hold_times:
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

        except Exception as e:
            pass

    if detected_inflations > 0:
        print("Beatmap has " + str(detected_inflations) + " inflated LN patterns. Changed them to normal notes.")
    else:
        print("Beatmap does not have any inflated patterns.")
    
    # Save new beatmap
    beatmap.save_beatmap(output_path)