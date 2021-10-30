import os
import json
import base64
import logging
from io import BytesIO
from PIL import Image as PImage

from image import Image

log = logging.getLogger(__name__)


def format_cache_file(file, channel, size):
    f = os.path.splitext(file)[0].replace(' ','_')
    return f'{f}_thumb_c{channel}_{size}x{size}.json'


def get(file, channel, size, force=False):

    name = os.path.basename(file)
    log.info(f'working on "{file}"')
    log.info(f'channel: {channel} size: {size}x{size}')
    cached = format_cache_file(file, channel, size)
    log.info(f'checking for "{cached}"')

    if force and os.path.exists(cached):
        log.info('Path exists but is being overwritten due to --force')
    elif os.path.exists(cached):
        log.info('found it')
        with open(cached, 'r') as fin:
            return json.load(fin)

    log.info(f'creating it with size {size}')

    with Image(file, channel=channel, size=size) as zstack:

        # copy so that changes can be made for non-serializable objects
        metadata = dict(zstack.metadata)

        if metadata.get('date'):
            metadata['date'] = metadata['date'].strftime('%m%d%Y, %H:%M:%S')

        metadata.pop('z_levels')
        metadata.update({'sizes': zstack.sizes})

        img = PImage.fromarray(zstack.maxprojection()).convert('L')

        with BytesIO() as buffer:
            img.save(buffer, format='png')

            enc = base64.b64encode(buffer.getvalue())
            res = {'file': os.path.basename(file),
                   'abspath': os.path.abspath(file),
                   'resolution': img.size,
                   'channel': channel,
                   'size': size,
                   'meta': metadata,
                   'image': enc.decode('utf-8')}
            with open(cached, 'w') as fout:
                json.dump(res, fout)

            return res


def run(args, listing):

    for name, file in listing:
        try:
            get(file, args.channel, args.size, force=args.force)
        except Exception as e:
            log.warn(f'! aborting {file} {e}')
