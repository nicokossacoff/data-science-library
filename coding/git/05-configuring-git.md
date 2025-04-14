***
# Level of Settings

You can access a list of customizable settings, you have to run the following command:
```zsh
git config --list
```
Git has three levels of settings:
- You can customize the settings of one specific project using the `--local` flag.
- You can customize the settings of all your projects using the `--global` flag.
- You can customize the settings for every user on your computer using the `--system` flag.

Each level overrides the values in the previous level. The _local_ level overrides the values in the _global_ level, which overrides the values in the _system_ level.
# Using aliases

You can use aliases for the most repeated commands. You have to set up this aliases through global settings, by running the following command:
```zsh
git config --global alias.unstage 'reset HEAD'
```
Now, to un-stage a file you have to run the following command:
```zsh
git unstage file-name
```
# Set-up an SSH key

SSH keys are a pair of public and private keys used to securely connect to remote servers. The private key stays on your machine, and the server uses the matching public key to confirm it's really you.
When using Git over HTTPS, you’ll need to enter your GitHub username and password every time you push. With SSH, once your public key is added to GitHub, you're good to go—no more typing credentials every time.

To create an SSH key you have to run the following command:
```zsh
ssh-keygen -t rsa -b 4096 -C 'nicokossacoff@gmail.com'
```
After creating the SSH key, you have to add it to the SSH agent:
```zsh
ssh-add ~/.ssh/id_rsa
```
