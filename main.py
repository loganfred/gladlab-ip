#! /usr/local/Caskroom/miniconda/base/envs/glad/bin/python

import os
import glob
import logging
import argparse

from logs import log
import postprocess
import webapp
import cache


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='command')

    cache_parser = subparsers.add_parser('thumbs')
    web_parser = subparsers.add_parser('draw')
    compute_parser = subparsers.add_parser('postprocess')

    cache_parser.add_argument('folder', help='Folder with nd2 files')
    cache_parser.add_argument('-s', '--size', default=512)
    cache_parser.add_argument('-c', '--channel', type=int, default=0)
    cache_parser.add_argument('-f', '--force', action='store_true')
    cache_parser.add_argument('-v', '--verbose', action='store_true')

    web_parser.add_argument('folder', help='Folder with nd2 files')
    web_parser.add_argument('-p', '--port', action='store', default=8080)
    web_parser.add_argument('-t', '--tablet', action='store_true', dest='lan')
    web_parser.add_argument('-v', '--verbose', action='store_true')

    compute_parser.add_argument('file', help='JSON file of export data')
    compute_parser.add_argument('-d', '--dest', default=None, help='output folder')
    compute_parser.add_argument('-v', '--verbose', action='store_true')

    args = parser.parse_args()

    if args.verbose:
        log.setLevel(logging.INFO)
    else:
        log.setLevel(logging.WARNING)

    if args.command in ['thumbs', 'draw']:
        # go ahead and get the list of files and file names
        files = glob.glob(os.path.join(args.folder, '*.nd2'))
        files.sort()
        names = [os.path.basename(f) for f in files]
        listing = zip(names, files)
    elif args.dest is None:
        args.dest = os.path.basename(args.file)

    if args.command == 'thumbs':
        cache.run(args, listing)
    elif args.command == 'draw':
        webapp.run(args, listing)
    elif args.command == 'postprocess':
        postprocess.run(args)
    else:
        parser.print_usage()
