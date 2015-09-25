# Magento Version Identification

Hashes of static files can be used to determine the version of a remote Magento installation. Currently this results in an accurate version identification for 91,7% of 220,000 tested Magento installations worldwide.

See [the resulting hashes](version_hashes.json)

This repo does:

- Generate md5sum from static files of Magento releases
- Calculate the best set of checksums, optimized for coverage and speed (find the right version with the least amount of requests).

The original idea was discussed [here](https://github.com/steverobbins/magescan/issues/77).

Thanks to Steve Robbins for contributing Enterprise hashes.

