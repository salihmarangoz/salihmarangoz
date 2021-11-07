
import time

f = open(".github/TEMPLATE.md", "r")
readme = f.readlines()


readme.append("\n\n\n\n\n")
readme.append("Last updated: " + time.ctime(time.time()) + "\n")

f = open("README.md", "w")
f.writelines(readme)
f.close()