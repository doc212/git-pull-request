#!/bin/sh


###################################################################
#
# You can change some values here if you have "non-standard" needs
#
###################################################################

#the command to invoke merge.py
MERGE=merge-pull-request

#the remote name
ORIGIN=origin

#the master branch name
MASTER=master

###################################################################

PROG=`basename "$0"`

if [ "$#" -ne 1 ]
then
    cat <<EOF > /dev/stderr
error: missing PULL_REQUEST_NUMBER argument

usage: $PROG PULL_REQUEST_NUMBER

* merge the given pull request with an empty message by invoking "$MERGE #pr-number -e"
* then update local branch $MASTER with branch with the same name on the remote ($ORIGIN) (ff only) by invoking git fetch $ORIGIN $MASTER:$MASTER
* checks out $MASTER
* then for each merged branch :
    * delete the remote branch with the same name on $ORIGIN
    * delete the local branch
EOF
    exit 1
fi

set -e

echo $ merge-pull-request $1
merge-pull-request $1 -e

echo $ git fetch $ORIGIN $MASTER:$MASTER
git fetch $ORIGIN $MASTER:$MASTER
echo $ git checkout $MASTER
git checkout $MASTER

echo $ delete remote merged branches
git branch --merged|grep $MASTER -v|xargs -i git push $ORIGIN :{}

echo $ delete local merged branches
git branch --merged|grep $MASTER -v|xargs git branch -d
