# Collect Text from Past CS 410 Project Files

## Overview

This is a skeletal ReadMe for the scripts which harvest text from document files of past CS 410 projects. That text will be used for further analysis.

## Scripts

### `clone_forks.py`

Takes a URL of GitHub forks from the main CS 410 project and returns a CSV of information and links to each project. Optionally gets shallow clones of projects that were last pushed more than n months ago.

#### Arguments
* `--forksurl`: URL for GitHub API to retrieve desired forks
* `--destination`: local top-level folder to clone to
* `--doclone`: whether to perform cloning step. "yes" to clone, "no" to simply collect info about the forks.
* `--minmonthsold`: only clone forks that were last pushed at least this number of months ago.

#### Output
* When `--doclone` is "yes", shallow clones of GitHub repos more than `--minmonthsold` months old.
* `repo_forks.csv`: file of information about each fork. Will be used in the following step to help harvest text.

#### Example Usage

```
python ./clone_forks.py --forksurl "https://api.github.com/repos/CS410Assignments/CourseProject/forks" --destination "./Past_Projects" --doclone "yes" --minmonthsold 3
```

### `get_project_text.py`

Given a `repo_forks.csv` file (see above) and a directory of cloned repositories, harvests text from document files at the top level of each repository. Processes PDFs, Word documents, Powerpoint documents, and markdown files.

#### Arguments
* `--projectlist`: CSV file containing information about the cloned CS 410 projects. Helps associate project URLs with harvested text.
* `--projectroot`: folder containing cloned CS 410 projects. Walks through the top level of each project directory and harvests textual documents.

#### Output
* `project_file_text.tsv`: tab-delimited file of project URLs, filenames, and the text harvested from those files. One row per project file.
* `project_text.tsv`: same as above, but with a single line per project. Concatenates text from each project's files.

#### Example Usage
```
python ./get_project_text.py --projectlist "./Past_Projects/repo_forks.csv" --projectroot "./Past_Projects"
```
