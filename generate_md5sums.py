#!/usr/bin/env python3
import json
import os
import logging
import re
import tarfile
import lzma
from hashlib import md5
from operator import itemgetter


DST = 'md5sums'


def find_archive_files(start_path):
    for root, dir, files in os.walk(start_path, followlinks=True):
        for file in files:
            if not file.endswith('.gz'):
                print("Invalid extension: {}".format(file))
                continue
            if re.search('sample', file, flags=re.IGNORECASE):
                print("Sample data, skipping {}".format(file))
                continue
            yield os.path.join(root, file)


def magento_version_from_archive_path(path):

    match = re.search('-([\d\.]+\d)', path)
    if match:
        version = match.group(1)
    else:
        return None

    if re.search('-EE|ee-full|enterprise', path):
        edition = 'EE'
    elif re.search('-CE|ce-full', path):
        edition = 'CE'
    else:
        return None

    return 'magento-{}-{}'.format(edition, version)


def hashes_from_archive(path):

    hashes = dict()
    with tarfile.open(path) as tar:
        for ti in tar:
            if not ti.isfile():
                continue

            # some archives have a container folder, others don't
            if ti.name.startswith('magento/') or ti.name.startswith('1.9.1.1/'):
                relpath = ti.name.partition('/')[2]
            else:
                relpath = ti.name

            content = tar.extractfile(ti).read()
            hashes[relpath] = md5(content).hexdigest()

            # print(hashes[relpath], relpath, ti.size)

    return sorted(hashes.items(), key=itemgetter(0))


if __name__ == '__main__':

    for archive in find_archive_files('sources'):
        version = magento_version_from_archive_path(archive)
        if not version:
            logging.warning("no version could be derived from {}".format(archive))
            continue

        checksum_file = os.path.join(DST, version) + '.xz'

        if os.path.exists(checksum_file):
            print("Skipping {}, already exists".format(checksum_file))
            continue

        print("{} => {}".format(archive, checksum_file))

        hashes = hashes_from_archive(archive)

        with lzma.open(checksum_file, 'wt') as fh:
            for p, h in hashes:
                fh.write("{} {}\n".format(h, p))


