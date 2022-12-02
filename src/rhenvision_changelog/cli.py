import argparse

from typing import List, Optional
from pathlib import Path

from git_changelog import templates

from rhenvision_changelog.changelog import ProvisioningChangelog
from rhenvision_changelog.commit_check import check_commit

JIRA_URL = "https://issues.redhat.com"
JIRA_PROJECT = "HMSPROV"

def get_parser() -> argparse.ArgumentParser:
    """
    Return the CLI argument parser.
    Returns:
        An argparse parser.
    """
    parser = argparse.ArgumentParser(
        add_help=True, prog="rhenvision-changelog", description="Command line tool for rhenvision-changelog Python package."
    )
    parser.add_argument("repository", metavar="REPOSITORY", help="The repository path, relative or absolute.")
    return parser


def write_changelog(args: Optional[List[str]] = None) -> int:
    parser = get_parser()
    opts = parser.parse_args(args=args)

    changelog = ProvisioningChangelog(opts.repository, JIRA_URL, JIRA_PROJECT)
    template = templates.get_template("angular")
    rendered = template.render(changelog=changelog)

    # sys.stdout.write(rendered)
    with open(Path(opts.repository).joinpath("CHANGELOG.md"), "w") as stream:
      stream.write(rendered)

    return 0


def run_check_commit(args: Optional[List[str]] = None) -> int:
    length_limit = 70
    changelog = ProvisioningChangelog('.', JIRA_URL, JIRA_PROJECT, limit=1)
    return check_commit(changelog.commits[0], JIRA_PROJECT, length_limit=length_limit)
