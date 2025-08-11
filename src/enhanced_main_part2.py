    # Canvas Event Handlers
    def on_button_press(self, event):
        \"\"\"Handle mouse button press on canvas\"\"\"
        if self.current_image is None:
            return
            
        # Get actual coordinates relative to image
        canvas_x = self.canvas.canvasx(event.x)
        canvas_y = self.canvas.canvasy(event.y)
        
        self.start_x = canvas_x
        self.start_y = canvas_y
        
        # Delete previous selection rectangle
        if self.rect:
            self.canvas.delete(self.rect)
        
        # Create new selection rectangle
        self.rect = self.canvas.create_rectangle(
            canvas_x, canvas_y, canvas_x, canvas_y,
            outline="#00ff00", width=2, tags="selection"
        )
    
    def on_mouse_drag(self, event):
        \"\"\"Handle mouse drag on canvas\"\"\"
        if self.current_image is None or self.rect is None:
            return
            
        canvas_x = self.canvas.canvasx(event.x)
        canvas_y = self.canvas.canvasy(event.y)
        
        # Update rectangle coordinates
        self.canvas.coords(self.rect, self.start_x, self.start_y, canvas_x, canvas_y)
    
    def on_button_release(self, event):
        \"\"\"Handle mouse button release on canvas\"\"\"
        if self.current_image is None or self.rect is None:
            return
            
        canvas_x = self.canvas.canvasx(event.x)
        canvas_y = self.canvas.canvasy(event.y)
        
        # Store crop coordinates
        x1 = min(self.start_x, canvas_x)
        y1 = min(self.start_y, canvas_y)
        x2 = max(self.start_x, canvas_x)
        y2 = max(self.start_y, canvas_y)
        
        # Convert to original image coordinates
        scale_x = self.current_image.width / self.displayed_image.width
        scale_y = self.current_image.height / self.displayed_image.height
        
        self.crop_coords = [
            int(x1 * scale_x), int(y1 * scale_y),
            int(x2 * scale_x), int(y2 * scale_y)
        ]
    
    def on_mouse_wheel(self, event):
        \"\"\"Handle mouse wheel for zooming\"\"\"
        if self.current_image is None:
            return
            
        # Determine zoom direction
        if event.delta > 0 or event.num == 4:
            self.zoom_in()
        elif event.delta < 0 or event.num == 5:
            self.zoom_out()
    
    # Zoom Operations
    def zoom_in(self):
        \"\"\"Zoom in on the image\"\"\"
        if self.current_image is None:
            return
        self.zoom_factor = min(self.zoom_factor * 1.2, 10.0)
        self.display_image()
    
    def zoom_out(self):
        \"\"\"Zoom out on the image\"\"\"
        if self.current_image is None:
            return
        self.zoom_factor = max(self.zoom_factor / 1.2, 0.1)
        self.display_image()
    
    def fit_to_window(self):
        \"\"\"Fit image to window\"\"\"
        if self.current_image is None:
            return
            
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        if canvas_width <= 1 or canvas_height <= 1:
            return
            
        img_width, img_height = self.current_image.size
        
        scale_x = canvas_width / img_width
        scale_y = canvas_height / img_height
        
        self.zoom_factor = min(scale_x, scale_y) * 0.9  # 90% of fit
        self.display_image()
    
    # Template Operations
    def load_templates(self):
        \"\"\"Load crop templates\"\"\"
        return {
            "Square (1:1)": (1, 1),
            "Portrait (4:5)": (4, 5),
            "Landscape (16:9)": (16, 9),
            "Instagram Post (1:1)": (1, 1),
            "Instagram Story (9:16)": (9, 16),
            "Facebook Cover (16:9)": (16, 9),
            "Twitter Header (3:1)": (3, 1),
            "YouTube Thumbnail (16:9)": (16, 9)
        }
    
    def apply_template(self, template_name):
        \"\"\"Apply crop template\"\"\"
        if self.current_image is None or template_name == "Custom":
            return
            
        if template_name in self.templates:
            ratio_w, ratio_h = self.templates[template_name]
            
            # Calculate crop area based on template
            img_width, img_height = self.current_image.size
            
            # Fit template to image
            if img_width / img_height > ratio_w / ratio_h:
                # Image is wider, fit to height
                crop_height = img_height
                crop_width = int(crop_height * ratio_w / ratio_h)
            else:
                # Image is taller, fit to width
                crop_width = img_width
                crop_height = int(crop_width * ratio_h / ratio_w)
            
            # Center the crop
            x1 = (img_width - crop_width) // 2
            y1 = (img_height - crop_height) // 2
            x2 = x1 + crop_width
            y2 = y1 + crop_height
            
            # Convert to display coordinates
            scale_x = self.displayed_image.width / self.current_image.width
            scale_y = self.displayed_image.height / self.current_image.height
            
            display_x1 = x1 * scale_x
            display_y1 = y1 * scale_y
            display_x2 = x2 * scale_x
            display_y2 = y2 * scale_y
            
            # Create selection rectangle
            if self.rect:
                self.canvas.delete(self.rect)
                
            self.rect = self.canvas.create_rectangle(
                display_x1, display_y1, display_x2, display_y2,
                outline="#00ff00", width=2, tags="selection"
            )
            
            # Store crop coordinates
            self.crop_coords = [x1, y1, x2, y2]
    
    def apply_custom_dimensions(self):
        \"\"\"Apply custom crop dimensions\"\"\"
        if self.current_image is None:
            return
            
        try:
            width = int(self.width_entry.get())
            height = int(self.height_entry.get())
            
            if width <= 0 or height <= 0:
                messagebox.showerror("Error", "Width and height must be positive numbers")
                return
                
            img_width, img_height = self.current_image.size
            
            # Center the crop
            x1 = max(0, (img_width - width) // 2)
            y1 = max(0, (img_height - height) // 2)
            x2 = min(img_width, x1 + width)
            y2 = min(img_height, y1 + height)
            
            # Convert to display coordinates
            scale_x = self.displayed_image.width / self.current_image.width
            scale_y = self.displayed_image.height / self.current_image.height
            
            display_x1 = x1 * scale_x
            display_y1 = y1 * scale_y
            display_x2 = x2 * scale_x
            display_y2 = y2 * scale_y
            
            # Create selection rectangle
            if self.rect:
                self.canvas.delete(self.rect)
                
            self.rect = self.canvas.create_rectangle(
                display_x1, display_y1, display_x2, display_y2,
                outline="#00ff00", width=2, tags="selection"
            )
            
            # Store crop coordinates
            self.crop_coords = [x1, y1, x2, y2]
            
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numeric values")
    
    # Basic Image Operations
    def crop_image(self):
        \"\"\"Crop the image to selected area\"\"\"
        if self.current_image is None or self.crop_coords is None:
            messagebox.showwarning("Warning", "Please select an area to crop")
            return
            
        x1, y1, x2, y2 = self.crop_coords
        
        # Ensure coordinates are within image bounds
        x1 = max(0, x1)
        y1 = max(0, y1)
        x2 = min(self.current_image.width, x2)
        y2 = min(self.current_image.height, y2)
        
        if x2 - x1 <= 0 or y2 - y1 <= 0:
            messagebox.showerror("Error", "Invalid crop area")
            return
            
        # Add to history
        self.add_to_history()
        
        # Crop the image
        self.current_image = self.current_image.crop((x1, y1, x2, y2))
        
        # Reset crop selection
        if self.rect:
            self.canvas.delete(self.rect)
            self.rect = None
        self.crop_coords = None
        
        # Update display
        self.display_image()
        self.update_info_label()
        
        messagebox.showinfo("Success", "Image cropped successfully!")
    
    def reset_image(self):
        \"\"\"Reset image to original\"\"\"
        if self.original_image is None:
            return
            
        self.current_image = self.original_image.copy()
        self.zoom_factor = 1.0
        self.rotation_angle = 0
        
        # Reset sliders
        self.brightness_slider.set(1.0)
        self.contrast_slider.set(1.0)
        self.saturation_slider.set(1.0)
        self.sharpness_slider.set(1.0)
        self.rotation_slider.set(0)
        
        # Clear selection
        if self.rect:
            self.canvas.delete(self.rect)
            self.rect = None
        self.crop_coords = None
        
        # Reset history
        self.history = [self.original_image.copy()]
        self.history_index = 0
        
        self.display_image()
        self.update_info_label()
    
    # History Management
    def add_to_history(self):
        \"\"\"Add current state to history\"\"\"
        # Remove any redo history when adding new state
        self.history = self.history[:self.history_index + 1]
        self.history.append(self.current_image.copy())
        self.history_index += 1
        
        # Limit history size
        if len(self.history) > 20:
            self.history.pop(0)
            self.history_index -= 1
    
    def undo(self):
        \"\"\"Undo last operation\"\"\"
        if self.history_index > 0:
            self.history_index -= 1
            self.current_image = self.history[self.history_index].copy()
            self.display_image()
            self.update_info_label()
    
    def redo(self):
        \"\"\"Redo last undone operation\"\"\"
        if self.history_index < len(self.history) - 1:
            self.history_index += 1
            self.current_image = self.history[self.history_index].copy()
            self.display_image()
            self.update_info_label()
    
    # Transform Operations
    def rotate_image(self, angle):
        \"\"\"Rotate image by angle\"\"\"
        if self.current_image is None:
            return
            
        self.rotation_angle = angle
        self.add_to_history()
        
        # Rotate image
        self.current_image = self.current_image.rotate(-angle, expand=True, fillcolor='white')
        self.display_image()
        self.update_info_label()
    
    def quick_rotate(self, angle):
        \"\"\"Quick rotate by 90 degree increments\"\"\"
        if self.current_image is None:
            return
            
        self.add_to_history()
        
        if angle == 90:
            self.current_image = self.current_image.transpose(Image.ROTATE_270)
        elif angle == -90:
            self.current_image = self.current_image.transpose(Image.ROTATE_90)
        elif angle == 180:
            self.current_image = self.current_image.transpose(Image.ROTATE_180)
            
        self.display_image()
        self.update_info_label()
    
    def flip_horizontal(self):
        \"\"\"Flip image horizontally\"\"\"
        if self.current_image is None:
            return
            
        self.add_to_history()
        self.current_image = self.current_image.transpose(Image.FLIP_LEFT_RIGHT)
        self.display_image()
    
    def flip_vertical(self):
        \"\"\"Flip image vertically\"\"\"
        if self.current_image is None:
            return
            
        self.add_to_history()
        self.current_image = self.current_image.transpose(Image.FLIP_TOP_BOTTOM)
        self.display_image()
    
    # Image Adjustment Operations
    def adjust_brightness(self, value):
        \"\"\"Adjust image brightness\"\"\"
        if self.current_image is None:
            return
        self.apply_adjustments()
    
    def adjust_contrast(self, value):
        \"\"\"Adjust image contrast\"\"\"
        if self.current_image is None:
            return
        self.apply_adjustments()
    
    def adjust_saturation(self, value):
        \"\"\"Adjust image saturation\"\"\"
        if self.current_image is None:
            return
        self.apply_adjustments()
    
    def adjust_sharpness(self, value):
        \"\"\"Adjust image sharpness\"\"\"
        if self.current_image is None:
            return
        self.apply_adjustments()
    
    def apply_adjustments(self):
        \"\"\"Apply all current adjustments\"\"\"
        if len(self.history) == 0:
            return
            
        # Start with base image from history
        base_image = self.history[0].copy()
        
        # Apply brightness
        brightness = self.brightness_slider.get()
        if brightness != 1.0:
            enhancer = ImageEnhance.Brightness(base_image)
            base_image = enhancer.enhance(brightness)
        
        # Apply contrast
        contrast = self.contrast_slider.get()
        if contrast != 1.0:
            enhancer = ImageEnhance.Contrast(base_image)
            base_image = enhancer.enhance(contrast)
        
        # Apply saturation
        saturation = self.saturation_slider.get()
        if saturation != 1.0:
            enhancer = ImageEnhance.Color(base_image)
            base_image = enhancer.enhance(saturation)
        
        # Apply sharpness
        sharpness = self.sharpness_slider.get()
        if sharpness != 1.0:
            enhancer = ImageEnhance.Sharpness(base_image)
            base_image = enhancer.enhance(sharpness)
        
        self.current_image = base_image
        self.display_image()
    
    # Filter Operations
    def apply_filter(self, filter_name):
        \"\"\"Apply image filter\"\"\"
        if self.current_image is None:
            return
            
        self.add_to_history()
        
        try:
            if filter_name == "Blur":
                self.current_image = self.current_image.filter(ImageFilter.BLUR)
            elif filter_name == "Sharpen":
                self.current_image = self.current_image.filter(ImageFilter.SHARPEN)
            elif filter_name == "Edge Enhance":
                self.current_image = self.current_image.filter(ImageFilter.EDGE_ENHANCE)
            elif filter_name == "Smooth":
                self.current_image = self.current_image.filter(ImageFilter.SMOOTH)
            elif filter_name == "Emboss":
                self.current_image = self.current_image.filter(ImageFilter.EMBOSS)
            elif filter_name == "Find Edges":
                self.current_image = self.current_image.filter(ImageFilter.FIND_EDGES)
                
            self.display_image()
            messagebox.showinfo("Success", f"{filter_name} filter applied successfully!")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to apply filter: {str(e)}")
    
    # Advanced Features
    def auto_enhance(self):
        \"\"\"Automatically enhance image\"\"\"
        if self.current_image is None:
            return
            
        self.add_to_history()
        
        try:
            # Convert PIL to OpenCV
            cv_image = cv2.cvtColor(np.array(self.current_image), cv2.COLOR_RGB2BGR)
            
            # Apply CLAHE (Contrast Limited Adaptive Histogram Equalization)
            lab = cv2.cvtColor(cv_image, cv2.COLOR_BGR2LAB)
            l, a, b = cv2.split(lab)
            
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
            l = clahe.apply(l)
            
            enhanced = cv2.merge([l, a, b])
            enhanced = cv2.cvtColor(enhanced, cv2.COLOR_LAB2BGR)
            
            # Convert back to PIL
            self.current_image = Image.fromarray(cv2.cvtColor(enhanced, cv2.COLOR_BGR2RGB))
            self.display_image()
            
            messagebox.showinfo("Success", "Auto enhancement applied!")
            
        except Exception as e:
            messagebox.showerror("Error", f"Auto enhancement failed: {str(e)}")
    
    def reduce_noise(self):
        \"\"\"Reduce image noise\"\"\"
        if self.current_image is None:
            return
            
        self.add_to_history()
        
        try:
            # Convert to OpenCV format
            cv_image = cv2.cvtColor(np.array(self.current_image), cv2.COLOR_RGB2BGR)
            
            # Apply Non-Local Means Denoising
            denoised = cv2.fastNlMeansDenoisingColored(cv_image, None, 10, 10, 7, 21)
            
            # Convert back to PIL
            self.current_image = Image.fromarray(cv2.cvtColor(denoised, cv2.COLOR_BGR2RGB))
            self.display_image()
            
            messagebox.showinfo("Success", "Noise reduction applied!")
            
        except Exception as e:
            messagebox.showerror("Error", f"Noise reduction failed: {str(e)}")
    
    def histogram_equalization(self):
        \"\"\"Apply histogram equalization\"\"\"
        if self.current_image is None:
            return
            
        self.add_to_history()
        
        try:
            # Convert to numpy array
            img_array = np.array(self.current_image)
            
            # Apply histogram equalization to each channel
            if len(img_array.shape) == 3:
                # Color image
                img_yuv = cv2.cvtColor(img_array, cv2.COLOR_RGB2YUV)
                img_yuv[:, :, 0] = cv2.equalizeHist(img_yuv[:, :, 0])
                img_eq = cv2.cvtColor(img_yuv, cv2.COLOR_YUV2RGB)
            else:
                # Grayscale image
                img_eq = cv2.equalizeHist(img_array)
            
            self.current_image = Image.fromarray(img_eq)
            self.display_image()
            
            messagebox.showinfo("Success", "Histogram equalization applied!")
            
        except Exception as e:
            messagebox.showerror("Error", f"Histogram equalization failed: {str(e)}")
    
    def color_balance(self):
        \"\"\"Automatic color balance\"\"\"
        if self.current_image is None:
            return
            
        self.add_to_history()
        
        try:
            # Convert to numpy array
            img_array = np.array(self.current_image)
            
            # Simple white balance using gray world assumption
            img_float = img_array.astype(np.float32)
            
            # Calculate mean for each channel
            mean_b, mean_g, mean_r = np.mean(img_float, axis=(0, 1))
            
            # Calculate scaling factors
            gray_mean = (mean_b + mean_g + mean_r) / 3
            scale_b = gray_mean / mean_b if mean_b > 0 else 1
            scale_g = gray_mean / mean_g if mean_g > 0 else 1
            scale_r = gray_mean / mean_r if mean_r > 0 else 1
            
            # Apply scaling
            img_float[:, :, 0] *= scale_b  # Blue channel
            img_float[:, :, 1] *= scale_g  # Green channel
            img_float[:, :, 2] *= scale_r  # Red channel
            
            # Clip values and convert back to uint8
            img_balanced = np.clip(img_float, 0, 255).astype(np.uint8)
            
            self.current_image = Image.fromarray(img_balanced)
            self.display_image()
            
            messagebox.showinfo("Success", "Color balance applied!")
            
        except Exception as e:
            messagebox.showerror("Error", f"Color balance failed: {str(e)}")
    
    def perspective_correction(self):
        \"\"\"Interactive perspective correction\"\"\"
        if self.current_image is None:
            return
            
        messagebox.showinfo("Perspective Correction", 
                          "Click on four corners of the object you want to correct.\\n" +
                          "Click in this order: Top-left, Top-right, Bottom-right, Bottom-left")
        
        # This would require a more complex implementation
        # For now, show a placeholder
        messagebox.showinfo("Info", "Perspective correction feature will be implemented in a future update")
    
    # Batch Operations
    def batch_crop(self):
        \"\"\"Batch crop multiple images\"\"\"
        if self.crop_coords is None:
            messagebox.showwarning("Warning", "Please select a crop area first")
            return
            
        input_folder = filedialog.askdirectory(title="Select input folder")
        if not input_folder:
            return
            
        output_folder = filedialog.askdirectory(title="Select output folder")
        if not output_folder:
            return
            
        # Get crop dimensions from current selection
        x1, y1, x2, y2 = self.crop_coords
        crop_width = x2 - x1
        crop_height = y2 - y1
        
        try:
            processed = 0
            supported_formats = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.gif', '.webp']
            
            for filename in os.listdir(input_folder):
                if any(filename.lower().endswith(fmt) for fmt in supported_formats):
                    try:
                        # Open image
                        img_path = os.path.join(input_folder, filename)
                        img = Image.open(img_path)
                        
                        # Calculate crop area (centered)
                        img_width, img_height = img.size
                        crop_x1 = max(0, (img_width - crop_width) // 2)
                        crop_y1 = max(0, (img_height - crop_height) // 2)
                        crop_x2 = min(img_width, crop_x1 + crop_width)
                        crop_y2 = min(img_height, crop_y1 + crop_height)
                        
                        # Crop and save
                        cropped = img.crop((crop_x1, crop_y1, crop_x2, crop_y2))
                        
                        # Generate output filename
                        name, ext = os.path.splitext(filename)
                        output_path = os.path.join(output_folder, f"{name}_cropped{ext}")
                        
                        cropped.save(output_path)
                        processed += 1
                        
                    except Exception as e:
                        print(f"Error processing {filename}: {e}")
            
            messagebox.showinfo("Success", f"Batch crop completed! Processed {processed} images.")
            
        except Exception as e:
            messagebox.showerror("Error", f"Batch crop failed: {str(e)}")
    
    def batch_resize(self):
        \"\"\"Batch resize multiple images\"\"\"
        resize_window = ctk.CTkToplevel(self.root)
        resize_window.title("Batch Resize")
        resize_window.geometry("300x200")
        resize_window.transient(self.root)
        resize_window.grab_set()
        
        # Width input
        ctk.CTkLabel(resize_window, text="Target Width:").pack(pady=5)
        width_entry = ctk.CTkEntry(resize_window, placeholder_text="800")
        width_entry.pack(pady=5)
        
        # Height input
        ctk.CTkLabel(resize_window, text="Target Height:").pack(pady=5)
        height_entry = ctk.CTkEntry(resize_window, placeholder_text="600")
        height_entry.pack(pady=5)
        
        # Maintain aspect ratio checkbox
        maintain_aspect = ctk.CTkCheckBox(resize_window, text="Maintain aspect ratio")
        maintain_aspect.pack(pady=10)
        maintain_aspect.select()
        
        def do_batch_resize():
            try:
                target_width = int(width_entry.get())
                target_height = int(height_entry.get())
                
                input_folder = filedialog.askdirectory(title="Select input folder")
                if not input_folder:
                    return
                    
                output_folder = filedialog.askdirectory(title="Select output folder")
                if not output_folder:
                    return
                
                processed = 0
                supported_formats = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.gif', '.webp']
                
                for filename in os.listdir(input_folder):
                    if any(filename.lower().endswith(fmt) for fmt in supported_formats):
                        try:
                            # Open image
                            img_path = os.path.join(input_folder, filename)
                            img = Image.open(img_path)
                            
                            # Resize image
                            if maintain_aspect.get():
                                img.thumbnail((target_width, target_height), Image.Resampling.LANCZOS)
                                resized = img
                            else:
                                resized = img.resize((target_width, target_height), Image.Resampling.LANCZOS)
                            
                            # Save resized image
                            name, ext = os.path.splitext(filename)
                            output_path = os.path.join(output_folder, f"{name}_resized{ext}")
                            
                            resized.save(output_path, quality=95, optimize=True)
                            processed += 1
                            
                        except Exception as e:
                            print(f"Error processing {filename}: {e}")
                
                resize_window.destroy()
                messagebox.showinfo("Success", f"Batch resize completed! Processed {processed} images.")
                
            except ValueError:
                messagebox.showerror("Error", "Please enter valid numeric values")
            except Exception as e:
                messagebox.showerror("Error", f"Batch resize failed: {str(e)}")
        
        ctk.CTkButton(resize_window, text="Start Batch Resize", command=do_batch_resize).pack(pady=20)
    
    # Utility Functions
    def load_presets(self):
        \"\"\"Load application presets\"\"\"
        # This would load user preferences, recent files, etc.
        pass
    
    def run(self):
        \"\"\"Start the application\"\"\"
        self.root.mainloop()

def print_info():
    \"\"\"Print application information\"\"\"
    logo = r\"\"\"
   _____ _   _ _   _ ___ _   _ _   _  ___ _____ ____  
  |  ___| \\ | | | | | | \\ | | | \\ | |/ ___| ____|  |  _ \\ 
  | |_  |  \\| | |_| | |  \\| | |  \\| | |  _|  _|   | | | |
  |  _| | |\\  |  _  | | |\\  | | |\\  | |_| | |___  | |_| |
  |_|   |_| \\_|_| |_|_|_| \\_|_|_| \\_|\\____\\____| |____/ 
                                                        
   ___ __  __    _    ____ _____    ____ ____   ___  ____  ____  _____ ____  
  |_ _|  \\/  |  / \\  / ___| ____|  / ___|  _ \\ / _ \\|  _ \\|  _ \\| ____|  _ \\ 
   | || |\\/| | / _ \\| |  _|  _|   | |   | |_) | | | | |_) | |_) |  _| | |_) |
   | || |  | |/ ___ \\ |_| | |___  | |___|  _ <| |_| |  __/|  __/| |___|  _ < 
  |___|_|  |_/_/   \\_\\____|_____|  \\____|_| \\_\\___/|_|   |_|   |_____|_| \\_\\
                                                                            
    \"\"\"
    print("=" * 80)
    print(logo)
    print("Enhanced Image Cropper v1.0.2")
    print("A comprehensive photo editing application with modern features")
    print("Built with Python, tkinter, CustomTkinter, OpenCV, and PIL")
    print("=" * 80)

if __name__ == "__main__":
    print_info()
    app = EnhancedImageCropper()
    app.run()
