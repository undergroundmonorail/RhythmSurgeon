import json
import re

class Level:
    """A Rhythm Doctor level."""
    
    def __init__(self, filename):
        level_json = open(filename)
        self.settings = level_json.settings
        self.rank_description = level_json.rankDescription
        self.rows = level_json.rows
        self.events = level_json.events

def open(filename):
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

    return json.parse(level_text)

def save(filename, level):
    """Save the level back to the file, after making a backup.
    
    Doesn't necessarily save exactly in the nicely formatted way that the
    Rhythm Doctor level editor does. It just spits out a valid JSON object.
    """

    level_text = json.dumps("""
    {
        "settings": {settings},
        "rankDescription": {rank_description},
        "rows": {rows},
        "events": {events}
    }""".format(settings=level.settings,
                rank_description=level.rank_description,
                rows=level.rows,
                events=level.events)

    with open(filename, "r+") as f:
        old_text = f.read()

        with open(filename + ".bak", "w") as g:
            g.write(old_text)

        f.write(json.dumps(level.level_json))
