import os
import re


def process_md_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    new_lines = []
    found_img = False
    inserted = False

    img_pattern = re.compile(r'!\[.*\]\(.*\)')

    for idx, line in enumerate(lines):
        new_lines.append(line)
        if not found_img and img_pattern.search(line):
            found_img = True
            # Only insert if not already present in the next line
            if idx + 1 < len(lines) and '<!-- more -->' in lines[idx + 1]:
                continue
            new_lines.append('<!-- more -->\n')
            inserted = True

    if inserted:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
        print(f"Updated: {filepath}")


def process_folder(folder):
    for root, _, files in os.walk(folder):
        for file in files:
            if file.endswith('.md'):
                process_md_file(os.path.join(root, file))


if __name__ == '__main__':
    # Change these as needed
    base_dirs = [
        'docs/posts/Proving Grounds/Windows',
    ]
    for base in base_dirs:
        if os.path.exists(base):
            process_folder(base)
