from collections import defaultdict
import json
import os
from pprint import pprint

from deco import concurrent, synchronized

DATADIR = "./data"


@concurrent
def langs(filename):
    """returns defaultdict of the languages represented in PullRequestEvents"""
    print('processing', filename)
    langs = defaultdict(int)
    events = [json.loads(e) for e in open(filename) if 'PullRequestEvent' in e]
    pull_request_events = [e for e in events if e['type']=='PullRequestEvent']
    for event in pull_request_events:
        try:
            lang = event['payload']['pull_request']['head']['repo']['language']
        except (AttributeError, TypeError):
            lang = 'no lang'
        langs[lang] += 1
    return langs

def reduce_langs(*lang_components):
    all_langs = defaultdict(int)
    for lang_component in lang_components:
        for key, value in lang_component.items():
            all_langs[key] += value
    return all_langs

@synchronized
def main():
    filenames = [os.path.join(DATADIR, f) for f in os.listdir(DATADIR) if ".json" in f]
    lang_components = [None for f in filenames]
    for i, f in enumerate(filenames):
        lang_components[i] = langs(f)

    pprint(reduce_langs(*lang_components))


if __name__ == '__main__':
    main()