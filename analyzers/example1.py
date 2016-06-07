import os
import json
import random

ANALYZERS_DIR = os.path.join(os.path.basename(__file__), 'analyzers')


def main():
    import argparse
    parser = argparse.ArgumentParser(description='Video analysis tool.')
    parser.add_argument('video', help='input video')
    parser.add_argument('meta')
    args = parser.parse_args()
    in_video = args.video
    with open(args.meta, 'r', encoding='utf-8') as f:
        meta = json.loads(f.read())

    # print(in_video, meta)
    for x in range(int(meta['duration'])):
        print("%f %f" % (x, random.randint(10, 100)))


if __name__ == '__main__':
    main()
