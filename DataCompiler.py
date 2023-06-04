import os
from PIL import Image

def list_projects():
    blocks_path = 'BLOCKS'
    items_path = 'ITEMS'
    
    projects = set()
    
    for folder in os.listdir(blocks_path):
        projects.add(os.path.join(blocks_path, folder))
        
    for folder in os.listdir(items_path):
        projects.add(os.path.join(items_path, folder))
        
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


def resize_and_copy_images(project_to_compile, project_directories):
    compiled_path = "./Compiled/"

    for directory in project_directories:
        dir_path = os.path.join(project_to_compile, directory)

        for entry in os.listdir(dir_path):
            if entry.lower().endswith('.png'):
                old_file_path = os.path.join(dir_path, entry)
                new_file_name = f"{directory}_{entry}"
                new_file_path = os.path.join(compiled_path, new_file_name)

                image = Image.open(old_file_path)
                resized_image = image.resize((256, 256), resample=Image.NEAREST)
                resized_image = remove_transparency(resized_image)
                resized_image.save(new_file_path)








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
