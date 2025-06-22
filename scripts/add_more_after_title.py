import os
import re


def process_md_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    new_lines = []
    inserted = False
    title_pattern = re.compile(r'^\s*#\s+')

    for idx, line in enumerate(lines):
        new_lines.append(line)
        if not inserted and title_pattern.match(line):
            # Only insert if not already present in the next line
            if idx + 1 < len(lines) and '<!-- more -->' in lines[idx + 1]:
                inserted = True
                continue
            new_lines.append('<!-- more -->\n')
            inserted = True

    if inserted:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
        print(f"Inserted <!-- more --> after title: {filepath}")


def process_folder(folder):
    for root, _, files in os.walk(folder):
        for file in files:
            if file.endswith('.md'):
                process_md_file(os.path.join(root, file))


if __name__ == '__main__':
    # Change these as needed
    base_dirs = [
        'docs/posts/Proving Grounds/AD',
    ]
    for base in base_dirs:
        if os.path.exists(base):
            process_folder(base)
