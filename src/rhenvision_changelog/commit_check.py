import sys

def check_commit(commit, jira_project, length_limit=70) -> int:
    if len(commit.subject) > length_limit:
        sys.stderr.write("ERROR: Commit message length too long (limit is " + length_limit + "): " + commit.subject + "\n")
        return 1

    if commit.convention["type"] == "":
        sys.stderr.write("ERROR: Commit message must have a type 'type: subject': " + commit.subject + "\n")
        return 2

    if commit.convention["type"] in ["Features", "Bug Fixes"]:
        if commit.convention["scope"] is not None and jira_project not in commit.convention["scope"]:
            sys.stderr.write("ERROR: Scope for Feature and Bug fix needs to be Jira issue in format '"+jira_project+"-XXX': " + commit.convention["scope"] + "\n")
            return 2

        if "issues" not in commit.text_refs or len(commit.text_refs["issues"]) == 0:
            sys.stderr.write("ERROR: Feature and bug fix must have a Jira issue linked\n")
            sys.stderr.write("ERROR: You can link the issue either in subject as 'feat("+jira_project+"-XXX): subject': " + commit.subject+"\n")
            sys.stderr.write("ERROR: or anywhere in the body preferably as 'Fixes: "+jira_project+"-XXX' or Refs: "+jira_project+"-XXX\n")
            return 3

    return 0
