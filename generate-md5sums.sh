#!/bin/bash
for dir in releases/*;
do
	base=$(basename $dir)
	md5file=$(echo $base | sed -e 's/magento-/magento-CE-/')
	echo Processing $base to $md5file

	cd releases/$base
	find {js,media,skin} -type f -exec md5sum "{}" \; > ../../md5sums/$md5file
	cd ../..
done
