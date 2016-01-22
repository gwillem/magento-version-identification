#!/bin/bash

cd sources
for x in *.gz; do
	base=$(basename $x .tar.gz);
	echo Parsing $base
	target=../releases/$base
	test -e $target && continue 
	echo Unzipping
	mainfolder=$(tar tfz $x | head -1)
	if [ "$mainfolder" == "magento/" ]; then
		echo found magento root
		tar xf $x && mv magento $target
	else
		echo found no magento root
		mkdir -p $target
		tar xf $x -C $target
	fi
	# (tar xf $x && mv magento $target);
done
cd ..
