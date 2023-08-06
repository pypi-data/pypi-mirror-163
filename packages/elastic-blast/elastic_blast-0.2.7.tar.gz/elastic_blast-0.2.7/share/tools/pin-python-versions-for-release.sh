#!/bin/bash
# share/tools/pin-python-versions-for-release.sh: Tool to pin python module
# dependencies before ElasticBLAST releases
#
# Author: Christiam Camacho (camacho@ncbi.nlm.nih.gov)
# Created: Wed 10 Aug 2022 06:01:40 PM EDT
set -ex
TMP=`mktemp -t $(basename -s .sh $0)-XXXXXXX`
trap " /bin/rm -fr $TMP " INT QUIT EXIT HUP KILL ALRM

pin_dependency_versions() {
    fname=$1
    truncate -s 0 $TMP
    pip freeze -r $fname > $TMP
    n=`egrep -n '^##' $TMP | awk -F: '{print $1}'`
    head -n $(($n-1)) $TMP >| $fname
}

pin_dependency_versions requirements/base.txt
pin_dependency_versions requirements/test.txt
