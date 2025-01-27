# Collect Text from Past CS 410 Project Files

## Overview

These are the scripts which harvest text from document files of past CS 410 projects. That text will be used for further analysis.

To harvest the text, first run `clone_forks.py` as below to clone forks of the base CS 410 project repository. Then run `get_project_text.py` to collect text from the clones.

## Requirements

Git must be installed for `clone_forks.py` to work. This project used git version 2.17.1.windows.2.

The scripts were tested and run on macOS Big Sur and in an Anaconda Python 3.8.8 virtual environment.

Python packages used:
* beautifulsoup4 4.10.0
* datetime 4.3
* docx2txt 0.8
* pymupdf 1.19.1
* fitz 0.0.1.dev2
* GitPython 3.1.24
* markdown 3.3.4
* pandas 1.2.4
* python-pptx 0.6.21
* unidecode 1.3.2* 

## Scripts

### `clone_forks.py`

Takes a URL of GitHub forks from the main CS 410 project and returns a CSV of information and links to each project. Optionally gets shallow clones of projects that were last pushed more than n months ago.

The functionality to walk through forks of a Github project comes from the [findforks repo](https://github.com/akumria/findforks) by Anand Kumria.

#### Arguments

Call `clone_forks.py` with no arguments to use default settings.

* `--forksurl`: URL for GitHub API to retrieve desired forks. Default: <https://api.github.com/repos/CS410Assignments/CourseProject/forks>
* `--destination`: local top-level folder to clone to. Defaults to subfolder "repo_forks" of the directory the script is in.
* `--doclone`: whether to perform cloning step. "yes" to clone, "no" to simply collect info about the forks. Defaults to "yes". 
* `--minmonthsold`: only clone forks that were last pushed at least this number of months ago. Defaults to 0.

#### Output
* When `--doclone` is "yes", shallow clones of GitHub repos more than `--minmonthsold` months old.
* `repo_forks.csv`: file of information about each fork. Will be used in the following step to help harvest text.

#### Usage

```
python ./clone_forks.py --forksurl "https://api.github.com/repos/CS410Assignments/CourseProject/forks" --destination "./repo_forks" --doclone "yes" --minmonthsold 0
```

### `get_project_text.py`

Given a `repo_forks.csv` file (see above) and a directory of cloned repositories, harvests text from document files at the top level of each repository. Processes PDFs, Word documents, Powerpoint documents, and markdown files.

The script converts sequences of whitespace characters into single space characters. The script also converts non-ASCII Unicode characters to their closest ASCII equivalents.

#### Arguments

Call `get_project_text.py` with no arguments to use default settings.

* `--projectlist`: CSV file containing information about the cloned CS 410 projects. Helps associate project URLs with harvested text. Defaults to "repo_forks.csv" in the same folder as the script.
* `--projectroot`: folder containing cloned CS 410 projects. Walks through the top level of each project directory and harvests textual documents. Defaults to subfolder "repo_forks" of the directory the script is in.
* `--outputdir`: Destination directory of output files. Defaults to the script's folder.

#### Output
* `project_file_text.tsv`: tab-delimited file of project URLs, filenames, and the text harvested from those files. One row per project file.
* `project_text.tsv`: same as above, but with a single line per project. Concatenates text from each project's files.

#### Usage
```
python ./get_project_text.py --projectlist "./repo_forks.csv" --projectroot "./repo_forks" --outputdir "."
```

### Troubleshooting

If there are any errors are encountered related to the `pymupdf` module, please try uninstalling and re-installing the module using pip (or any other module manager you might be using).