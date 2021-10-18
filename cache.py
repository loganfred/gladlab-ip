import os
import json
import base64
import logging
from io import BytesIO
from PIL import Image as PImage

from image import Image

logging.getLogger(__name__)


def format_cache_file(file, channel, size):
    return f'{file}_thumb_c{channel}_{size}x{size}.json'


def get(file, channel, size):

    name = os.path.basename(file)
    logging.info(f'working on {name} channel {channel} @ {size}x{size}')
    f = os.path.splitext(file)[0]
    cached = format_cache_file(f, channel, size)
    logging.info(f'checking for "{cached}"')

    if os.path.exists(cached):
        logging.info('found it')
        with open(cached, 'r') as fin:
            return json.load(fin)

    logging.info('creating it')

    with Image(file, channel=channel, size=size) as zstack:

        # copy so that changes can be made for non-serializable objects
        metadata = dict(zstack.metadata)

        if metadata.get('date'):
            metadata['date'] = metadata['date'].strftime('%m%d%Y, %H:%M:%S')

        metadata.pop('z_levels')
        metadata.update({'sizes': zstack.sizes})

        img = PImage.fromarray(zstack.maxprojection()).convert('L')
        width, height = img.size
        resolution = f'{width}x{height}'

        with BytesIO() as buffer:
            img.save(buffer, format='png')

            enc = base64.b64encode(buffer.getvalue())
            res = {'file': os.path.basename(f),
                   'abspath': f,
                   'resolution': resolution,
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
            _ = get(file, args.channel, args.size)
        except Exception as e:
            logging.warn(f'! aborting {file} {e}')
