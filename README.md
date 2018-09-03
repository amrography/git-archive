# git-archive
Create a zip archive of files from current commit to latest commit you zipped.

It required `git` module to be installed, `pip3 install git`

## How to use
1. Clone this repo
2. Copy the `git_archive` folder to your git repo folder
3. Navigate to `git_archive folder` and run `python3 archive.py`
4. Enter the full commit hash you want to start from

## Notice
* The new archive created in sub directory inside git_archive folder
* Use `--flush` to initalize the storage file, you will be asked to enter a commit hash again
