# -*- coding: utf-8 -*-
"""
clone_forks.py

Find all forks of a GitHub repository, then
locally clone them to a specified directory.
Also output a CSV of forks to that directory.

Arguments:
    --forksurl: URL for GitHub API to retrieve desired forks.
        Defaults to https://api.github.com/repos/CS410Assignments/CourseProject/forks
    --forksdest: Local top-level folder to clone to.
        Defaults to subfolder "repo_forks" of the directory this script is in.
    --outputfile: path and name of the output list of forks. Format is CSV.
        Defaults to "repo_forks.csv" in the same folder as this script.
    --doclone: whether to perform cloning step. "yes" to clone, "no" to simply collect info about the forks.
        Default is "yes".
    --minmonthsold: only process forks that were last pushed at least this number of months ago.
        Default = 0.

Heavily based on findforks.py by Anand Kumria:
    https://github.com/akumria/findforks

Created on Sat Oct 30 14:09:23 2021

@author: ktuoh
"""

import argparse
import json
#import subprocess
import urllib.error
import urllib.parse
import urllib.request
import os
import pandas as pd
from datetime import datetime
from datetime import date
import git

def find_forks(forks_url):
    """
    Query the GitHub API for all forks of a repository.
    """
    resp_json = []

    try:
        resp = urllib.request.urlopen(forks_url)
    except urllib.error.HTTPError as e:
        if e.code == 404:
            raise StopIteration

    resp_json += json.loads(resp.read())

    while github_resp_next_page(resp):
        resp = urllib.request.urlopen(github_resp_next_page(resp))
        resp_json += json.loads(resp.read())
        
    # Pull information about each fork into a dataframe
    # Used ShikharDua's solution: https://stackoverflow.com/questions/10715965/create-a-pandas-dataframe-by-appending-one-row-at-a-time
    forks_list = []
    
    for fork in resp_json:
        fork_dict = {
            "owner_login": fork["owner"]["login"],
            "path": fork["full_name"],
            "pushed_at": datetime.strptime(fork["pushed_at"], "%Y-%m-%dT%H:%M:%SZ"),
            "ssh_url": fork["ssh_url"],
            "project_url": fork["svn_url"],
            "default_branch": fork["default_branch"]
            }
        
        forks_list.append(fork_dict)
        
    # Return dataframe of forks.
    return pd.DataFrame(forks_list)
        

def github_resp_next_page(resp):
    """
    Check to see if the GitHub response has a next link.
    If the response, look for the 'link' header and see if
    there is a value pointed to by next.
    """
    link_header = resp.getheader(u"link")

    if not link_header:
        return None

    rel_next = u'rel="next"'
    for link in link_header.split(u","):
        if rel_next in link:
            return link[link.find(u"<") + 1:link.rfind(u">")]

    return None


def min_months_old_met(date_1, date_2, min_months_old):
    """
    Determine whether two dates are at least min_months_old months apart.
    Assume date_2 is greater than date_1.
    Solution from https://www.tutorialsrack.com/articles/451/how-to-get-the-number-of-months-between-two-dates-in-python
    """
    return ((date_2.year - date_1.year) * 12) + (date_2.month - date_1.month) >= int(min_months_old)


def shallow_clone_forks(forks_df, destination, min_months_old):
    """
    Given a dataframe of Git repo forks, clone all forks that are at least min_months_old.
    Clone them to the "destination" folder. Use depth = 1 for a shallow clone.
    """
    
    current_date = date.today() # Baseline for gauging age of last repo push
    
    # Loop through forks
    for index, fork in forks_df.iterrows():
        
        # Clone forks at least min_months_old
        if min_months_old_met(fork["pushed_at"], current_date, min_months_old):
            
            # Create subfolder for owner_login if it doesn't already exist
            
            fork_destination = os.path.join(destination, fork["owner_login"])
            if (not os.path.isdir(fork_destination)):
                try:
                    os.makedirs(fork_destination)
                    git.Repo.clone_from(fork["ssh_url"], fork_destination, branch=fork["default_branch"], depth=1)
                except Exception:
                    print("Error cloning ", fork["ssh_url"])
                    continue
            


def main():
    
    # Get folder this script is running from
    script_dir = os.path.dirname(__file__).replace("\\", "/")
    
    # Get any provided arguments. Use defaults for any not provided
    parser = argparse.ArgumentParser()
    parser.add_argument("--forksurl", help="URL for GitHub API to retrieve desired forks", default="https://api.github.com/repos/CS410Assignments/CourseProject/forks")
    parser.add_argument("--forksdest", help="Local top-level folder to clone to", default=os.path.join(script_dir, "repo_forks"))
    parser.add_argument("--outputfile", help="CSV output list of forks", default=os.path.join(script_dir, "repo_forks.csv"))
    parser.add_argument("--doclone", help="Whether to perform cloning step", default="yes")
    parser.add_argument("--minmonthsold", help="The minimum number of months since a repo was last pushed", default=0)
    args = parser.parse_args()
    
    # Get dataframe of forks
    forks_df = find_forks(args.forksurl)
    
    # First create the destination path if it doesn't exist.
    if (not os.path.isdir(args.forksdest)):
        os.makedirs(args.forksdest)

    # Output dataframe of forks.
    forks_df.to_csv(args.outputfile, index=False)
    
    # If desired, clone forks of at least minimum age
    if (args.doclone == "yes"):
        shallow_clone_forks(forks_df, args.forksdest, args.minmonthsold)


if __name__ == "__main__":
    main()