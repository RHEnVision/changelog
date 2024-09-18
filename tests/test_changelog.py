"""Test changelog parses Jira issues properly"""

from rhenvision_changelog.changelog import ProvisioningChangelog
from rhenvision_changelog.commit_check import check_commit

jira_project = "HMS"
commit_head = """a5bc1e0f00aed28102579d14d651a27d5dded4a4
John Doe
jdoe@test.com
1669736056
John Doe
jdoe@test.com
1669736056
HEAD -> branch, origin/branch
701eca9b345a940c8da0bab7fe601666ca9985b9
"""

class StubbedChangelog(ProvisioningChangelog):
    def __init__(self, commit_message):
        self.commit_message = commit_message
        super().__init__('.', 'https://jira.test.com', jira_project)

    def get_log(self) -> str:
        """Get stubbed `git log` output defined by stub passed to constructor.

        Returns:
            The stubbed `git log` in a particular format.
        """
        return commit_head + self.commit_message + "\n\n"+self.MARKER+"\n"

    def get_remote_url(self) -> str:
        return "https://github.com/RHEnVision/provisioning"



def test_jira_issue_parsing() -> int:
    changelog = StubbedChangelog("feat(HMS-123): Subject")
    issue = changelog.commits[0].text_refs["issues"][0]
    print(issue)
    assert changelog.commits[0].convention["scope"] == "[HMS-123](https://jira.test.com/browse/HMS-123)"
