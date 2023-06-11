import os
from PIL import Image

#Defualt = 256
SizeX=256
SizeY=256


def list_projects():
    blocks_path = './Types/BLOCKS'
    items_path = './Types/ITEMS'
    
    projects = set()
    
    for folder in os.listdir('./Types/'):
        for folder2 in os.listdir("./Types/"+folder):
            print(f"{folder} | {folder2}")
            projects.add(os.path.join("./Types/"+folder, folder2))


    return projects

def list_directories_in_project(project_path):
    directories = []
    
    for entry in os.scandir(project_path):
        if entry.is_dir():
            directories.append(entry.name)
            
    return directories

def remove_transparency(img):
    if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
        alpha = img.convert('RGBA').split()[-1]
        bg = Image.new("RGBA", img.size, (255, 255, 255, 255))
        bg.paste(img, mask=alpha)
        return bg
    else:
        return img

def create_tag_file(tag_path, default_tag):
    with open(tag_path, 'w') as f:
        f.write(default_tag.replace("_", " "))

def copy_tag_file(tag_path, compiled_tags_path):
    with open(tag_path, 'r') as original:
        with open(compiled_tags_path, 'w') as compiled:
            compiled.write(original.read())

def is_tag_file(entry):
    return entry.lower().endswith('.txt') or entry.lower().endswith('.zip')

def resize_and_copy_images(project_to_compile, project_directories):
    compiled_path = "./Compiled/"

    for directory in project_directories:
        dir_path = os.path.join(project_to_compile, directory)
        tags_path = os.path.join(dir_path, 'Tags')

        if not os.path.exists(tags_path):
            os.makedirs(tags_path)

        for entry in os.listdir(dir_path):
            file_path = os.path.join(dir_path, entry)

            if entry.lower().endswith('.png'):
                try:
                    image = Image.open(file_path)

                    new_file_name = f"{directory}_{entry}"
                    new_file_path = os.path.join(compiled_path, new_file_name)

                    resized_image = image.resize((SizeX, SizeY), resample=Image.NEAREST)
                    resized_image = remove_transparency(resized_image)
                    resized_image.save(new_file_path)

                    tag_file_name = f"{os.path.splitext(entry)[0]}.txt"
                    tag_file_path = os.path.join(tags_path, tag_file_name)
                    compiled_tags_file_name = f"{directory}_{tag_file_name}"
                    compiled_tags_file_path = os.path.join(compiled_path, compiled_tags_file_name)

                    if not os.path.exists(tag_file_path):
                        create_tag_file(tag_file_path, os.path.splitext(entry)[0])

                    copy_tag_file(tag_file_path, compiled_tags_file_path)

                except:
                    pass
            elif not is_tag_file(entry):
                try:
                    os.remove(file_path)
                except:
                    pass

def main():
    projects = list_projects()
    
    print("Available projects:")
    for i, project in enumerate(projects, start=1):
        print(f"{i}. {os.path.basename(project)}")
    
    while True:
        choice = input("Enter the number of the project you want to compile: ")
        try:
            user_choice = int(choice)
            if 1 <= user_choice <= len(projects):
                project_to_compile = list(projects)[user_choice - 1]
                print(f"Compiling project: {os.path.basename(project_to_compile)}")

                print("Directories inside the chosen project:")
                project_directories = list_directories_in_project(project_to_compile)
                for directory in project_directories:
                    print(f"    {directory}")

                resize_and_copy_images(project_to_compile, project_directories)
                print("Images resized and copied.")
                break
            else:
                print("Invalid choice. Please choose a valid number.")
        except ValueError:
            print("Invalid input. Please enter a number.")
    
if __name__ == "__main__":
    main()
