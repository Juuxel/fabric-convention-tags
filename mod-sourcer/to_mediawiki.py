import json
from operator import itemgetter
from typing import Dict, List

with open('tags.json', 'r') as fh:
    root = json.load(fh)


def generate_page(sources, tags: List[Dict], out):
    # Sort tags by depth first
    tags.sort(key=lambda x: x['id'].count('/'))
    tags.sort(key=itemgetter('id'))

    print("^ Tag ID ^ Contained IDs ^ Defined by ^", file=out)
    for tag in tags:
        for idx, content in enumerate(tag['content']):
            if idx == 0:
                print("|", 'c:' + tag['id'], file=out, end='')
            else:
                print("| :::", file=out, end='')

            print("|", content['value'], file=out, end='')
            print("|", ", ".join(content['sources']), file=out, end='')
            print(" |", file=out)


with open('tags.txt', 'wt') as out:
    print(file=out)
    print('===== Item Tags =====', file=out)
    print(file=out)
    generate_page(root['sources'], root['items'], out)

    print(file=out)
    print('===== Block Tags =====', file=out)
    print(file=out)
    generate_page(root['sources'], root['blocks'], out)

    print(file=out)
    print('===== Fluid Tags =====', file=out)
    print(file=out)
    generate_page(root['sources'], root['fluids'], out)

    print(file=out)
    print('===== Entity Types Tags =====', file=out)
    print(file=out)
    generate_page(root['sources'], root['entity_types'], out)

    print(file=out)
    print('===== Game Events Tags =====', file=out)
    print(file=out)
    generate_page(root['sources'], root['game_events'], out)

    print(file=out)
    print('===== Sources =====', file=out)
    print(file=out)
    print("^ Mod ID ^ Name ^ Version ^ URL ^", file=out)

    for source in root['sources'].values():
        print("|", source['id'], "|", source["name"], "|", source["version"], "|", source["url"], "|", file=out)
