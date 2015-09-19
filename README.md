# Git pull-request

A script written in Python to merge git branches by doing pull requests in GitHub.

## Installation and usage

The standalone script `merge.py` can be used directly to merge pull requests by number.
Try `merge.py --help` for more info.

However, what it does is simply merge pull requests in in GitHub.
Your local branch still exists, as does the merged remote branch.
And your local master is not updated.

To some extent, the script `merge.sh` does that for you (implemented by #4).
But it requires that you copy (or link) merge.py somewhere in your `PATH` under the name `merge-pull-request`

You can then invoke merge.sh like this:

    merge.sh PULL_REQUEST_NUMBER

For easier use, you should put `merge.sh` somewhere in your `PATH` under a friendly name like `mpr`

### What `merge.sh` does

* merge the given pull request with an empty message by invoking `merge-pull-request #pr-number -e`
* then update local master with origin master (ff only) by invoking git fetch origin master:master
* checks out master
* then for each merge branch :
    * delete the remote branch with the same name on origin
    * delete the local branch

### Customization

By editing some variables in `merge.sh`, it is easily possible to customize:
* the command issued to invoke merge.py (default: `merge-pull-request`)
* the remote name (default: `origin`)
* the master branch (default: `master`)
