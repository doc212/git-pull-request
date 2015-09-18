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

echo $ merge-pull-request $1
merge-pull-request $1 -e

echo $ git fetch origin master:master
git fetch origin master:master
echo $ git checkout master
git checkout master

echo $ delete remote merged branches
git branch --merged|grep master -v|xargs -i git push origin :{}

echo $ delete local merged branches
git branch --merged|grep master -v|xargs git branch -d
