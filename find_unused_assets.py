import os
import shutil
import urllib.parse

ASSETS_DIR = os.path.join('docs', 'HackTheBox', 'assets')
TEMP_DIR = os.path.join('docs', 'HackTheBox', 'assets', 'temp_unused')
SEARCH_DIRS = [
    os.path.join('docs', 'HackTheBox', 'AD'),
    os.path.join('docs', 'HackTheBox', 'Linux'),
    os.path.join('docs', 'HackTheBox', 'Windows'),
]


def get_all_asset_files():
    asset_files = []
    for root, _, files in os.walk(ASSETS_DIR):
        for f in files:
            asset_files.append(os.path.relpath(os.path.join(root, f), ASSETS_DIR))
    return asset_files


def get_all_md_files():
    md_files = []
    for search_dir in SEARCH_DIRS:
        for root, _, files in os.walk(search_dir):
            for f in files:
                if f.endswith('.md'):
                    md_files.append(os.path.join(root, f))
    return md_files


def is_asset_used(asset, md_files):
    # Check if asset filename appears in any md file
    asset_name = os.path.basename(asset)
    asset_name_encoded = urllib.parse.quote(asset_name)
    for md_file in md_files:
        with open(md_file, encoding='utf-8', errors='ignore') as f:
            content = f.read()
            if asset_name in content or asset_name_encoded in content:
                return True
    return False


def main():
    asset_files = get_all_asset_files()
    md_files = get_all_md_files()
    unused_assets = []
    for asset in asset_files:
        if not is_asset_used(asset, md_files):
            unused_assets.append(asset)
    if unused_assets:
        print("Unused asset files:")
        os.makedirs(TEMP_DIR, exist_ok=True)
        for asset in unused_assets:
            src = os.path.join(ASSETS_DIR, asset)
            dst = os.path.join(TEMP_DIR, os.path.basename(asset))
            print(src)
            try:
                shutil.move(src, dst)
            except Exception as e:
                print(f"Failed to move {src}: {e}")
    else:
        print("No unused asset files found.")


if __name__ == '__main__':
    main()
