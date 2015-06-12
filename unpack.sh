 for x in *.gz; do base=$(basename $x .tar.gz); tar xf $x && mv magento $base; done
