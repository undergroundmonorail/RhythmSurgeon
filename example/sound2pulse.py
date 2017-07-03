import sys
import rhythmsurgeon

# Load the level
level = rhythmsurgeon.Level(sys.argv[1])

# Sorting the rows shouldn't be necessary unless you've messed with them in the
# file already, but no harm in making sure.
level.rows.sort(key=lambda r:r["row"])

# Set row 0 pulse sound to None
level.rows[0]["pulseSound"] = "None"

# Iterate through all classic beats on row 0
def row_0_classic_beat(event):
    return event["type"] == "AddClassicBeat" and event["row"] == 0
for classic in filter(row_0_classic_beat, level.events):
    if classic["swing"]:
        print("WARNING: {0}:{1}".format(classic["bar"], classic["beat"]),
              "This tool doesn't yet support swing!",
              "The sounds for this beat will be misalaigned with the pulses.",
              "------------------------------------------------",
              sep='\n',
              file=sys.stderr)

    # For each of the pulses, play the sound if there's no X on that clap
    pattern = level.x_at_beat(classic["bar"], classic["beat"], 0)

    for i in range(7):
        # Add the length of time between pulses times the number of pulses so
        # far to get offset from when beat started
        cur_bar, cur_beat = level.sum_beats(classic["bar"],
                                                    classic["beat"],
                                                    1,
                                                    classic["tick"] * i)
        if (pattern + '-')[i] != 'x':
            level.events.append({
                "bar": cur_bar,
                "beat": cur_beat,
                "y": 0,
                "type": "PlaySound",
                "filename": "sound.ogg",
                "offset": 0,
                "volume": 60
            })

# Save it back into the file
level.save()

input("Press Enter to continue.")
