#!/bin/bash
set -e -x

package_name=densefog

echo 'prepare...'
rpmbuild_dir=/root/rpmbuild
ln -s `pwd`/contrib $rpmbuild_dir

version=`python setup.py --version | tail -n1`
release=1

spec=$package_name.spec
sed -i "2i\%define version ${version}\n%define release ${release}" contrib/SPECS/$spec

echo 'rpmbuild...'
python setup.py sdist
cp dist/$package_name-$version.tar.gz contrib/SOURCES

# yum-builddep -y contrib/SPECS/$spec
rpmbuild -ba contrib/SPECS/$spec

echo 'uploading...'
wget http://192.168.31.110:8080/upload.py
for filename in `find ./ -name *.rpm`
do
    if [[ "$version" =~ "dev" ]]; then
        python upload.py -f $filename -r develop
    else
        python upload.py -f $filename -r staging
    fi
done
