import re
import sys
import os.path
from pathlib import Path
from typing import Dict

from git_changelog import templates
from git_changelog.build import Changelog
from git_changelog.providers import GitHub, RefDef, RefRe

RefRe.BBB = r"(?:^|[\s,]|\(|/)"  # blank or bracket before
RefRe.BBA = r"(?:[\s,]|$)|\)"  # blank or bracket after
RefRe.JIRA_ISSUE = r"(?P<jira_project>HMS[A-Z]*)-(?P<ref>[1-9]\d*)"  # forces the HMS jira project prefix for now

class GitHubJiraProvider(GitHub):
    REF: Dict[str, RefDef] = {
        **GitHub.REF,
        "issues": RefDef(
            regex=re.compile(RefRe.BBB + RefRe.JIRA_ISSUE + RefRe.BBA),
            url_string=("{jira_url}/browse/{jira_project}-{ref}"),
        ),
    }

    def __init__(self, namespace: str, project: str, jira_url: str, jira_project: str):
        self.jira_url = jira_url
        self.jira_project = jira_project
        super().__init__(namespace, project)

    def build_ref_url(self, ref_type: str, match_dict: Dict[str, str]) -> str:  # noqa: D102 (use parent docstring)
        match_dict["jira_url"] = self.jira_url
        if not match_dict.get("jira_project"):
            match_dict["jira_project"] = self.jira_project
        return super().build_ref_url(ref_type, match_dict)


class ProvisioningChangelog(Changelog):
    """A class to represent a Provisioning common project changelog."""

    def __init__(self, repository: str, jira_url: str, jira_project: str, limit=None):
        self.limit = limit

        # setting repository here before super() for the get_remote_url to work
        self.repository: str = repository
        remote_url = self.get_remote_url()
        split = remote_url.split("/")
        namespace, project = "/".join(split[3:-1]), split[-1]

        provider = GitHubJiraProvider(namespace, project, jira_url, jira_project)
        super().__init__(repository, provider=provider, style="angular")

    def get_log(self) -> str:
        """Get the `git log` output possibly limited by limit passed to constructor.

        Returns:
            The output of the `git log` command, with a particular format.
        """
        if self.limit:
            return self.run_git("log", "-"+str(self.limit), "--date=unix", "--format=" + self.FORMAT)
        return super().get_log()
