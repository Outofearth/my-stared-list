import os
import requests
import yaml

# 获取你的 GitHub 用户名和 Token
USER = os.environ.get("GITHUB_REPOSITORY_OWNER", "YOUR_GITHUB_USERNAME")
TOKEN = os.environ.get("GH_TOKEN")

assert TOKEN, "GitHub Actions 内置 GH_TOKEN 不可用，请检查 workflow 权限配置"

def fetch_all_stars(user, token):
    stars = []
    page = 1
    per_page = 100
    headers = {'Authorization': f'token {token}'}
    while True:
        resp = requests.get(
            f"https://api.github.com/users/{user}/starred?per_page={per_page}&page={page}",
            headers=headers,
        )
        data = resp.json()
        if not data:
            break
        stars.extend(data)
        page += 1
    return [
        {
            "full_name": repo["full_name"],
            "name": repo["name"],
            "html_url": repo["html_url"],
            "description": (repo["description"] or "").replace("\n", " "),
        } for repo in stars
    ]

# 1. 读取所有 star 项目
all_stars = fetch_all_stars(USER, TOKEN)

# 2. 读取自定义分组
if os.path.exists("star-category.yaml"):
    with open("star-category.yaml", encoding="utf-8") as f:
        category = yaml.safe_load(f)
else:
    category = {}

groups = {k: [] for k in category}  # 已分组
catset = set()  # 统计已分组仓库

for star in all_stars:
    found = False
    for group, repo_list in category.items():
        if star["full_name"] in repo_list:
            groups[group].append(star)
            catset.add(star["full_name"])
            found = True
            break
    # 其余进入“未分组”

# 3. 归类未分组
groups["未分组"] = [star for star in all_stars if star["full_name"] not in catset]

# 4. 写入 README.md
with open("README.md", "w", encoding="utf-8") as f:
    f.write("# 我的 Star 项目导航\n\n")
    for group, repos in groups.items():
        f.write(f"## {group}\n")
        for repo in repos:
            f.write(f"- [{repo['name']}]({repo['html_url']}) - {repo['description']}\n")
        f.write("\n")
    f.write("> 本页由自动脚本生成，分组可手动编辑 star-category.yaml\n")
