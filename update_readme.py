import os
import requests
import yaml

def fetch_all_stars(user, token):
    """
    获取用户所有 starred 仓库
    :param user: GitHub 用户名
    :param token: GitHub Token
    :return: 仓库列表，包含 full_name, name, html_url, description
    """
    stars = []
    page = 1
    per_page = 100
    headers = {'Authorization': f'token {token}'}
    
    while True:
        resp = requests.get(
            f"https://api.github.com/users/{user}/starred?per_page={per_page}&page={page}",
            headers=headers,
        )
        
        if resp.status_code != 200:
            print(f"API 请求失败，状态码: {resp.status_code}")
            print(f"响应内容: {resp.text}")
            break
            
        data = resp.json()
        if not data:
            break
            
        stars.extend(data)
        page += 1
        print(f"已获取第 {page-1} 页，共 {len(stars)} 个仓库")
    
    return [
        {
            "full_name": repo["full_name"],
            "name": repo["name"],
            "html_url": repo["html_url"],
            "description": (repo["description"] or "").replace("\n", " ").strip(),
        } for repo in stars
    ]

def load_categories(filepath):
    """
    加载自定义分组配置
    :param filepath: 分类配置文件路径
    :return: 分组字典
    """
    if os.path.exists(filepath):
        with open(filepath, encoding="utf-8") as f:
            category = yaml.safe_load(f)
        return category if category else {}
    return {}

def generate_readme(groups, output_file="README.md"):
    """
    生成 README.md 文件
    :param groups: 分组字典
    :param output_file: 输出文件名
    """
    MAX_DESC_LENGTH = 200
    
    def truncate(text, max_len=MAX_DESC_LENGTH):
        """截断过长的文本，添加省略号"""
        if len(text) > max_len:
            return text[:max_len] + "..."
        return text
    
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("# 我的 Star 项目导航\n\n")
        
        # 按分类顺序输出
        for group, repos in groups.items():
            f.write(f"## {group} ({len(repos)})\n")
            if repos:
                for repo in repos:
                    desc = truncate(repo['description']) if repo['description'] else ""
                    f.write(f"- [{repo['name']}]({repo['html_url']}) - {desc}\n")
                f.write("\n")
        
        f.write("> 本页由自动脚本生成，分组可手动编辑 star-category.yaml\n")

def main():
    # 获取环境变量
    USER = os.environ.get("GITHUB_REPOSITORY_OWNER")
    TOKEN = os.environ.get("GH_TOKEN")
    
    # 本地测试时使用默认值
    if not USER:
        USER = "YOUR_GITHUB_USERNAME"
        print("警告: 使用默认用户名，建议在 GitHub Actions 中运行")
    
    assert TOKEN, "请在 Actions secrets 中配置 GH_TOKEN"
    
    print(f"开始获取用户 {USER} 的 starred 仓库...")
    
    # 1. 读取所有 star 项目
    all_stars = fetch_all_stars(USER, TOKEN)
    print(f"共获取到 {len(all_stars)} 个仓库")
    
    # 2. 读取自定义分组
    category = load_categories("star-category.yaml")
    print(f"加载到 {len(category)} 个自定义分组")
    
    # 3. 初始化分组
    groups = {k: [] for k in category}
    catset = set()  # 已分组仓库集合
    
    # 4. 匹配分组
    for star in all_stars:
        for group, repo_list in category.items():
            if star["full_name"] in repo_list:
                groups[group].append(star)
                catset.add(star["full_name"])
                break
    
    # 5. 归类未分组
    uncategorized = [star for star in all_stars if star["full_name"] not in catset]
    groups["未分组"] = uncategorized
    print(f"未分组仓库: {len(uncategorized)} 个")
    
    # 6. 生成 README.md
    generate_readme(groups)
    print("README.md 已生成")

if __name__ == "__main__":
    main()
