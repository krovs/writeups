import os


def process_md_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    new_lines = [line for line in lines if '<!-- more -->' not in line]

    if len(new_lines) != len(lines):
        with open(filepath, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
        print(f"Removed <!-- more --> from: {filepath}")


def process_folder(folder):
    for root, _, files in os.walk(folder):
        for file in files:
            if file.endswith('.md'):
                process_md_file(os.path.join(root, file))


if __name__ == '__main__':
    # Change this path as needed
    base_dirs = [
        'docs/posts/Proving Grounds/Windows',
    ]
    for base in base_dirs:
        if os.path.exists(base):
            process_folder(base)
