
import time
from ghapi.all import GhApi
import os
from datetime import datetime


class ReadmeGenerator:
    def __init__(self, username, sort_list_with_stargazers=False, add_timestamp=False, add_badge=False):
        self.api = self.get_github_api()
        self.username = username
        self.sort_list_with_stargazers = sort_list_with_stargazers
        self.add_timestamp = add_timestamp
        self.add_badge = add_badge


    def get_github_api(self):
        # https://ghapi.fast.ai/fullapi.html
        #github_token = os.environ['GITHUB_TOKEN']
        #api = GhApi(token=github_token)
        api = GhApi()
        return api


    def generate_repositories_table(self, repos, category="favorites", exclude_repos_path="exclude_repos.list"):
        readme = []
        readme.append("| Stars | Forks | Repository | Description |\n")
        readme.append("| ----- | ----- | ---------- | ----------- |\n")

        f = open(exclude_repos_path)
        exclude_repos = f.readlines()

        to_be_deleted = []
        for o in repos:
            if not o["fork"] and o["name"] not in exclude_repos:
                if category is None or category in o["topics"]:
                    readme.append("| {} | {} | [{}]({}) | {} |\n".format(o["stargazers_count"], o["forks_count"], o["name"], o["html_url"], o["description"]))
                    to_be_deleted.append(o)

        filtered_repos = [x for x in repos if (x not in to_be_deleted)]
        return readme, filtered_repos


    def build(self, template_path="TEMPLATE.md", output_path="README.md"):
        f = open(template_path)
        readme = f.readlines()

        categories = {"My Current Favorites": "gh-favorites",
                      "Robotics": "gh-robotics",
                      "Deep Learning / Machine Learning": "gh-dlml",
                      "Miscellaneous": None}

        repos = self.api.repos.list_for_user(username=self.username, per_page=100, sort="pushed")

        if self.sort_list_with_stargazers:
            repos = sorted(repos, key=lambda d: d['stargazers_count'], reverse=True) 

        for c, t in categories.items():
            readme.append("## {}\n".format(c))
            if t == "gh-favorites":
                readme.append("Note: Projects in this section may reappear in other categories.\n")
                new_table, _ = self.generate_repositories_table(repos=repos, category=t)
            else:
                new_table, repos = self.generate_repositories_table(repos=repos, category=t)
            readme.extend(new_table)

        if self.add_timestamp:
            readme.append("\n\n\n")
            readme.append("Last updated: " + str(time.ctime()) + "\n")

        if self.add_badge:
            readme.append("[![automated-profile-updater](https://github.com/{}/{}/actions/workflows/update.yml/badge.svg)](https://github.com/{}/{}/actions/workflows/update.yml)\n".format(self.username,self.username,self.username,self.username))

        f = open(output_path, "w")
        f.writelines(readme)
        f.close()

# Parameters:
rg = ReadmeGenerator(username="salihmarangoz", sort_list_with_stargazers=False, add_timestamp=True, add_badge=True)
rg.build()