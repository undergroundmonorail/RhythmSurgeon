import json
import re

class Level:
    """A Rhythm Doctor level."""
    
    def __init__(self, filename):
        self.filename = filename
        level_json = read(filename)
        self.settings = level_json["settings"]
        self.rows = level_json["rows"]
        self.events = level_json["events"]

    def save(self):
        """Save the level back to the file, after making a backup.
        
        Doesn't necessarily save exactly in the nicely formatted way that the
        Rhythm Doctor level editor does. It just spits out a valid JSON object.
        """
    
        level_text = json.dumps({
            "settings": self.settings,
            "rows": self.rows,
            "events": self.events
        })
    
        with open(self.filename, "r+") as f:
            old_text = f.read()
    
            with open(self.filename + ".bak", "w") as g:
                g.write(old_text)
    
            f.seek(0, 0)
            f.write(level_text)
            f.truncate()

    def bars(self):
        """Generator that yields all the events in each measure."""

        def sort_by_beats(events):
            """Sort events by bar first, then beat in the bar."""
            bar_beat = lambda e:(e["bar"], e["beat"])
            return sorted(events, key=bar_beat)

        # the list to yield
        bar = []

        for event in sort_by_beats(self.events):
            # If the list is non-empty and the most recent event was in a
            # different bar than the current one, yield the list and clear it
            if bar != [] and event["bar"] != bar[-1]["bar"]:
                yield bar
                bar = []

            bar.append(event)

        yield bar


def read(filename):
    """Return the level's file parsed as JSON"""

    def strip_trailing_commas(text):
        """Remove trailing commas from JSON text.
        
        Rhythm Doctor puts a comma at the end of each event, row, etc., despite
        this being technically non-compliant JSON. This function removes those
        commas so the json module can parse the text.

        This regex solution isn't bulletproof, but a comma directly followed by
        whitespace characters and '}' or ']' shouldn't be an issue for this
        purpose.
        """

        text = re.sub(",[ \t\r\n]+}", "}", text)
        text = re.sub(",[ \t\r\n]+\]", "]", text)

        return text

    with open(filename) as f:
        level_text = strip_trailing_commas(f.read())

    return json.loads(level_text)


