cd sources
for x in *.gz; do
	base=$(basename $x .tar.gz);
	target=../releases/$base
	test -e $target || (tar xf $x && mv magento $target);
done
cd ..
