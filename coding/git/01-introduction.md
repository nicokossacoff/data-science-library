***
# What is version control?

**Version control** is a system that tracks changes to a file or directory over time. You can then revert a file to a previous state, revert the whole directory back to a previous state, manage who made changes to the files, etc.
The most important thing is that allows multiple people to work and make changes to the same directory, without over writing their work.
***
# How Git stores data?

## Files in a Git repository

Every Git repository could be divided into two parts:
1. The first part contains all our files and directories. Here we could find a markdown file with documentation, a directory to store important data, etc.
2. The second part contains all the information that Git uses to track the project’s history. This information is stored in a directory called `.git`.
   Whenever you clone a repo, you will copy all the project’s history until that moment and that information is stored in the `.git` directory. This is very useful because if the server that contains the repo goes down, you can upload your local repo with all the project’s history included.
## Snapshots

Git thinks of its data as a series of snapshots of a project. Every time you save the current state of your project, Git “takes a picture” of all the files at that moment and stores the reference to that snapshot.
The good thing is that Git does not store files that haven’t changed. Instead, it stores a link to the previous identical file that has been stored.