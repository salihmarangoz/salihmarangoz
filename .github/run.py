
import time
from ghapi.all import GhApi
import os


f = open(".github/TEMPLATE.md", "r")
readme = f.readlines()


# https://ghapi.fast.ai/fullapi.html
#github_token = os.environ['GITHUB_TOKEN']
#api = GhApi(token=github_token)
api = GhApi()
#github_user = api.users.get_authenticated() # github_user["login"]

repos = []
out = api.repos.list_for_user(username="salihmarangoz", per_page=100, sort="pushed", type="owner")
for o in out:
    if not o["fork"]:
        repos.append(o)
        print(o["topics"], o["description"])

readme.append("\n\n\n\n\n")
readme.append("Last updated: " + time.ctime(time.time()) + "\n")

f = open("README.md", "w")
f.writelines(readme)
f.close()