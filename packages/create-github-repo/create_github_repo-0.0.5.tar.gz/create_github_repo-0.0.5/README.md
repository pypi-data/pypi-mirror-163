# create-github-repo

![GitHub release (latest by date)](https://img.shields.io/github/v/release/geocoug/create-github-repo)
[![pre-commit.ci](https://results.pre-commit.ci/badge/github/geocoug/create-github-repo/main.svg)](https://results.pre-commit.ci/latest/github/geocoug/create-github-repo/main)
[![GitHub Super-Linter](https://github.com/geocoug/create-github-repo/workflows/lint%20code%20base/badge.svg)](https://github.com/marketplace/actions/super-linter)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
![license](https://img.shields.io/github/license/geocoug/create-github-repo)

Simple CLI to initialize repos on GitHub using Python.

## Example Usage

- Create a new public repository (-p) called `New-Repository` with the description (-d) `My new Repository`.
- Use GitHub credentials stored in a local file (-f) called `github.txt` to authenticate with the GitHub API.
- Interactively confirm or revert changes (-r).

```bash
$ python -m pip install create_github_repo

$ python -m create_github_repo -f github.txt -d "My new repo" -p -r "Test Repository"

Created: https://github.com/geocoug/Test-Repository
Attributes:
  visibility: public
  created_at: 2022-08-16 12:39:33
  description: My new repo
Do you want to keep these changes [Y/n]: y
```
