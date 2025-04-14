***
# Fetching data

You can fetch data from a remote repo by running the `git fetch` command, followed by the name of the remote (which is usually called `origin`) and the name of the local branch (which is usually called `master`).
```zsh
git fetch origin main
```
## Difference between `git fetch` and `git pull`

The `git fetch` command downloads new commits from your remote repo without merging them into your local repo. This command is useful because you can review the commits that were made in the remote repo before merging. After fetching the data, you have to perform a `git merge` to add the changes to your local repo.
The `git pull` command combines this workflow into a single command by automatically fetching for commits in the remote repo and then merging them. However, this can cause problems:
- If we did a commit in our local branch and we fetch new commits, then our local and remote branches will diverge. In this case, merging is not that simple, so it's always better to first fetch the commits, check the files for possible conflicts, and then merge the two branches.
- You can specify the merging method:
	- If you add the `--rebase` flag, Git will perform a **rebase**. A rebase will allow you to combine commits from one branch to another by moving a group of commits to a new base. For example, it moves the commits in your local branch _after_ the commits in the remote branch.
	- If you add the `--ff` flag (short for _fast-forward_), Git will perform a traditional merge.
	- If you add the `--ff-only` flag, Git will fetch the commits from your remote repo but it won't perform a merge if detects that branches are diverging. You have to figure out what are the divergencies and merge both branches as you think is more convenient.