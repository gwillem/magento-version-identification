# Magento Version Identification

Hashes of static files can be used to determine a Magento's version remotely.

See [the result](version_hashes.json)

This repo does:

- Generate md5sum from static files of Magento releases
- Calculate the best set of checksums, optimized for coverage and speed (find the right version with the least amount of requests).

See also https://github.com/steverobbins/magescan/issues/77

Thanks to Steve Robbins for contributing hashes of Magento Enterprise releases.

