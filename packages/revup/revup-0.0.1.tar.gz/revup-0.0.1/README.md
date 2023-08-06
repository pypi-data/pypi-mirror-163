![Revup](docs/images/revup_light.png#gh-light-mode-only)
![Revup](docs/images/revup_dark.png#gh-dark-mode-only)
<p align="center">
<a href="https://github.com/Skydio/revup"><img alt="Source Code" src="https://img.shields.io/badge/source-code-blue" /></a>
<a href="https://github.com/Skydio/revup/issues"><img alt="Issues" src="https://img.shields.io/badge/issue-tracker-blue" /></a>
<img alt="Python 3.8 | 3.9 | 3.10" src="https://img.shields.io/pypi/pyversions/revup" />
<a href="https://github.com/Skydio/revup/tree/main/LICENSE"><img alt="MIT License" src="https://img.shields.io/pypi/l/revup" /></a>
</p>

Revup is a Python command-line toolkit for speeding up your git workflow. It provides commit-based development support and full github integration.

## Features

<Add animated gif here>
  
- Create multiple standalone and/or relative github PRs with a single command
- Uses "true" relative PRs that target the actual base branch and can be merged manually or by CI
- Rebase detection saves time and CI cost by not re-pushing if the patch hasn't changed
- Add reviewers, labels, and create drafts all from the commit text
- Adds auto-updating "review graph" and "patchsets" comments to PRs to aid reviewers
- "amend" and "restack" save time by eliminating slow rebases

## Compatibility

Revup requires Python 3.8 or higher and git 3.6 or higher. Revup works with Linux, OSX, and Windows.

## Installing

Install with `pip` or your favorite package manager.

```sh
python -m pip install revup
```

Verify that installation was successful

```sh
revup -h
```

## First time setup

On first run, revup will prompt you to add github credentials
```sh
revup upload
```
When creating the OAuth, revup requires "full repo permissions"
<IMG HERE>

## Tutorial

# Creating PRs
Upload uses tags in the commit message to set attributes of each PR. To make revup create a PR from a commit, add a "Topic" tag:

```
Hello revup!

My first revup commit.

Topic: hello_revup
```
Multiple commits can be added to a single PR, just add the same topic label to each one.
  
To make a PR that is relative to a previous PR, add a Relative label specifying the topic of the PR to be relative to.
  
With these basic tags, you can make any number of interspersed independent and dependent PRs.
  
# Updating PRs
  
  
# Working on other branches
  
# Review graph and patchsets
  

  


## Commit Based Development

This workflow has gone by many names as it has been rediscovered over the years; you may know it as "stacked diffs", "patch based" or "".

If you've used tools such as Gerrit, Phabricator, or git mailing lists, you may already be familiar with the style of development. If not, here are some well written summaries of the methodologies and advantages of such a style.

## Peer Projects 

Revup is inspired in part by this non-exhaustive list of open source projects that also support a patch based workflow:
  
# ghstack
  
## License

## Contributing & Support



