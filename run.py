from ghapi.all import GhApi
from time import ctime

class ReadmeGenerator:
    def __init__(self, username, sort_list_with_stargazers=False, add_timestamp=False, add_badge=False, mobile_url="", desktop_url=""):
        self.api                       = self.get_github_api()
        self.username                  = username
        self.sort_list_with_stargazers = sort_list_with_stargazers
        self.add_timestamp             = add_timestamp
        self.add_badge                 = add_badge
        self.mobile_url                = mobile_url
        self.desktop_url               = desktop_url
        self.categories                = {
            "My Current Favorites"             : "gh-favorites",
            "Robotics"                         : "gh-robotics",
            "Deep Learning / Machine Learning" : "gh-dlml",
            "Miscellaneous"                    : None
        }

        self.repos = self.api.repos.list_for_user(username=self.username, per_page=100, sort="pushed")

        if self.sort_list_with_stargazers:
            self.repos = sorted(self.repos, key=lambda data: data['stargazers_count'], reverse=True) 

        self.build_desktop(use_repocards=False)
        self.build_mobile(use_repocards=True)

    def get_github_api(self):
        # https://ghapi.fast.ai/fullapi.html
        # github_token = os.environ['GITHUB_TOKEN']
        # api = GhApi(token=github_token)
        api = GhApi()
        return api

    def __generate_repositories_table(self, repos, category="favorites", exclude_repos_path="exclude_repos.list", use_repocards=False):
        readme = []

        if not use_repocards:
            readme.extend((
                "| Stars | Forks | Repository | Description |\n",
                "| ----- | ----- | ---------- | ----------- |\n"
            ))

        with open(exclude_repos_path) as file:
            exclude_repos = file.readlines()

        to_be_deleted = []
        for repo in repos:
            if not repo["fork"] and repo["name"] not in exclude_repos and (category is None or category in repo["topics"]):
                if use_repocards:
                    readme.append(f'[![](https://github-readme-stats.vercel.app/api/pin/?username={self.username}&repo={repo["name"]})]({repo["html_url"]})')
                else:
                    readme.append(f"| {repo['stargazers_count']} | {repo['forks_count']} | [{repo['name']}]({repo['html_url']}) | {repo['description']} |\n")
                to_be_deleted.append(repo)

        filtered_repos = [repo for repo in repos if (repo not in to_be_deleted)]
        return readme, filtered_repos

    def __end_of_readme(self, readme, path, use_repocards):
        for category, tag in self.categories.items():
            readme.append(f"\n## {category}\n\n")
            if tag == "gh-favorites":
                readme.append("Note: Projects in this section may reappear in other categories.\n\n")
            new_table, _ = self.__generate_repositories_table(self.repos, category=tag, use_repocards=use_repocards)
            readme.extend(new_table)

        if self.add_badge:
            readme.append(f"\n\n[![automated-profile-updater](https://github.com/{self.username}/{self.username}/actions/workflows/update.yml/badge.svg)](https://github.com/{self.username}/{self.username}/actions/workflows/update.yml)\n")

        if self.add_timestamp:
            readme.append("\n\n\n")
            readme.append(f"Last updated: {str(ctime())}\n")

        with open(path, "w") as file:
            file.writelines(readme)

    def build_desktop(self, template_path="TEMPLATE.md", output_path_desktop="README.md", use_repocards=False):
        with open(template_path) as file:
            readme = file.readlines()

        readme.append(f"\n[**>>> Click here for mobile website! <<<**]({self.mobile_url})\n\n")

        self.__end_of_readme(readme, output_path_desktop, use_repocards)

    def build_mobile(self, template_path="TEMPLATE.md", output_path_mobile="README_mobile.md", use_repocards=False):
        with open(template_path) as file:
            readme = file.readlines()

        readme.append(f"\n[**>>> Click here for desktop website! <<<**]({self.desktop_url})\n\n")

        self.__end_of_readme(readme, output_path_mobile, use_repocards)



if __name__ == '__main__':
    ReadmeGenerator(
        username                  = "salihmarangoz",
        sort_list_with_stargazers = False, 
        add_timestamp             = True, 
        add_badge                 = True,
        desktop_url               = "https://github.com/salihmarangoz",
        mobile_url                = "https://salihmarangoz.github.io/salihmarangoz/README_mobile"
    )
