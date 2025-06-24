from utils.load_data import load_substack_data

def main():
    data = load_substack_data()
    print(f"Loaded {len(data)} posts.")
    # Sample print
    for post in data[:1]:
        print(post["title"])
        print(post.get("tags", []))
        print()

if __name__ == "__main__":
    main()
