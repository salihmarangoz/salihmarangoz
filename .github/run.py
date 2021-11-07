
import time
from ghapi.all import GhApi
import os


class ReadmeGenerator:
    def __init__(self, username):
        self.api = self.get_github_api()
        self.username = username


    def get_github_api(self):
        # https://ghapi.fast.ai/fullapi.html
        #github_token = os.environ['GITHUB_TOKEN']
        #api = GhApi(token=github_token)
        api = GhApi()
        return api


    def generate_repositories_table(self):
        readme = []
        readme.append("| Repository | Description |\n")
        readme.append("| ---------- | ----------- |\n")

        repos = []
        out = self.api.repos.list_for_user(username=self.username, per_page=100, sort="pushed", type="owner")
        print(out[0])
        for o in out:
            if not o["fork"]:
                repos.append(o)
                print(o["topics"])
                readme.append("| [{}]({}) | {} |\n".format(o["name"], o["html_url"], o["description"]))
        
        return readme


    def build(self, template_path=".github/TEMPLATE.md", output_path="README.md"):
        f = open(template_path)
        readme = f.readlines()

        # modify template here
        #readme.append("\n\n\n\n\n")
        #readme.append("Last updated: " + time.ctime(time.time()) + "\n")
        repo_table = self.generate_repositories_table()
        readme.extend(repo_table)

        f = open(output_path, "w")
        f.writelines(readme)
        f.close()


rg = ReadmeGenerator(username="salihmarangoz")
rg.build()