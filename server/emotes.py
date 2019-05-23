from os import path
from configparser import ConfigParser

import logging
logger = logging.getLogger('debug')


char_dir = 'characters'

class Emotes:
    """
    Represents a list of emotes read in from a character INI file
    used for validating which emotes can be sent by clients.
    """

    def __init__(self, name):
        self.name = name
        self.emotes = set()
        self.read_ini()

    def read_ini(self):
        char_ini = ConfigParser(comment_prefixes=('#', ';', '//', '\\\\'),
            strict=False)
        try:
            char_path = path.join(char_dir, self.name, 'char.ini')
            with open(char_path) as f:
                char_ini.read_file(f)
        except FileNotFoundError:
            logger.warn(f'Character file {char_path} not found')
            return

        for emote_id in range(1, int(char_ini['Emotions']['number'])):
            _name, preanim, anim, _mod = char_ini['Emotions'][emote_id].split('#')
            if emote_id in char_ini['SoundN']:
                sfx = char_ini['SoundN'][emote_id]
                if len(sfx) == 1:
                    # Often, a one-character SFX is a placeholder for no sfx,
                    # so allow it
                    sfx = None
            else:
                sfx = None
            self.emotes.add((preanim, anim, sfx))

            # No SFX should always be allowed
            self.emotes.add((preanim, anim, None))


    def validate(self, preanim, anim, sfx):
        """
        Determines whether or not an emote canonically belongs to this
        character (that is, it is defined server-side).
        """
        # There are no emotes loaded, so allow anything
        if len(self.emotes) == 0:
            return True

        if len(sfx) <= 1:
            sfx = None
        return (preanim, anim, sfx) in self.emotes