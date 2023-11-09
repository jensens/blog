import feedparser
from feedgen.feed import FeedGenerator
import sys

def convert_atom_to_rss(atom_file, rss_file):
    # Parse Atom feed
    atom_feed = feedparser.parse(atom_file)

    # Create RSS feed
    fg = FeedGenerator()
    fg.title(atom_feed.feed.title)
    fg.link(href=atom_feed.feed.link, rel='alternate')
    fg.description(getattr(atom_feed.feed, "subtitle", "./."))

    # Add entries
    for entry in atom_feed.entries:
        fe = fg.add_entry()
        fe.title(entry.title)
        fe.link(href=entry.link, rel='alternate')
        fe.description(entry.summary or "./.")
        fe.published(entry.published)
        fe.updated(entry.updated)

    # Generate RSS 2.0 feed
    rss_feed = fg.rss_str(pretty=True)

    # Write RSS feed to a new file
    with open(rss_file, 'wb') as f:
        f.write(rss_feed)

# Example usage
if __name__ == '__main__':
    convert_atom_to_rss(sys.argv[1], sys.argv[2])
