"""Test commit check validates Jira issues properly"""

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
    assert check_commit(changelog.commits[0], jira_project) == 0
    changelog = StubbedChangelog("feat: Subject\nFixes: HMS-123")
    assert check_commit(changelog.commits[0], jira_project) == 0

    # allows different HMS projects - legacy reasons
    changelog = StubbedChangelog("feat: Subject\nRefs: HMSJIRA-123")
    assert check_commit(changelog.commits[0], jira_project) == 0
    changelog = StubbedChangelog("feat(HMSJIRA-123): Subject")
    assert check_commit(changelog.commits[0], jira_project) == 0

    # allows link to ticket in the commit body
    changelog = StubbedChangelog("feat: Subject\njira.test.com/browse/HMS-123")
    assert check_commit(changelog.commits[0], jira_project) == 0

    # no issue link necessary for other types
    changelog = StubbedChangelog("build: Subject")
    assert check_commit(changelog.commits[0], jira_project) == 0

    # issue link needed for feat and fix
    changelog = StubbedChangelog("feat: Subject")
    assert check_commit(changelog.commits[0], jira_project) != 0
    changelog = StubbedChangelog("fix: Subject")
    assert check_commit(changelog.commits[0], jira_project) != 0
