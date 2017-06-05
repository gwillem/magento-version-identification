#!/usr/bin/env python3
import lzma
from glob import glob
from collections import defaultdict
import json
import unittest
import re

"""
Searching for the smallest set of (publicly accessible) filenames that identify a Magento version.
"""

STATIC_FILTER = [
    'js/',
    'media/',
    'skin/',
    'favicon.ico',
]

# Often removed/altered
BLACKLIST_FILTER = [
    'skin/frontend',
]


def is_primary_candidate(path):
    # Can we use this path for identifiation purposes?
    for x in BLACKLIST_FILTER:
        if path.startswith(x):
            return False

    for x in STATIC_FILTER:
        if path.startswith(x):
            return True

    return False


def filter_candidates(lines):
    for line in lines:
        try:
            md5, _, path = line.strip().partition(' ')
        except:
            print("line: {}".format(line))
            raise

        if is_primary_candidate(path):
            yield md5, path


def _sort_filehash_on_granularity_and_impact(filehash):
    # granularity = how many versions does this filehash identify (ideally, 1)
    # impact = how many versions have a unique hash for this file (reverse sort)
    
    filename, hash = filehash
    
    granularity = len(md5sums[filename][hash])
    impact = -len(unique_sums[filename])
    
    return (granularity, impact)


def humanize(versions):
    # squash multiple versions, assume ordered
    allversions = [re.split('[\.\ ]', x) for x in versions]
    minlength = min([len(x) for x in allversions])
    output = []
    for i in range(minlength):
        items_at_pos_i = set([x[i] for x in allversions])
        if len(items_at_pos_i) != 1:
            output.append('x')
            break
        output.append(items_at_pos_i.pop())
    
    if len(output) <= 1:
        return ', '.join(versions)
    
    return output.pop(0) + ' ' + '.'.join(output)


def source_path_to_release(path):
    # magento-CE-2.0.12.xz
    match = re.search('(CE|EE)-(\d[\d\.]+\d)', path)
    assert match, "Could not determine version from file {}".format(path)
    return match.group(1) + ' ' + match.group(2)


if __name__ == '__main__':

    md5sums = defaultdict(lambda: defaultdict(list))
    """
    md5sums = {
        'x/y/file1' : {
            'hash1': ['CE 1.0.0', 'EE 2.0.1'],
            'hash2': ...
        }
    }

    """
    releases = defaultdict(dict)
    unique_sums = defaultdict(dict)
    """
    unique_sums = {
        'x/y/file1' : {
            'hash1' : 'CE 1.0.0',
            'hash2' : 'CE 1.9.3'
        }

    }
    """

    releases_hashes = defaultdict(list)

    sources = glob('md5sums/magento-??-1.*.xz')

    for source in sources:
        version = source_path_to_release(source)
        with lzma.open(source, 'rt') as fh:
            for md5, path in filter_candidates(fh):
                releases[version][path] = md5
                md5sums[path][md5].append(version)


    for filename, hashes in md5sums.items():
        for hash, versions in hashes.items():
            if len(versions) > 1:
                continue
                
            
            release = versions[0]
            unique_sums[filename][hash] = release
            releases_hashes[release].append(hash)

    fingerprints = defaultdict(dict)

    for version, files in sorted(releases.items()):
        # find the file/hash from files which 
        # has the least amount of versions attached (preferably just 1).
        ordered_files = sorted(files.items(), key=_sort_filehash_on_granularity_and_impact)
        filename, hash = ordered_files[0]
        all_versions_for_this_hash = md5sums[filename][hash]
        fingerprints[filename][hash] = humanize(sorted(all_versions_for_this_hash))

    # After we determine which files to include, add all unique hashes to
    # these file entries. Some versions are now listed multiple times. This
    # reduces the number of files we need to request and gives better results
    # if a site has modified some files.
    for filename in fingerprints.keys():
        for hash, release in unique_sums[filename].items():
            fingerprints[filename][hash] = release
        
    print(json.dumps(fingerprints, indent=4, sort_keys=True))

    with open('version_hashes.json', 'w') as f:
        f.write(json.dumps(fingerprints, indent=4, sort_keys=True))


class TestIt(unittest.TestCase):
    
    def test_humanize(self):
        
        tests = (
            (['CE 1.3.2.3', 'CE 1.3.2.4', 'CE 1.3.3.0'], 'CE 1.3.x'),
            (['CE 1.7.0.1', 'CE 1.7.0.2'], 'CE 1.7.0.x'),
            (['CE 1.7.0.1', 'EE 1.7.0.2'], 'CE 1.7.0.1, EE 1.7.0.2'),
        )
        
        for test, expected in tests:
            real = humanize(test)
            self.assertEqual(real, expected)
        
    def test_version_from_path(self):

        tests = (
            ('md5sums/magento-CE-2.0.12.xz', 'CE 2.0.12'),
            ('md5sums/magento-EE-2.0.0', 'EE 2.0.0'),
        )
        for test, want in tests:
            got = source_path_to_release(test)
            self.assertEqual(got, want)
