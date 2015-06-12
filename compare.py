from glob import glob
from collections import defaultdict
from pprint import pprint
import json

"""

md5sums = {
    'file1' : {
        'hash1': ['magento1','magento2'],
        'hash2': ...
    }
}

Op zoek naar de kleinste set filenames die uniek een magento versie identificeren.

Welke files zijn uniek?
* Alle hashes met len(list) == 1
* Opslaan in dict: filename => [list of unique hashes]

Dan sorteren op number unique hashes reverse, 

"""

sources = glob('md5sums/*')

md5sums = defaultdict(lambda: defaultdict(list))
releases = defaultdict(dict)

for source in sources:
    release = 'CE ' + source.split('/')[1].split('-')[1]
    #~ print source, release
    with open(source) as fh:
        for line in fh:
            md5, name = line.strip().split()
            #~ print name, md5
            releases[release][name] = md5
            md5sums[name][md5].append(release)

#~ for filename, hashes in md5sums.iteritems():
    #~ num = len(hashes)
    #~ print "%(num)2d %(filename)s" % locals()


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
        #~ print '%(filename)s has only a single hash: %(hash)s for magento version %(release)s' % locals()
    

#~ print json.dumps(unique_sums, indent=4)
#~ sys.exit(1)

fingerprints = defaultdict(dict)

#~ for filename in sorted(unique_sums, key=lambda x: len(unique_sums[x]), reverse=True)[:15]:
    #~ print filename
    #~ for h, r in unique_sums[filename].iteritems():
        #~ fingerprints[filename][h] = r
        #~ print "\t", h, r


def sort_filehash_on_granularity_and_impact(filehash):
    # granularity = how many versions does this filehash identify (ideally, 1)
    # impact = how many versions have a unique hash for this file (reverse sort)
    
    filename, hash = filehash
    
    granularity = len(md5sums[filename][hash])
    impact = -len(unique_sums[filename])
    
    return (granularity, impact)

for version, files in sorted(releases.items()):
    # find the file/hash from files which 
    # has the least amount of versions attached (preferably just 1).
    ordered_files = sorted(files.items(), key=sort_filehash_on_granularity_and_impact)

    filename, hash = ordered_files[0]

    all_versions_for_this_hash = md5sums[filename][hash]

    print "Version %(version)s has %(filename)s which is unique to these versions: %(all_versions_for_this_hash)s" % locals()

    fingerprints[filename][hash] = ', '.join(sorted(all_versions_for_this_hash))
    
print json.dumps(fingerprints, indent=4)
    
    #~ 
#~ print json.dumps(
    #~ sorted(unique_sums.items(), key=lambda x: -len(x[1]))[:10],
    #~ indent=4
    #~ )
    
#~ for source in sources:
    #~ release = source.split('/')[1]
    #~ numhash = len(releases_hashes[release]) if release in releases_hashes else 0
    #~ print "Release %s has %d hashes" % (release, numhash)
    #~ for h in releases_hashes[release]:
        
#~ for release in sorted(releases):
    #~ print "Processing release", release
        
#~ for filename, hashes in unique_sums.iteritems():
    

#~ pprint(unique_sums)
