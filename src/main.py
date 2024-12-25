import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

class ImageBinder:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Combiner")
        self.root.geometry("600x500")

        # Frame for canvas and vertical scroll bar
        self.canvas_frame = tk.Frame(root)
        self.canvas_frame.pack(fill=tk.BOTH, expand=True)

        # Canvas for displaying images
        self.canvas = tk.Canvas(self.canvas_frame, bg='Grey')
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.canvas.bind("<Enter>", self.bind_mouse_scroll)
        self.canvas.bind("<Leave>", self.unbind_mouse_scroll)

        # Vertical Scrollbar
        self.scrollbar_v = tk.Scrollbar(self.canvas_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scrollbar_v.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Horizontal Scrollbar
        self.scrollbar_h = tk.Scrollbar(self.root, orient=tk.HORIZONTAL, command=self.canvas.xview)
        self.scrollbar_h.pack(side=tk.BOTTOM, fill=tk.X)

        # Connect scrollbars with the canvas
        self.canvas.config(yscrollcommand=self.scrollbar_v.set)
        self.canvas.config(xscrollcommand=self.scrollbar_h.set)

        self.images = []  # List to store selected images
        self.image_names = []  # List to store image filenames for display
        self.image_labels = []  # List to store ImageTk labels for preview

        # Frame to hold the buttons at the bottom
        self.button_frame = tk.Frame(root)
        self.button_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.choose_button = tk.Button(self.button_frame, text="Choose Images", command=self.select_images)
        self.choose_button.pack(side=tk.LEFT, padx=10)

        self.save_button = tk.Button(self.button_frame, text="Save Image", command=self.save_image)
        self.save_button.pack(side=tk.LEFT, padx=10)

        # Frame for displaying the list of image names
        self.list_frame = tk.Frame(root)
        self.list_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10)

        # Listbox to display the image names
        self.listbox = tk.Listbox(self.list_frame, selectmode=tk.SINGLE, height=15)
        self.listbox.pack(side=tk.LEFT, fill=tk.Y)

        # Scrollbar for the listbox
        self.listbox_scroll = tk.Scrollbar(self.list_frame, orient=tk.VERTICAL, command=self.listbox.yview)
        self.listbox_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox.config(yscrollcommand=self.listbox_scroll.set)

        # Buttons to move images up and down
        self.move_up_button = tk.Button(self.list_frame, text="Move Up", command=self.move_image_up)
        self.move_up_button.pack(side=tk.TOP, fill=tk.X)
        
        self.move_down_button = tk.Button(self.list_frame, text="Move Down", command=self.move_image_down)
        self.move_down_button.pack(side=tk.TOP, fill=tk.X)
       
    def bind_mouse_scroll(self, event):
        if self.root.tk.call('tk', 'windowingsystem') == 'x11':  # Linux
            self.canvas.bind("<Button-4>", self.on_mouse_wheel)
            self.canvas.bind("<Button-5>", self.on_mouse_wheel)
        else:  
            self.canvas.bind("<MouseWheel>", self.on_mouse_wheel) # Windows and macOS

    def unbind_mouse_scroll(self, event):
        if self.root.tk.call('tk', 'windowingsystem') == 'x11':
            self.canvas.unbind("<Button-4>")
            self.canvas.unbind("<Button-5>")
        else:
            self.canvas.unbind("<MouseWheel>")

    def on_mouse_wheel(self, event):
        if event.num == 4 or event.delta > 0:  # Scroll up
            self.canvas.yview_scroll(-1, "units")
        elif event.num == 5 or event.delta < 0:  # Scroll down
            self.canvas.yview_scroll(1, "units")

    def select_images(self):
        file_paths = filedialog.askopenfilenames(
            title="Select Images", 
            filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg;*.jpeg")],
        )
        
        if file_paths:
            self.images = [Image.open(path) for path in file_paths]  # Open the images
            self.image_names = [path.split("/")[-1] for path in file_paths]  # Extract image names
            self.display_images()
            self.update_image_list()

    def display_images(self):
        self.canvas.delete("all")
      
        # Clear the image labels list
        self.image_labels = []

        # Display selected images in the canvas
        y_offset = 10
        max_width = 0
        total_height = 0
        
        for idx, image in enumerate(self.images):
            image_tk = ImageTk.PhotoImage(image) # Convert image to Tkinter-compatible format
            self.image_labels.append(image_tk)# Store reference to avoid garbage collection

            # Display the image on the canvas
            self.canvas.create_image(10, y_offset, anchor=tk.NW, image=image_tk)

            max_width = max(max_width, image.width)
            total_height += image.height + 10

            y_offset += image.height + 10

        # Update the canvas scroll region to fit all images
        self.canvas.config(scrollregion=(0, 0, max_width, total_height))

    def update_image_list(self):
        # Clear the listbox and add updated image names
        self.listbox.delete(0, tk.END)
        for name in self.image_names:
            self.listbox.insert(tk.END, name)

    def move_image_up(self):
        # Get the selected image's index
        selected_index = self.listbox.curselection()
        if selected_index:
            idx = selected_index[0]
            if idx > 0:
                # Move the image and its name up in the list
                self.images[idx], self.images[idx - 1] = self.images[idx - 1], self.images[idx]
                self.image_names[idx], self.image_names[idx - 1] = self.image_names[idx - 1], self.image_names[idx]
                self.display_images()
                self.update_image_list()
                # Re-select the moved item
                self.listbox.selection_set(idx - 1)

    def move_image_down(self):
        # Get the selected image's index
        selected_index = self.listbox.curselection()
        if selected_index:
            idx = selected_index[0]
            if idx < len(self.images) - 1:
                # Move the image and its name down in the list
                self.images[idx], self.images[idx + 1] = self.images[idx + 1], self.images[idx]
                self.image_names[idx], self.image_names[idx + 1] = self.image_names[idx + 1], self.image_names[idx]
                self.display_images()
                self.update_image_list()
                # Re-select the moved item
                self.listbox.selection_set(idx + 1)

    def save_image(self):
        # Ask user for save location and file name
        save_path = filedialog.asksaveasfilename(
            title="Save Image As", 
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg;*.jpeg")]
        )
        
        if save_path:
            # Ask user to choose horizontal or vertical combination
            choice = messagebox.askquestion("Combine Images", "Combine images horizontally? Click 'No' for vertical.")

            # Combine images
            if choice == 'yes':  # Horizontal combination
                combined_width = sum(image.width for image in self.images)
                combined_height = max(image.height for image in self.images)
                
                combined_image = Image.new("RGBA", (combined_width, combined_height), (0, 0, 0, 0))  # Transparent
                
                x_offset = 0
                for image in self.images:
                    combined_image.paste(image, (x_offset, 0))
                    x_offset += image.width  
            else:  # Vertical combination
                combined_width = max(image.width for image in self.images)
                combined_height = sum(image.height for image in self.images)
                
                combined_image = Image.new("RGBA", (combined_width, combined_height), (0, 0, 0, 0))  # Transparent
                
                y_offset = 0
                for image in self.images:
                    combined_image.paste(image, (0, y_offset))
                    y_offset += image.height  # Update y_offset

                # Check for JPEG format (no transparency support)
            if save_path.lower().endswith(".jpg") or save_path.lower().endswith(".jpeg"):
                combined_image = combined_image.convert("RGB")  # Remove transparency

                # Save the combined image
            combined_image.save(save_path)
        else:
            messagebox.showerror("Error", "Failed to save the image.")

# Create Tkinter window
root = tk.Tk()

# Create an instance of the ImageCombinerApp
app = ImageBinder(root)

# Start the Tkinter event loop
root.mainloop()
