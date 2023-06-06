import os
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

def list_directories():
    dirs = []
    dirs.extend(['ITEMS/' + d for d in os.listdir('./ITEMS/') if os.path.isdir(os.path.join('./ITEMS/', d))])
    dirs.extend(['BLOCKS/' + d for d in os.listdir('./BLOCKS/') if os.path.isdir(os.path.join('./BLOCKS/', d))])
    return dirs

def find_all_images_and_tag_files(directory):
    image_tag_pairs = []
    for subdir, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                image_path = os.path.join(subdir, file)
                tag_file_path = os.path.join(subdir, 'Tags', os.path.splitext(file)[0] + '.txt')
                image_tag_pairs.append((image_path, tag_file_path))
    return image_tag_pairs

def get_tag_content(tag_file_path):
    with open(tag_file_path, 'r') as file:
        return file.read()

def display_image_and_form(image_path, tag_file_path, remaining_count, display_next_func):
    root = tk.Tk()

    with Image.open(image_path) as img:
        img = img.resize((256, 256), resample=Image.NEAREST)
        img = ImageTk.PhotoImage(img)

    label_img = tk.Label(root, image=img)
    label_img.pack()

    directory_name = os.path.dirname(image_path)
    image_name = os.path.basename(image_path)

    label_info = tk.Label(root, text=f"Directory: {directory_name}\nImage: {image_name}")
    label_info.pack()

    label_remaining = tk.Label(root, text=f"Images remaining: {remaining_count}")
    label_remaining.pack()

    input_text = tk.Entry(root)
    input_text.insert(tk.END, get_tag_content(tag_file_path))
    input_text.pack()

    def save_new_content():
        new_content = input_text.get()

        with open(tag_file_path, 'w') as file:
            file.write(new_content)

        root.destroy()
        display_next_func()

    save_button = tk.Button(root, text='Save', command=save_new_content)
    save_button.pack()

    def skip():
        root.destroy()
        display_next_func()

    skip_button = tk.Button(root, text='Skip', command=skip)
    skip_button.pack()

    def remove_image():
        answer = messagebox.askyesno('Remove image', 'Are you sure you want to delete the image?')
        if answer:
            os.remove(image_path)
            root.destroy()
            display_next_func()

    remove_button = tk.Button(root, text='Remove', command=remove_image)
    remove_button.pack()

    root.mainloop()

def main():
    dirs = list_directories()

    for i, d in enumerate(dirs):
        print(f'{i + 1}. {d}')

    chosen_index = int(input('Choose a directory by entering the number: '))
    chosen_dir = dirs[chosen_index - 1]

    image_tag_pairs = find_all_images_and_tag_files(chosen_dir)

    def display_image_pairs_iterator(image_pairs):
        if not image_pairs:
            return
        image_path, tag_file_path = image_pairs.pop(0)
        remaining_count = len(image_pairs)
        display_image_and_form(image_path, tag_file_path, remaining_count, lambda: display_image_pairs_iterator(image_pairs))

    display_image_pairs_iterator(image_tag_pairs)

if __name__ == '__main__':
    main()
