#!/bin/sh


PROG=`basename "$0"`

if [ "$#" -ne 1 ]
then
    cat <<EOF > /dev/stderr
error: missing PULL_REQUEST_NUMBER argument

usage: $PROG PULL_REQUEST_NUMBER

* merge the given pull request with an empty message by invoking "git-pull-request #pr-number -e"
* then update local master with origin master (ff only) by invoking git fetch origin master:master
* checks out master
* then for each merge branch :
    * delete the remote branch with the same name on origin
    * delete the local branch
EOF
    exit 1
fi

set -e
merge-pull-request $1 -e
git fetch origin master:master
git checkout master
git branch --merged|grep master -v|xargs -i git push origin :{}
git branch --merged|grep master -v|xargs git branch -d
