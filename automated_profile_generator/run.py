
import time
from ghapi.all import GhApi # see: https://ghapi.fast.ai/fullapi.html
import os
import yaml
import copy
import textwrap

class ReadmeGenerator:
    def __init__(self, config, script_path="."):
        self.api = GhApi()
        self.config = config
        self.script_path = script_path
        self.repos = self.get_user_repositories()

    def get_user_repositories(self):
        username = self.config["github"]["username"]
        per_page = 100
        page = 1
        repos = []
        finished = False

        print("Parsing user repositories...")
        while not finished:
            new_repos = self.api.repos.list_for_user(username=username, per_page=per_page, page=page, sort="pushed") 
            repos.extend(new_repos)
            if len(new_repos) < per_page:
                print("Found {} repositories.".format(len(new_repos)))
                finished = True
            else:
                print("Found {} repositories. There may be more...".format(len(new_repos)))
                page += 1
        print("Finished! Found {} repositories in total.".format(len(repos)))

        print("Filtering excluded repositories...")
        repos_ = copy.deepcopy(repos)
        for repo in repos:
            if repo["name"] in self.config["exclude_repositories"]:
                print("- Removed", repo["name"])
                repos_.remove(repo)
        repos = repos_

        print("Filtering forks and archived repositories...")
        repos_ = copy.deepcopy(repos)
        for repo in repos:
            if (repo["archived"] or repo["fork"]) and not repo["name"] in self.config["include_repositories"]:
                print("- Removed", repo["name"])
                repos_.remove(repo)
        repos = repos_

        return repos

    # For contents of repo objects check this example: https://api.github.com/repos/salihmarangoz/salihmarangoz
    def generate_section_1(self, name, description, repos, use_repocards):
        readme = []

        if name is not None:
            readme.append("## {}\n".format(name))

        if description is not None:
            readme.append("{}\n".format(description))

        if use_repocards:
            for repo in repos:
                readme.append("[![](https://github-readme-stats.vercel.app/api/pin/?username={}&repo={})]({})".format(repo["owner"]["login"], repo["name"], repo["html_url"]))
            readme.append("\n")
        else:
            star_icon = "<img src=\"https://raw.githubusercontent.com/primer/octicons/main/icons/star-24.svg\" width=\"16\" height=\"16\" align=\"left\">"
            fork_icon = "<img src=\"https://raw.githubusercontent.com/primer/octicons/main/icons/repo-forked-24.svg\" width=\"16\" height=\"16\" align=\"left\">"
            code_icon = "<img src=\"https://raw.githubusercontent.com/primer/octicons/main/icons/file-code-24.svg\" width=\"16\" height=\"16\" align=\"left\">"
            readme.append("| {} | {}  | Repository/Description |\n".format(star_icon, fork_icon, code_icon))
            readme.append("| -- | -- | --------------------- |\n")
            for repo in repos:
                test_icon = "<img src=\"https://raw.githubusercontent.com/devicons/devicon/master/icons/c/c-original.svg\" width=\"16\" height=\"16\" align=\"left\">"
                readme.append("| {} | {}  | [{}]({}): {} |\n".format(repo["stargazers_count"], repo["forks_count"], repo["name"], repo["html_url"], repo["description"]))

        return readme

    # For contents of repo objects check this example: https://api.github.com/repos/salihmarangoz/salihmarangoz
    def generate_section_2(self, name, description, repos, use_repocards):
        readme = []
        if use_repocards:
            if name is not None:
                readme.append("## {}\n".format(name))
            if description is not None:
                readme.append("{}\n".format(description))
            for repo in repos:
                #readme.append("[![](https://ghc.clait.sh/repo/{}/{}?bg_color=ffffff&title_color=0366d6&text_color=333333&icon_color=333333&show_user=false)]({})".format(repo["owner"]["login"], repo["name"], repo["html_url"]))
                readme.append("[![](https://github-readme-stats.vercel.app/api/pin/?username={}&repo={})]({})".format(repo["owner"]["login"], repo["name"], repo["html_url"]))
                #readme.append("<a href=\"{}\"><img height=\"150px\" width=\"45%\" src=\"https://github-readme-stats.vercel.app/api/pin/?username={}&amp;repo={}\" alt=\"\"></a>".format(repo["html_url"], repo["owner"]["login"], repo["name"]))
            readme.append("\n")
        else:
            star_icon = "<img src=\"https://raw.githubusercontent.com/primer/octicons/main/icons/star-24.svg\" width=\"16\" height=\"16\">"
            fork_icon = "<img src=\"https://raw.githubusercontent.com/primer/octicons/main/icons/repo-forked-24.svg\" width=\"16\" height=\"16\">"
            code_icon = "<img src=\"https://raw.githubusercontent.com/primer/octicons/main/icons/code-24.svg\" width=\"16\" height=\"16\">"
            law_icon  = "<img src=\"https://raw.githubusercontent.com/primer/octicons/main/icons/law-24.svg\" width=\"16\" height=\"16\">"
            readme.append("\n| {} |\n".format(name))
            readme.append("| ---------------------- |\n")
            for repo in repos:
                # list style:
                #readme.append("| [{}]({}): {} ({} {} {} {} {} {})  |\n".format(repo["name"], repo["html_url"], repo["description"], code_icon, repo["language"], star_icon, repo["stargazers_count"], fork_icon, repo["forks_count"]))
                
                # repocard style:
                #readme.append("| [**{}**]({})<br>{}<br><br><p align=\"right\">".format(repo["name"], repo["html_url"], repo["description"]))

                # repocard+textwrap style:
                #readme.append("| [**{}**]({})<br>".format(repo["name"], repo["html_url"]))
                #for t in textwrap.wrap(str(repo["description"]), width=50):
                #    readme.append("{}<br>".format(t))
                #readme.append("<br><p align=\"right\">")

                # repocard+shorten style:
                readme.append("| [**{}**]({})<br>{}<br><br><p align=\"right\">".format(repo["name"], repo["html_url"], textwrap.shorten(str(repo["description"]), width=100, placeholder="...")))

                if repo["stargazers_count"] > 0:
                    readme.append(" [{}]({}) {} &nbsp;".format(star_icon, repo["html_url"]+"/stargazers", repo["stargazers_count"]))
                if repo["forks_count"] > 0:
                    readme.append(" [{}]({}) {} &nbsp;".format(fork_icon, repo["html_url"]+"/network/members", repo["forks_count"]))
                if repo["language"] is not None:
                    readme.append(" [{}]({}) {} &nbsp;".format(code_icon, repo["html_url"], repo["language"]))
                if repo["license"] is not None:
                    readme.append(" [{}]({}) {}".format(law_icon, repo["html_url"]+"/blob/"+repo["default_branch"]+"/LICENSE", repo["license"]["spdx_id"]))
                readme.append("</p> |\n")

        return readme

    def build_desktop(self, target="desktop"):
        print("\n########## Building for: {} ##########".format(target))

        username            = config["github"]["username"]
        template_path       = os.path.join(self.script_path, self.config[target]["template_path"])
        output_path         = os.path.join(self.script_path, self.config[target]["output_path"])
        sort_repositories   = self.config[target]["sort_repositories"]
        sort_reversed       = self.config[target]["sort_reversed"]
        use_repocards       = self.config[target]["use_repocards"]
        add_timestamp       = self.config[target]["add_timestamp"]
        add_profile_counter = self.config[target]["add_profile_counter"]
        add_badge           = self.config[target]["add_badge"]
        tags                = self.config["tags"]
        repos               = copy.deepcopy(self.repos)

        if sort_repositories is not None:
            repos = sorted(repos, key=lambda d: d[sort_repositories], reverse=sort_reversed) 

        f = open(template_path)
        readme = f.readlines()

        for tag in tags:
            print("\nGenerating section:", tag["name"])

            repos_ = copy.deepcopy(repos)
            repos_this_tag = []
            for repo in repos:
                if tag["repositories"] is None or repo["name"] in tag["repositories"]:
                    print("- Added", repo["name"])
                    repos_this_tag.append(repo)
                    if tag["consume"]:
                        repos_.remove(repo)
            repos = repos_

            readme.extend( self.generate_section_2(tag["name"], tag["description"], repos_this_tag, use_repocards) )

        if add_profile_counter:
            readme.append("\n\n![](https://visitor-badge.glitch.me/badge?page_id={}&left_text=Page%20View%20Counter)".format(username))

        if add_badge:
            readme.append("\n\n[![automated-profile-updater](https://github.com/{}/{}/actions/workflows/update.yml/badge.svg)](https://github.com/{}/{}/actions/workflows/update.yml)\n".format(username, username, username, username))

        if add_timestamp:
            readme.append("\n\n\n")
            readme.append("Last updated: " + str(time.ctime()) + "\n")

        f = open(output_path, "w")
        f.writelines(readme)
        f.close()

    def generate_starred_section(self, name, description, collapse, repos, notes):
        readme = []
        readme.append("\n### {}\n".format(name))

        if collapse:
            readme.append("\n<details>\n<summary>Click to expand!</summary>\n\n")

        for repo in repos:
            # list style:
            readme.append("- [{}]({}):".format(repo["full_name"], repo["html_url"]))
            if repo["description"] is not None and repo["description"] != "None" :
                readme.append(" {}".format(repo["description"]))
            else:
                readme.append(" N/A")
            if repo["language"] is not None and repo["language"] != "None" :
                readme.append(" ({})".format(repo["language"]))
            readme.append("\n")
            if repo["full_name"] in notes:
                readme.append("  - **{}**\n".format(notes[repo["full_name"]]))

        if collapse:
            readme.append("</details>\n")

        return readme

if __name__ == "__main__":
    script_folder = os.path.dirname(__file__)
    with open(os.path.join(script_folder, "config.yaml"), "r") as stream:
        try:
            config = yaml.safe_load(stream)
        except yaml.YAMLError as e:
            print(e)

    rg = ReadmeGenerator(config, script_folder)
    rg.build_desktop()