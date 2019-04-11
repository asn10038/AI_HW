for line in $(cat /tmp/image_urls.txt)
do
  wget $line
done
