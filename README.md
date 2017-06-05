# Magento Version Identification

Hashes of static files can be used to determine the version of a remote Magento installation. Measured in 2015, this resulted in an accurate version identification for 91,7% of 220,000 tested Magento installations worldwide.

See [the resulting hashes](version_hashes.json)

This repo does:

- Generate md5sum from static files of Magento releases
- Calculate the best set of checksums, optimized for coverage and speed (find the right version with the least amount of requests).

The original idea was discussed [here](https://github.com/steverobbins/magescan/issues/77).

# How to rebuild the winning fingerprints

To get accurate results, you need a complete archive of Magento tar.gz files. There is no single source to mirror, so you would have to:

1. Use a Magento partner account to mirror recent Community and Enterprise releases. The [magento-downloader](https://github.com/gwillem/magento-downloader) tool could help.
1. You can find older releases here:

```
wget -r -l 1 -nc -nd -P sources --reject '*latest.tar.gz' -A '*.gz' http://magento.mirror.hypernode.com/releases/
```

Place releases in the `sources` folder, in `ce-full` and `ee-full` subfolders. Then run `generate_md5sums.py` (takes a few minutes) and `find_unique_checksums.py` which will calculate a new `version_hashes.json` for you.

# Contributors

Thanks to Steve Robbins, Sjoerd Langkemper and Ryan Dewhurst!

This code has been ported:

* [PHP](https://github.com/steverobbins/magento-version-identification-php)
* [Ruby](https://gist.github.com/ethicalhack3r/9cc15b914a2866c29db1415730fa910b)



