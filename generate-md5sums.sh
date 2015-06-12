#!/bin/bash
for dir in releases/*;
do
	base=$(basename $dir)
	echo Processing $base
	cd releases/$base
	find {js,media,skin} -type f -exec md5sum "{}" \; > ../../md5sums/$base
	cd ../..
done
