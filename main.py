
kuda = "https://discord.com/api/v9/channels/1070050111368994848/messages"
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import requests
import time

class DiscordApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Discord App")

        self.message_label = tk.Label(root, text="Message:")
        self.message_label.pack()

        self.message_entry = tk.Entry(root, width=40)
        self.message_entry.pack(padx=25)

        self.message_label = tk.Label(root, text="Authorition:")
        self.message_label.pack()

        self.message_entry_authority = tk.Entry(root)
        self.message_entry_authority.pack()

        self.message_label = tk.Label(root, text="Discord Channel id:")
        self.message_label.pack()

        self.message_entry_id = tk.Entry(root)
        self.message_entry_id.pack()

        self.upload_button = tk.Button(root, text="Upload Photo(s)", command=self.upload_photos)
        self.upload_button.pack()
        self.image_labels = []
        self.image_previews = []
        self.remove_buttons = []
        self.image_paths = []  # Track selected image paths

        self.send_button = tk.Button(root, text="Send", command=self.send_message)
        self.send_button.pack()

    def upload_photos(self):
        selected_photos = filedialog.askopenfilenames()
        for photo in selected_photos:
            self.display_image(photo)

    def display_image(self, image_path):
        img = Image.open(image_path)
        img.thumbnail((150, 150))
        image_preview = ImageTk.PhotoImage(img)
        self.image_previews.append(image_preview)

        image_label = tk.Label(self.root, image=image_preview)
        image_label.pack()
        self.image_labels.append(image_label)
        self.image_paths.append(image_path)  # Store the selected image path

        remove_button = tk.Button(self.root, text="Remove", command=lambda path=image_path: self.remove_image(path))
        remove_button.pack()
        self.remove_buttons.append(remove_button)

    def remove_image(self, image_path):
        index = self.image_paths.index(image_path)
        self.image_labels[index].destroy()
        self.remove_buttons[index].destroy()
        self.image_labels.pop(index)
        self.remove_buttons.pop(index)
        self.image_previews.pop(index)
        self.image_paths.pop(index)

    def send_message(self):
        message = self.message_entry.get()
        message_authority = self.message_entry_authority.get()
        message_id = self.message_entry_id.get()

        # Prepare the message data
        payload = {
            "content": message,
        }
        files = {}
        for image_path in range(len(self.image_paths)):
            files[f"file{image_path}"] = open(self.image_paths[image_path], "rb")
            print(files)
        print(message, message_authority)
        # Send the request to Discord
        while True:
            time.sleep(5)
            response = requests.post(f"https://discord.com/api/v9/channels/{message_id}/messages", headers={
                "Authorization": message_authority
            }, data=payload, files=files)
            if response.status_code == 200:
                print("Message sent successfully!")
            else:
                print("Error sending message:", response.text)
        

if __name__ == "__main__":
    root = tk.Tk()
    app = DiscordApp(root)
    root.mainloop()
