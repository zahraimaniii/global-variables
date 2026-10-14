import os
import shutil
import argparse

FOLDERS = ["immovable", "movable", "animals", "other"]

RULES = {
    "deed": "immovable",
    "land": "immovable",
    "field": "immovable",
    "house": "immovable",
    "barn":"immovable",
    "tractor": "movable",
    "plow": "movable",
    "car":"movable",
    "trailer":"movable",
    "generator":"movable",
    "invoice": "movable",
    "vaccine": "animals",
    "vet": "animals",
    "cattle": "animals",
    "cow":"animals",
    "bull":"animals",
    "sheep":"animals",
    "lamb":"animals",
    "horse":"animals",
    "chicken":"animals",
    
}

PROTECTED = ["cli.py", "README.md"]


def get_category(filename):
    name = os.path.splitext(filename)[0].lower()
    name = name.replace("_", " ").replace("-", " ")
    for word in name.split():
        if word in RULES:
            return RULES[word]
    return "other"


def organize_files(source, farm, apply):
    if not os.path.isdir(source):
        print(f"[ERROR] Source folder not found: '{source}'")
        return

    for filename in sorted(os.listdir(source)):
        old_path = os.path.join(source, filename)
        if filename.startswith(".") or filename in PROTECTED or not os.path.isfile(old_path):
            continue

        category = get_category(filename)
        folder = os.path.join(farm, category)
        new_path = os.path.join(folder, filename)

        if os.path.exists(new_path):
            print(f"Skip existing: {filename}")
        elif not apply:
            print(f"Would move: {filename} -> {category}/")
        else:
            try:
                os.makedirs(folder, exist_ok=True)
                shutil.move(old_path, new_path)
                print(f"Moved: {filename} -> {category}/")
            except OSError as error:
                print(f"[ERROR] Could not move '{filename}': {error}")

    if not apply:
        print("Preview only. Add --apply to move the files.")


def add_record(farm, category, name, details):
    name = name.strip()
    if name == "" or ".." in name or "/" in name or "\\" in name:
        print("[ERROR] Invalid name (empty, or contains '..', '/' or '\\').")
        return

    folder = os.path.join(farm, category)
    path = os.path.join(folder, name.replace(" ", "_").lower() + ".txt")
    if os.path.exists(path):
        print(f"[ERROR] Record already exists: {path}")
        return

    try:
        os.makedirs(folder, exist_ok=True)
        with open(path, "w", encoding="utf-8") as file:
            file.write(f"Name: {name}\nCategory: {category}\nDetails: {details}\n")
        print(f"[SUCCESS] Record created: {path}")
    except OSError as error:
        print(f"[ERROR] Could not write record: {error}")


def report(farm):
    if not os.path.isdir(farm):
        print(f"[ERROR] Farm folder not found: '{farm}'")
        return

    total = 0

    for category in FOLDERS:
        folder = os.path.join(farm, category)
        count = 0

        if os.path.isdir(folder):
            for filename in os.listdir(folder):
                path = os.path.join(folder, filename)

                if os.path.isfile(path):
                    count += 1

        print(f"{category}: {count} files")
        total += count

    print(f"Total: {total} files")


def main():
    parser = argparse.ArgumentParser(description="Farm document organizer")
    parser.add_argument("command", choices=["organize", "add", "report"])
    parser.add_argument("--path", default="farm", help="farm folder (default: farm)")
    parser.add_argument("--source", help="folder with incoming files (organize)")
    parser.add_argument("--apply", action="store_true", help="really move the files")
    parser.add_argument("--category", choices=["immovable", "movable", "animals"], help="(add)")
    parser.add_argument("--name", help="asset name (add)")
    parser.add_argument("--details", default="General Record", help="notes (add)")
    args = parser.parse_args()

    if args.command == "organize":
        if args.source is None:
            parser.error("organize needs --source")
        organize_files(args.source, args.path, args.apply)
    elif args.command == "add":
        if args.category is None or args.name is None:
            parser.error("add needs --category and --name")
        add_record(args.path, args.category, args.name, args.details)
    else:
        report(args.path)


if __name__ == "__main__":
    main()