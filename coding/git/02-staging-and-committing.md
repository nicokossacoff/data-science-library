***
# Staging and committing files

To change a file or add a new one to your Git repo, you first have to **stage** your changes in the **staging area**. Once you have staged all your changes, you can “save/update” the staged changes by **committing** them.

> **Staging** is like writing an email and **committing** is like sending the email. You can change the grammar and add/remove files, but once you sent the email, you cannot change it.

You can stage several versions of your file, but if you only commit the last one, that’s the version that Git is going to “remember”.

To stage a file you have to run the following command on your terminal:
```zsh
git add file-name
```
If you want to stage all files that were modified in the current location, you have to run the following command:
```zsh
git add .
```
To commit all files in the staging area you have to run the following command:
```zsh
git commit -m 'Your message'
```
The `-m` flag adds a message to the current commit. This is very useful for future reference.

If you’ve made several changes to your repo, it’s worth checking which files are already in the staging area and which aren’t. To check the status of your repo, you have to run the following command:
```zsh
git status
```
***
# Comparing Files

You can easily compare the current state of a file (not staged) with the last committed state by running the following command:
```zsh
git diff file-name
```
This provides useful information about the changes made to the file such as lines that were removed, lines that were added, and the location of these lines.
## Output
1. The first line in the output shows two versions of the same file. The old version is called “A” and the new version is called “B”.
2. The second line shows the metadata of the file:
3. The third line assigns a minus sign (-) to A since it’s the old version and a plus sign (+) to B since it’s the new version.
4. Then we have a chunk of lines showing which lines have been modified. The line(s) in red comes from version A and the line(s) in green comes from version B.
5. Before the chunk of lines, we have a chunk header that starts and ends with `@@`.
6. If the set of numbers in the header looks like `-1 +1` it’s because we removed one line from version A (starting at line one) and we added one line in version B (starting at line one).
7. If the set of numbers looks like `-3,4 +3,2` it’s because we extracted four lines from version A (starting at line three) and we added two lines in version B (also starting at line three).

If you want to compare a staged file with the most recent commit version, you have to add the `-r` flag to indicate you want to compare a particular revision of the file:
```zsh
git diff -r HEAD file-name
```