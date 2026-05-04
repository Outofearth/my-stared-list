"""
自动生成 star-category.yaml 模板
根据仓库名称关键词自动生成分组
支持从本地 README.md 或 GitHub API 获取仓库列表
智能合并：保留手动调整的分类，新增项目自动分类，未知项目归入其他
"""
import os
import re
import yaml

def parse_readme_stars(readme_file):
    """
    从本地 README.md 解析 starred 仓库列表
    """
    stars = []
    pattern = r'- \[([^\]]+)\]\(https://github\.com/([^/]+)/([^)]+)\)'

    with open(readme_file, encoding="utf-8") as f:
        content = f.read()

    for match in re.finditer(pattern, content):
        name = match.group(1)
        full_name = f"{match.group(2)}/{match.group(3)}"
        stars.append({
            "full_name": full_name,
            "name": name,
        })

    return stars

def load_existing_categories(filepath):
    """加载已存在的分类配置"""
    if not os.path.exists(filepath):
        return {}

    with open(filepath, encoding="utf-8") as f:
        old_config = yaml.safe_load(f) or {}

    # 转换为 {repo_full_name: set(categories)} 格式
    repo_categories = {}
    for category, repos in old_config.items():
        if not repos:
            continue
        for repo in repos:
            if repo not in repo_categories:
                repo_categories[repo] = set()
            repo_categories[repo].add(category)

    return repo_categories

def group_by_keywords(stars):
    """按仓库名称关键词分组"""
    keyword_map = {
        "AI/ML": [
            "ai", "ml", "deeplearning", "deep-learning", "pytorch", "tensorflow",
            "llm", "gpt", "bert", "transformer", "neural", "nlp", "cv", "diffusion",
            "stable-diffusion", "llama", "gemini", "chatgpt", "openai", "claude",
            "langchain", "agent", "rag", "embedding", "ocr", "asr", "tts", "stt",
            "whisper", "yolo", "gan", "vae", "vlm", "vqa", "multimodal", "llava",
            "stable-diffusion", "diffusion", "gpt", "chatbot", "conversation", "copilot",
            "mistral", "qwen", "deepseek", "vector", "embedding",
            "speech", "voice", "tts", "asr", "cosyvoice", "emotivovoice",
            "mineru", "mindspore", "comfyui", "langchain", "autogpt", "agent",
            "huatuo", "qwen", "deepseek", "claude", "gemini", "deer-flow",
            "supervision", "cv", "vision", "detection"
        ],
        "3DM/P/AI": [
            "3d", "print", "slicer", "cad", "stl", "obj", "mesh", "sdf", "gaussian",
            "splat", "pointcloud", "reconstruction", "blender", "deform", "planar",
            "extrusion", "reprap", "duet", "grbl", "printing", "three.js", "3d",
            "triposr", "unique3d", "dreamgaussian", "zperiod", "poly", "multiscan",
            "smoothificator", "split-flap", "s4_slicer", "sls4all", "roetz",
            "trellis", "stltexturizer", "chili3d", "zperiod", "miropgfish",
            "mirofish", "scara_plotter", "pakeplus", "x-scara", "scara"
        ],
        "Robot": [
            "robot", "robotic", "arm", "hand", "humanoid", "drone", "vehicle",
            "champ", "cheetah", "quadruped", "dexhand", "duck", "legged", "locomotion",
            "manipulation", "humanoid", "walker", "bipedal",
            "agibot", "openclaw", "ironclaw", "clawra", "matrix", "freemocap",
            "lerobot", "dexhand", "champ", "cheetah", "asimov", "ar3_core", "miropgfish",
            "master-board"
        ],
        "AI Projects": [
            "swarm", "metahuman", "langup", "virtualwife", "dh_live", "huatuo",
            "gpt_academic", "gligen", "facefusion", "answer", "stable-diffusion-webui",
            "wav2lip", "video-retalking", "so-vits-svc", "bark", "voice-changer",
            "gpt-engineer", "xiaogpt", "gpt4free", "word-as-image", "vits",
            "emotivovoice", "desktopai", "chineseaidungeon", "paper2gui",
            "codeformer", "chatgptcnserver", "roop", "ultimatevocalremover",
            "gpt-sovits", "vall-e-x", "hello-ai", "awesome-free-chatgpt",
            "cosyvoice", "comfyui", "lobehub", "page-assist", "mcp-marketplace",
            "awesome-deepseek-integration", "xiaozhi-esp32-server", "firecrawl",
            "openmanus", "unsloth", "go-cursor-help", "servers", "pocketpal-ai",
            "crawl4ai", "go2coding", "browser-use", "system-prompts",
            "awesome-llm-apps", "doly", "wan2gp", "gstack", "pua",
            "agency-agents", "moneyprinterturbo", "openmaic", "bb-sites",
            "opendataloader", "infinitetalk", "zhizix", "chinese-independent-developer",
            "howto-make-more-money", "narratoai", "vibevoice", "system_prompts_leaks",
            "hermes-agent", "awesome-gpt-image-2", "free-claude-code",
            "public-apis", "awesome-codex-skills", "ai-legal-claude", "deer-flow"
        ],
        "TopGoodTool": [
            "tool", "util", "cli", "gui", "desktop", "app", "application", "utility",
            "helper", "wrapper", "manager", "launcher", "installer", "paste", "pasteMD",
            "powertoys", "taskexplorer", "winutil", "res-downloader", "pansou", "gopeed",
            "mind-map", "ezbookkeeping", "linsa", "ytdownloader", "linuxmirrors",
            "awesome-cloudflare", "teslamate", "aivideotranscriber", "smartsystemmenu",
            "pastemd", "taskexplorer", "immich", "proxmark3", "books",
            "next-ai-draw-io", "autoclip", "deer-flow", "miropgfish", "online3dviewer",
            "pinokio", "editor", "res-downloader", "aicheck", "aicomicbuilder",
            "aitoearn", "pilipili-autovideo", "xiaohu-wechat-format", "easy-vibe",
            "zperiod", "carbonyl", "logo-generator-skill", "glm-ocr", "oh-my-codex",
            "openscreen", "career-ops", "funasr", "winutil", "supersplat",
            "three.js", "ai-reads-books-page-by-page", "sentrysearch",
            "ai-website-cloner-template", "pixelle-video", "ghosttrack",
            "voice-pro", "hackingtool", "mpc-be", "fuzzyficator", "carbonyl",
            "taskexplorer", "pastemd", "gopeed", "res-downloader", "pansou",
            "openscreen", "mpc-be"
        ],
        "Finance": [
            "finance", "stock", "trading", "quant", "quantitative", "algotrading",
            "backtest", "indicator", "strategy", "market", "invest", "trading",
            "bitcoin", "crypto", "currency", "forex", "chanlun", "tdx", "mootdx",
            "gotdx", "mytt", "ashare", "rstock", "tuchart", "tickflow", "dexter",
            "trendradar", "fincept", "smart-money-concepts", "ai_quant_trade",
            "tradingagents-cn", "aiagents-stock", "daily_stock_analysis",
            "quantfinance", "stock-learning", "chan.py", "czsc", "chanlun-pro",
            "fmzquant", "strategies"
        ],
        "NetworkTools": [
            "network", "proxy", "vpn", "firewall", "dns", "cdn", "gateway",
            "router", "tcp", "udp", "websocket", "cloudflare", "tunnel", "proxy",
            "v2ray", "shadowsocks", "ssr", "xray", "trojan", "free-proxy", "fq",
            "new-pac", "freersh", "v2rayn", "shadowsocks-windows",
            "share-ssr-v2ray", "fq", "imfile-desktop", "github520",
            "openwrt", "freedomain", "cloudflare-vless-trojan", "cfnew",
            "fastgithub", "domain-list-community", "cloudflare-proxy",
            "xray-config-toolkit", "proxfly", "vless", "trojan", "free-fq", "free"
        ],
        "Books/Learning": [
            "learn", "course", "tutorial", "book", "guide", "handbook",
            "documentation", "doc", "wiki", "example", "demo", "study", "class",
            "hello-algo", "weekly", "howtocook", "chinese-history", "chinatextbook",
            "opentutor", "deeptutor", "learning", "scripta-sinica",
            "books-free-books", "pyqt5", "learningpyqt5", "opencv-python-tutorial",
            "funnlp", "bazi", "python_cn_resouce", "ruanyf-weekly",
            "krahets-hello-algo", "shjwudp-shu", "tapxworld-chinatextbook",
            "jningwei-chinese_history", "deeplearningbook-chinese",
            "anduin2017-howtocok", "calibre-web", "proxy-guide",
            "ai-money-maker-handbook", "cs-video-courses", "free-premium-ai",
            "learning", "howtocook", "chinese-history", "shjwudp", "shu",
            "chinese_history", "history"
        ],
        "ClawFamily": [
            "claw", "openclaw", "ironclaw", "clawra", "qwenpaw", "edict",
            "openclaw-medical-skills", "awesome-openclaw-skills", "cowagent",
            "aionui", "autocli", "rowboat", "deeptutor", "huashu-design",
            "opencli", "hermes-web-ui", "darwin-skill", "portable-hermes-agent",
            "ppt-design-prompt", "agency-agents-zh", "awesome-gpt-image-2"
        ],
        "舆情分析": [
            "sentiment", "opinion", "舆情", "monitor", "spider", "analyzer",
            "social-analyzer", "mindspider", "wechat-download-api", "horizon",
            "worldmonitor", "bettafish", "social-analyzer", "awesome-public-datasets"
        ],
        "ESP32/Hardware": [
            "esp", "esp32", "arduino", "raspberry", "pi", "circuit", "pcb", "hardware",
            "firmware", "embedded", "microcontroller", "stm32", "fpga", "chip",
            "proxmark", "reprap", "duet", "esp32-csi-tool", "ruview",
            "aily-blockly", "pidoc-site-zhcn", "web-flasher", "meshtastic",
            "thatproject", "scara_plotter", "xiaozhi", "ar4", "ros", "driver"
        ],
        "Skill Box": [
            "skill", "scripts", "python-scripts", "handright", "handwrite",
            "subtitleedit", "pytranscriber", "worker-vless-2-sub", "gradio",
            "termux", "nekoboxforandroid", "deepling_Notes_cv", "logicflow",
            "jellyfin", "casaos", "umi-ocr", "pages-vless-sub", "opensource",
            "pyqt", "object-detection", "shape_recognition", "zoomeye",
            "are-u-ok", "istoreos", "bulk-crap-uninstaller", "clash-merlin",
            "file-checksum", "iptv", "algorithm-structure", "arduino-cli",
            "yuan"
        ],
        "Web": [
            "web", "http", "server", "frontend", "backend", "api", "website",
            "html", "css", "javascript", "vue", "react", "angular", "nextjs", "nuxt",
            "django", "flask", "fastapi", "node", "website", "page", "blog", "forum",
            "flasher", "public-apis", "cors", "nginx", "apache"
        ],
        "Awesome": [
            "awesome", "collection", "list", "curated", "resources"
        ],
        "Dev": [
            "dev", "develop", "ide", "editor", "debug", "code", "coding", "programming",
            "compiler", "interpreter", "sdk", "api", "framework", "library", "repo",
            "source", "git", "github", "pyqt", "qt", "gui", "cli", "fff", "tinker"
        ],
        "Media": [
            "video", "audio", "image", "photo", "media", "stream", "ffmpeg",
            "caption", "subtitle", "transcribe", "voice", "speech", "music", "song",
            "podcast", "camera", "pic", "picture", "photo", "gallery", "lossless-cut",
            "ytdownloader", "mpc", "immich", "openscreen", "voice-changer"
        ],
        "Cloud": [
            "cloud", "aws", "azure", "gcp", "kubernetes", "k8s", "docker",
            "container", "serverless", "lambda", "deployment", "server", "host",
            "openwrt", "istoreos", "cfnew", "cloudflare"
        ],
        "OS": [
            "windows", "linux", "macos", "mac", "ubuntu", "debian", "fedora",
            "arch", "redhat", "android", "ios", "unix", "freebsd", "openwrt",
            "dockur"
        ],
        "SmartHome": [
            "home", "smart", "assistant", "homeassistant", "automation",
            "iot", "sensor", "temperature", "light", "switch", "teslamate"
        ],
        "Download": [
            "download", "downloader", "fetcher", "get", "save", "gopeed", "pansou"
        ],
        "MindMap/Doc": [
            "mind", "map", "mindmap", "note", "doc", "document", "knowledge"
        ],
    }

    def auto_categorize(name_lower):
        """自动为仓库分类"""
        matched = set()
        for group, keywords in keyword_map.items():
            if any(kw in name_lower for kw in keywords):
                matched.add(group)
        return matched

    # 加载旧配置
    old_config_path = "star-category-by-keywords.yaml"
    old_repo_categories = load_existing_categories(old_config_path)

    # 初始化结果
    groups = {k: [] for k in keyword_map}
    groups["其他"] = []
    known_categories = set(keyword_map.keys())

    new_repos_count = 0
    kept_repos_count = 0
    other_repos_count = 0

    for star in stars:
        name_lower = star["name"].lower()
        full_name = star["full_name"]

        # 检查是否已在旧配置中
        if full_name in old_repo_categories:
            old_categories = old_repo_categories[full_name]
            auto_categories = auto_categorize(name_lower)

            # 如果自动分类结果与旧分类一致，保留旧分类
            if old_categories == auto_categories:
                for cat in old_categories:
                    if full_name not in groups[cat]:
                        groups[cat].append(full_name)
                kept_repos_count += 1
            else:
                # 分类不一致，可能是手动调整过，保留旧分类
                for cat in old_categories:
                    if cat in groups:  # 旧分类可能已被移除
                        if full_name not in groups[cat]:
                            groups[cat].append(full_name)
                kept_repos_count += 1
        else:
            # 新项目，自动分类
            new_repos_count += 1
            auto_categories = auto_categorize(name_lower)

            if auto_categories:
                for cat in auto_categories:
                    if full_name not in groups[cat]:
                        groups[cat].append(full_name)
            else:
                # 无法自动分类，归入其他
                if full_name not in groups["其他"]:
                    groups["其他"].append(full_name)
                other_repos_count += 1

    # 过滤空类别
    result = {k: v for k, v in groups.items() if v}

    # 打印统计
    total = sum(len(v) for v in result.values())
    print("\n" + "="*60)
    print(f"分类完成 (共 {total} 个仓库):")
    print(f"  - 保留旧分类: {kept_repos_count} 个")
    print(f"  - 新增项目: {new_repos_count} 个")
    print(f"  - 归入其他: {other_repos_count} 个")
    print("="*60 + "\n")

    for group, repos in result.items():
        print(f"## {group} ({len(repos)} 个)")

    return result

def save_yaml(groups, filepath):
    """保存为 YAML 文件"""
    with open(filepath, "w", encoding="utf-8") as f:
        yaml.dump(groups, f, allow_unicode=True, default_flow_style=False, sort_keys=False)

def main():
    import sys

    readme_file = "README.md"

    if len(sys.argv) > 1:
        readme_file = sys.argv[1]

    print(f"从 {readme_file} 解析 starred 仓库...")

    try:
        stars = parse_readme_stars(readme_file)
        print(f"共解析到 {len(stars)} 个仓库\n")
    except FileNotFoundError:
        print(f"错误: 文件 {readme_file} 不存在")
        print("使用方法: python generate_category_template.py [README.md路径]")
        return

    groups = group_by_keywords(stars)

    output_file = "star-category-by-keywords.yaml"
    save_yaml(groups, output_file)
    print(f"\n已保存: {output_file}")

if __name__ == "__main__":
    main()
