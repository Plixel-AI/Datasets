import os
from glob import glob
from PIL import Image
Errors=0
def count_16x16_pngs(path):

    count = 0
    for root, _, files in os.walk(path):
        for file in files:
            if file.endswith('.png'):
                try:
                    with Image.open(os.path.join(root, file)) as img:
                        if img.size == (16, 16):
                            count += 1
                except Exception as E:
                    print(f"Error: {E}")
    return count
def generate_table(directory):
    table = f"| {'Directory Name'} | {'Number of 16x16 PNGs'} |\n"
    table += "| -------------- | ------------------- |\n"

    for subdir in os.listdir(directory):
        path = os.path.join(directory, subdir)
        if os.path.isdir(path):
            count = count_16x16_pngs(path)
            table += f"| {subdir} | {count} |\n"

    return table

def main():
    with open('README.md', 'w') as readme:
        readme.write('# ITEMS\n\n')
        readme.write(generate_table('./ITEMS'))
        readme.write('\n\n# BLOCKS\n\n')
        readme.write(generate_table('./BLOCKS'))

if __name__ == '__main__':
    main()
