import os
import json

def load_substack_data():
    base_dir = os.path.dirname(os.path.dirname(__file__))
    data_dir = os.path.join(base_dir, "data", "substack")

    index_path = os.path.join(data_dir, "index.json")
    summary_path = os.path.join(data_dir, "summary_dna.json")
    mirror_path = os.path.join(base_dir, "data", "mirror_dna.json")

    # Load index
    with open(index_path, "r", encoding="utf-8") as f:
        index_data = json.load(f)

    # Load DNA files
    summary_dna = {}
    mirror_dna = {}
    # Load summary_dna.json
    if os.path.exists(summary_path):
        with open(summary_path, "r", encoding="utf-8") as f:
            summary_list = json.load(f)
            summary_dna = {item["id"]: item for item in summary_list}
            
    # Load mirror_dna.json
    if os.path.exists(mirror_path):
        with open(mirror_path, "r", encoding="utf-8") as f:
            mirror_dna = json.load(f)

    posts = []
    for entry in index_data:
        post_id = entry["id"]
        md_path = os.path.join(data_dir, f"{post_id}.md")

        try:
            with open(md_path, "r", encoding="utf-8") as f:
                content = f.read()
        except FileNotFoundError:
            content = "(Markdown file missing.)"

        post = {
            "id": post_id,
            "title": entry.get("title", "Untitled"),
            "url": entry.get("url", "#"),
            "tags": entry.get("tags", []),
            "content": content,
            "summary": summary_dna.get(post_id, ""),
            "mirror": mirror_dna.get(post_id, {})
        }
        posts.append(post)

    return posts
