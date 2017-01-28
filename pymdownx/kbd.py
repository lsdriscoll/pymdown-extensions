"""KBD."""
from __future__ import unicode_literals
from markdown import Extension
from markdown.inlinepatterns import Pattern
from markdown import util as md_util
from . import util
from . import keymap_db as keymap
import re

RE_KBD = r'''(?x)
(?:
    # Escape
    (?<!\\)((?:\\{2})+)(?=\+)|
    # Key
    \+{2}
    (
        (?:(?:[\w\-]+|"(?:\\.|[^"])+"|\'(?:\\.|[^\'])+\')\+)*?
        (?:[\w\-]+|"(?:\\.|[^"])+"|\'(?:\\.|[^\'])+\')
    )
    \+{2}
)
'''

ESCAPE_RE = re.compile(r'''(?<!\\)(?:\\\\)*\\(.)''')
ESCAPED_BSLASH = '%s%s%s' % (md_util.STX, ord('\\'), md_util.ETX)
DOUBLE_BSLASH = '\\\\'


class KbdPattern(Pattern):
    """Return kbd tag."""

    def __init__(self, pattern, config, md):
        """Initialize."""

        self.ksep = config['keyboard_separator']
        self.markdown = md
        self.strict = config['strict']
        self.classes = config['class'].split(' ')
        self.html_parser = util.HTMLParser()
        self.map = self.merge(keymap.keymap, config['key_map'])
        self.aliases = keymap.aliases
        self.camel = config['camel_case']
        Pattern.__init__(self, pattern)

    def merge(self, x, y):
        """Given two dicts, merge them into a new dict."""

        z = x.copy()
        z.update(y)
        return z

    def normalize(self, key):
        """Normalize the value."""

        if not self.camel:
            return key

        norm_key = []
        last = ''
        for c in key:
            if c.isupper():
                if not last or last == '-':
                    norm_key.append(c.lower())
                else:
                    norm_key.extend(['-', c.lower()])
            else:
                norm_key.append(c)
            last = c
        return ''.join(norm_key)

    def process_key(self, key):
        """Process key."""

        if key.startswith(('"', "'")):
            value = (None, self.html_parser.unescape(ESCAPE_RE.sub(r'\1', key[1:-1])))
        else:
            norm_key = self.normalize(key)
            canonical_key = self.aliases.get(norm_key, norm_key)
            name = self.map.get(canonical_key, None)
            value = (canonical_key, name) if name else None
        return value

    def handleMatch(self, m):
        """Hanlde kbd pattern matches."""

        if m.group(2):
            return m.group('escapes').replace(DOUBLE_BSLASH, ESCAPED_BSLASH)

        content = [self.process_key(key) for key in m.group(3).split('+')]

        if None in content:
            return

        base_classes = self.classes[:]

        el = md_util.etree.Element(
            ('kbd' if self.strict else 'span'),
            ({'class': ' '.join(self.classes)} if self.classes else {})
        )

        last = None
        for item_class, item_name in content:
            classes = base_classes[:]
            if item_class:
                classes.append('key-' + item_class)
            if last is not None and self.ksep:
                span = md_util.etree.SubElement(el, 'span')
                span.text = md_util.AtomicString(self.ksep)
            kbd = md_util.etree.SubElement(el, 'kbd', {'class': (' '.join(classes) if classes else {})})
            kbd.text = md_util.AtomicString(item_name)
            last = kbd

        return el


class KbdExtension(Extension):
    """Add KBD extension to Markdown class."""

    def __init__(self, *args, **kwargs):
        """Initialize."""

        self.config = {
            'keyboard_separator': ['+', "Provide a keyboard separator - Default: \"+\""],
            'strict': [False, "Format keys and menus according to HTML5 spec - Default: False"],
            'class': ['keyboard', "Provide class(es) for the kbd elements - Default: kbd"],
            'camel_case': [False, 'Allow camle case conversion for key names PgDn -> pg-dn - Default: False'],
            'key_map': [{}, 'Additional keys to include or keys to override - Default: {}']
        }
        super(KbdExtension, self).__init__(*args, **kwargs)

    def extendMarkdown(self, md, md_globals):
        """Add support for emojis."""

        util.escape_chars(md, ['+'])
        md.inlinePatterns.add("kbd", KbdPattern(RE_KBD, self.getConfigs(), md), "<escape")


###################
# Make Available
###################
def makeExtension(*args, **kwargs):
    """Return extension."""

    return KbdExtension(*args, **kwargs)
