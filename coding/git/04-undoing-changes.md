***
Suppose that you have three files in your staging area (figure below) but you only want to commit two of them. In that case, you must:
1. Un-stage the file back to your repo.
2. Commit the remaining files in the staging area.
3. Do the changes needed in the first file, stage it and then commit it.
![unstage-files](unstage-files.png)
## Un-stage a single file

To un-stage a single file from the staging area, you must run the following command:
```zsh
git reset HEAD file-name
```
## Un-staged all files

To un-stage all files in the staging area, you must run the same command as above but without specifying any file name:
```zsh
git reset HEAD
```
## Undo changes in an un-staged file

To undo changes to a file that's not in the staging area, we use the `git checkout` command. This will revert the file back to the version in the last commit.
```zsh
git checkout -- file-name
```
If you want to revert all files in the repo (including current working directory and sub-directories) to their previous version, you must use the following command:
```zsh
git checkout .
```
Note that this command should be run from the root directory in order to work.

You can revert an un-staged file to a specific version by replacing the two dashes with the hash code to the commit:
```zsh
git checkout dc9d8fac file-name
```
or using the `HEAD` flag:
```zsh
git checkout HEAD~1 file-name
```