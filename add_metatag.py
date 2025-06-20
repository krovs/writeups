import os
import datetime

# Example metatag template
METATAG = """---
title: "{title}"
date: {date}
categories:
  - HackTheBox
  - Linux
tags:
  - HackTheBox
  - Linux
---
"""


def get_title_from_filename(filename):
    # Use filename (without extension) as title, replace -/_ with space and capitalize
    name = os.path.splitext(os.path.basename(filename))[0]
    return name.replace('-', ' ').replace('_', ' ').title()


def has_metatag(lines):
    # Check if file already starts with a YAML frontmatter block
    return len(lines) > 0 and lines[0].strip() == "---"


def process_md_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    title = get_title_from_filename(filepath)
    today = datetime.date.today().isoformat()
    metatag = METATAG.format(title=title, date=today)

    if has_metatag(lines):
        # Update existing metatag (replace from first '---' to next '---')
        start = None
        end = None
        for i, line in enumerate(lines):
            if line.strip() == "---":
                if start is None:
                    start = i
                elif end is None:
                    end = i
                    break
        if start is not None and end is not None and end > start:
            # Replace old metatag with new one
            new_lines = [metatag + '\n'] + lines[end + 1 :]
            with open(filepath, 'w', encoding='utf-8') as f:
                f.writelines(new_lines)
            print(f"Metatag updated: {filepath}")
        else:
            # If malformed, skip
            print(f"Malformed metatag, skipped: {filepath}")
        return

    # If no metatag, add it
    new_content = metatag + '\n' + ''.join(lines)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"Metatag added: {filepath}")


def process_folder(folder):
    for root, _, files in os.walk(folder):
        for file in files:
            if file.endswith('.md'):
                process_md_file(os.path.join(root, file))


if __name__ == '__main__':
    # Change this path as needed
    base_dirs = [
        'docs/posts/HackTheBox/Linux',
    ]
    for base in base_dirs:
        if os.path.exists(base):
            process_folder(base)
