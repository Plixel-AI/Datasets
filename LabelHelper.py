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

def display_images(image_tag_pairs):
    if not image_tag_pairs:
        return

    root = tk.Tk()

    current_idx = 0
    pairs = image_tag_pairs

    with Image.open(pairs[current_idx][0]) as img:
        img = img.resize((256, 256), resample=Image.NEAREST)
        img = ImageTk.PhotoImage(img)

    label_img = tk.Label(root, image=img)
    label_img.pack()

    label_info = tk.Label(root)
    label_info.pack()

    label_remaining = tk.Label(root)
    label_remaining.pack()

    input_text = tk.Entry(root)
    input_text.pack()

    def navigate_images(step):
        nonlocal current_idx
        current_idx += step
        current_idx = max(0, min(current_idx, len(pairs) - 1))
        update_image(current_idx, pairs, label_img, label_info, label_remaining, input_text)

    def save_new_content():
        new_content = input_text.get()
        with open(pairs[current_idx][1], 'w') as file:
            file.write(new_content)
        # After saving, move forward one image
        navigate_images(1)

    save_button = tk.Button(root, text='Save', command=save_new_content)
    save_button.pack()

    def remove_image():
        answer = messagebox.askyesno('Remove image', 'Are you sure you want to delete the image?')
        if answer:
            os.remove(pairs[current_idx][0])
            del pairs[current_idx]
            if not pairs:
                root.destroy()
            else:
                update_image(current_idx, pairs, label_img, label_info, label_remaining, input_text)

    remove_button = tk.Button(root, text='Remove', command=remove_image)
    remove_button.pack()

    def navigate_images_with_event(event, step):
        if event.state == 1:  # Shift is pressed
            step *= 100
        elif event.state == 4:  # Control is pressed
            step *= 50
        elif event.state == 5:  # Shift and Control are both pressed
            step *= 500
        navigate_images(step)

    def on_back_click(event):
        navigate_images_with_event(event, -1)

    def on_forward_click(event):
        navigate_images_with_event(event, 1)

    back_button = tk.Button(root, text='Back')
    back_button.bind('<Button-1>', on_back_click)
    back_button.pack()

    forward_button = tk.Button(root, text='Forward')
    forward_button.bind('<Button-1>', on_forward_click)
    forward_button.pack()

    def update_image(idx, pairs, img_label, info_label, remaining_label, input_text):
        image_path, tag_file_path = pairs[idx]
        with Image.open(image_path) as img:
            img = img.resize((256, 256), resample=Image.NEAREST)
            img = ImageTk.PhotoImage(img)

        img_label.config(image=img)
        img_label.image = img

        directory_name = os.path.dirname(image_path)
        image_name = os.path.basename(image_path)

        info_label.config(text=f"Directory: {directory_name}\nImage: {image_name}")

        remaining_count = len(pairs) - idx - 1
        remaining_label.config(text=f"Images remaining: {remaining_count}")

        input_text.delete(0, tk.END)
        input_text.insert(tk.END, get_tag_content(tag_file_path))

    update_image(current_idx, pairs, label_img, label_info, label_remaining, input_text)
    root.mainloop()

def main():
    dirs = list_directories()

    for i, d in enumerate(dirs):
        print(f'{i + 1}. {d}')

    chosen_index = int(input('Choose a directory by entering the number: '))
    chosen_dir = dirs[chosen_index - 1]

    image_tag_pairs = find_all_images_and_tag_files(chosen_dir)
    display_images(image_tag_pairs)

if __name__ == '__main__':
    main()
