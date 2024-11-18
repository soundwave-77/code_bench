from itertools import chain
from typing import Any, Iterable

from github import Auth, Github
from github.Repository import Repository
from tqdm import tqdm

from constants import GET_ISSUES_FROM_PULL_QUERY


class Client:
    def __init__(
        self,
        repo_names: list[str] | None = None,
        languages: list[str] | None = None,
        access_token: str | None = None,
    ):
        self.github_client: Github = (
            Github(auth=Auth.Token(access_token)) if access_token else Github()
        )

        if repo_names is None and languages is None:
            raise ValueError(
                "One of the parameters `repos` or `languages` must be specified"
            )

        repositories = None

        if languages:
            repositories: list[Repository] = list(
                self._join_sequences(
                    (
                        list(
                            self.github_client.search_repositories(
                                query=f"language:{language}"
                            )
                        )
                        for language in languages
                    )
                )
            )

        if repo_names:
            repo_names = set(repo_names)
            if repositories:
                filtered_repositories: list[Repository] = [
                    repo for repo in repositories if repo.full_name in repo_names
                ]
            else:
                filtered_repositories: list[Repository] = [
                    self.github_client.get_repo(repo_name) for repo_name in repo_names
                ]

            repositories = filtered_repositories

        self.repositories: dict[str, Repository] = {
            repo.full_name: repo for repo in filtered_repositories
        }

    def _join_sequences(self, sequences: Iterable[Iterable]) -> Iterable:
        return chain.from_iterable(sequences)

    def get_issue_pulls(
        self, pull_state: str = "all", limit: int = 100
    ) -> dict[str, list[dict]]:
        issue_pulls: dict[str, list[dict]] = {}
        for repo in self.repositories.values():
            repo_pulls: dict[int, list[int]] = {}
            for pull in tqdm(repo.get_pulls(state=pull_state)[:limit]):
                query_params: dict[str, Any] = {
                    "repoOwner": repo.owner.login,
                    "repoName": repo.name,
                    "pullNumber": pull.number,
                }
                _, response = self.github_client.requester.graphql_query(
                    GET_ISSUES_FROM_PULL_QUERY, query_params
                )
                issues: dict[str, Any] = response["data"]["repository"]["pullRequest"][
                    "closingIssuesReferences"
                ]["nodes"]
                for issue in issues:
                    if issue["number"] not in repo_pulls:
                        repo_pulls[issue["number"]] = []
                    repo_pulls[issue["number"]].append(pull.number)
            issue_pulls[repo.full_name] = [
                {"issue": issue_number, "pull_requests": pulls_list}
                for issue_number, pulls_list in repo_pulls.items()
            ]
        return dict(issue_pulls)
