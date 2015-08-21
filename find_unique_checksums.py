from glob import glob
from collections import defaultdict
import json

"""
Searching for the smallest set of (publicly accessible) filenames that identify a Magento version.


md5sums = {
    'file1' : {
        'hash1': ['magento1','magento2'],
        'hash2': ...
    }
}

"""

sources = glob('md5sums/*')

md5sums = defaultdict(lambda: defaultdict(list))
releases = defaultdict(dict)

for source in sources:
    release = source.split('/')[1].replace('magento-', '').replace('-', ' ')
    with open(source) as fh:
        for line in fh:
            md5, name = line.strip().split()
            releases[release][name] = md5
            md5sums[name][md5].append(release)

unique_sums = defaultdict(dict)
"""
unique_sums = {
    'file1' : {
        'hash1' : 'releasex',
        'hash2' : 'releasey'
    }

}
"""

releases_hashes = defaultdict(list)

for filename, hashes in md5sums.iteritems():
    for hash, versions in hashes.iteritems():
        if len(versions) > 1:
            continue
            
        
        release = versions[0]
        unique_sums[filename][hash] = release
        releases_hashes[release].append(hash)

fingerprints = defaultdict(dict)

def _sort_filehash_on_granularity_and_impact(filehash):
    # granularity = how many versions does this filehash identify (ideally, 1)
    # impact = how many versions have a unique hash for this file (reverse sort)
    
    filename, hash = filehash
    
    granularity = len(md5sums[filename][hash])
    impact = -len(unique_sums[filename])
    
    return (granularity, impact)

for version, files in sorted(releases.items()):
    # find the file/hash from files which 
    # has the least amount of versions attached (preferably just 1).
    ordered_files = sorted(files.items(), key=_sort_filehash_on_granularity_and_impact)
    filename, hash = ordered_files[0]
    all_versions_for_this_hash = md5sums[filename][hash]
    fingerprints[filename][hash] = ', '.join(sorted(all_versions_for_this_hash))

for filename in fingerprints.keys():
    for hash, release in unique_sums[filename].items():
        fingerprints[filename][hash] = release
    
print json.dumps(fingerprints, indent=4)
