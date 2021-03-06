# Git pull-request

A script written in Python to merge git branches by doing pull requests in GitHub.

## Installation and usage

The standalone script `merge.py` can be used directly to merge pull requests by number.
Try `merge.py --help` for more info.

However, what it does is simply merge pull requests in GitHub.
Your local branch still exists, as does the merged remote branch.
And your local master is not updated.

To some extent, the script `merge.sh` does that for you (implemented in [issue #4](https://github.com/doc212/git-pull-request/issues/4)).
But it requires that you copy (or link) `merge.py` somewhere in your `PATH` under the name `merge-pull-request` (to bypass this or use a different name, see [Customization](Customization) below).

You can then invoke merge.sh like this:

    merge.sh PULL_REQUEST_NUMBER

For easier use, you should put `merge.sh` somewhere in your `PATH` under a friendly name like `mpr`

### What `merge.sh` does

* merge the given `PULL_REQUEST_NUMBER` with an empty message by invoking `merge-pull-request PULL_REQUEST_NUMBER -e`
* update local `master` with `origin`'s `master` (ff only) by invoking `git fetch origin master:master`
* checks out `master`
* then for each merge branch :
    * delete the remote branch with the same name on `origin`
    * delete the local branch

### Customization

By editing some variables in `merge.sh`, it is easily possible to customize:
* the command issued to invoke `merge.py` (default: `merge-pull-request` but you can change it to the full path to  `merge.py` or another alias in your `PATH`)
* the remote name (default: `origin`)
* the master branch (default: `master`)
