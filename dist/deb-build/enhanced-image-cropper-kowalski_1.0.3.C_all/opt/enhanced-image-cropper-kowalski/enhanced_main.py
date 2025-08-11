#!/usr/bin/env python3
"""
Enhanced Image Cropper v1.0.3.C
A comprehensive photo editing application with modern features and Kowalski icon

Features:
1. Modern dark theme UI with CustomTkinter
2. Advanced cropping with templates (Instagram, YouTube, etc.)
3. Image adjustments (brightness, contrast, saturation, sharpness)
4. Filters (blur, sharpen, edge enhance, emboss, etc.)
5. Transform operations (rotate, flip)
6. Advanced features (auto enhance, noise reduction, histogram equalization)
7. Batch operations (crop, resize multiple images)
8. Zoom and pan functionality
9. Undo/Redo system
10. Export with quality settings
11. Custom scaling and aspect ratio tools
12. Professional image enhancement tools
13. Kowalski icon integration
14. Optimized performance and error handling
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, colorchooser
import customtkinter as ctk
from PIL import Image, ImageTk, ImageEnhance, ImageFilter, ImageOps
import cv2
import numpy as np
import os
import json
from datetime import datetime
import math
from scipy import ndimage
from skimage import restoration, exposure, transform
import sys
import threading
import gc

# Set theme and appearance
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class EnhancedImageCropper:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Enhanced Image Cropper v1.0.3.C - Kowalski Edition")
        self.root.geometry("1400x900")
        self.root.minsize(1200, 800)
        
        # Set application icon
        self.set_app_icon()
        
        # Initialize variables
        self.original_image = None
        self.current_image = None
        self.displayed_image = None
        self.tk_image = None
        self.crop_coords = None
        self.rect = None
        self.start_x = None
        self.start_y = None
        self.zoom_factor = 1.0
        self.rotation_angle = 0
        self.history = []
        self.history_index = -1
        self.templates = self.load_templates()
        self.processing = False
        
        # Setup UI
        self.setup_ui()
        self.setup_canvas()
        self.load_presets()
        
        # Show startup banner
        self.show_startup_banner()
        
    def set_app_icon(self):
        """Set the application icon"""
        try:
            icon_path = os.path.join(os.path.dirname(__file__), "icons", "app_icon.png")
            if os.path.exists(icon_path):
                icon_image = Image.open(icon_path)
                # Convert to compatible format and resize for icon
                icon_image = icon_image.convert("RGBA")
                icon_image = icon_image.resize((64, 64), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(icon_image)
                self.root.iconphoto(True, photo)
                print(f"✅ Application icon set: {icon_path}")
            else:
                print(f"⚠️  Icon not found at: {icon_path}")
        except Exception as e:
            print(f"⚠️  Could not set icon: {e}")
    
    def show_startup_banner(self):
        """Display startup information"""
        banner = """
================================================================================

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
                                                                            
    
Enhanced Image Cropper v1.0.3.C - Kowalski Edition
A comprehensive photo editing application with modern features
Built with Python, tkinter, CustomTkinter, OpenCV, and PIL

🐧 KOWALSKI EDITION - Analysis Complete!
✅ Modern dark theme UI
✅ Professional crop templates (Instagram, YouTube, etc.)
✅ Advanced image adjustments (brightness, contrast, saturation)
✅ Professional filters and effects
✅ Smart auto-enhancement with CLAHE
✅ Noise reduction algorithms
✅ Histogram equalization
✅ Automatic color balance
✅ Batch processing for multiple images
✅ Zoom and pan functionality
✅ Undo/Redo system with 20-level history
✅ Export with quality settings
✅ Transform operations (rotate, flip)
✅ Optimized performance and memory management
================================================================================"""
        print(banner)
    
    def setup_ui(self):
        """Setup the modern user interface"""
        
        # Main container
        main_container = ctk.CTkFrame(self.root)
        main_container.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Left panel for tools
        self.left_panel = ctk.CTkFrame(main_container, width=280)
        self.left_panel.pack(side="left", fill="y", padx=(0, 10))
        self.left_panel.pack_propagate(False)
        
        # Center panel for image display
        self.center_panel = ctk.CTkFrame(main_container)
        self.center_panel.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        # Right panel for properties
        self.right_panel = ctk.CTkFrame(main_container, width=250)
        self.right_panel.pack(side="right", fill="y")
        self.right_panel.pack_propagate(False)
        
        self.setup_left_panel()
        self.setup_center_panel()
        self.setup_right_panel()
        
    def setup_left_panel(self):
        """Setup left panel with editing tools"""
        
        # File Operations
        file_frame = ctk.CTkFrame(self.left_panel)
        file_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(file_frame, text="📁 File Operations", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=5)
        
        ctk.CTkButton(file_frame, text="Open Image", command=self.open_image).pack(fill="x", pady=2)
        ctk.CTkButton(file_frame, text="Save Image", command=self.save_image).pack(fill="x", pady=2)
        ctk.CTkButton(file_frame, text="Export As...", command=self.export_image).pack(fill="x", pady=2)
        
        # Crop Templates
        template_frame = ctk.CTkFrame(self.left_panel)
        template_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(template_frame, text="📐 Crop Templates", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=5)
        
        self.template_var = ctk.StringVar(value="Custom")
        template_options = ["Custom", "Square (1:1)", "Portrait (4:5)", "Landscape (16:9)", 
                           "Instagram Post (1:1)", "Instagram Story (9:16)", "Facebook Cover (16:9)",
                           "Twitter Header (3:1)", "YouTube Thumbnail (16:9)"]
        
        self.template_menu = ctk.CTkOptionMenu(template_frame, variable=self.template_var, 
                                              values=template_options, command=self.apply_template)
        self.template_menu.pack(fill="x", pady=2)
        
        # Custom dimensions
        dim_frame = ctk.CTkFrame(template_frame)
        dim_frame.pack(fill="x", pady=5)
        
        ctk.CTkLabel(dim_frame, text="Custom Size:").pack()
        dim_inner = ctk.CTkFrame(dim_frame)
        dim_inner.pack(fill="x", pady=2)
        
        self.width_entry = ctk.CTkEntry(dim_inner, placeholder_text="Width", width=60)
        self.width_entry.pack(side="left", padx=2)
        
        ctk.CTkLabel(dim_inner, text="×").pack(side="left", padx=2)
        
        self.height_entry = ctk.CTkEntry(dim_inner, placeholder_text="Height", width=60)
        self.height_entry.pack(side="left", padx=2)
        
        ctk.CTkButton(template_frame, text="Apply Custom Size", command=self.apply_custom_dimensions).pack(fill="x", pady=2)
        
        # Basic Operations
        basic_frame = ctk.CTkFrame(self.left_panel)
        basic_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(basic_frame, text="✂️ Basic Operations", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=5)
        
        ctk.CTkButton(basic_frame, text="Crop Selection", command=self.crop_image).pack(fill="x", pady=2)
        ctk.CTkButton(basic_frame, text="Reset Image", command=self.reset_image).pack(fill="x", pady=2)
        ctk.CTkButton(basic_frame, text="Undo", command=self.undo).pack(fill="x", pady=2)
        ctk.CTkButton(basic_frame, text="Redo", command=self.redo).pack(fill="x", pady=2)
        
        # Transform Operations
        transform_frame = ctk.CTkFrame(self.left_panel)
        transform_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(transform_frame, text="🔄 Transform", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=5)
        
        # Rotation
        rot_frame = ctk.CTkFrame(transform_frame)
        rot_frame.pack(fill="x", pady=5)
        
        ctk.CTkLabel(rot_frame, text="Rotation:").pack()
        self.rotation_slider = ctk.CTkSlider(rot_frame, from_=-180, to=180, command=self.rotate_image)
        self.rotation_slider.pack(fill="x", pady=2)
        self.rotation_slider.set(0)
        
        rot_buttons = ctk.CTkFrame(rot_frame)
        rot_buttons.pack(fill="x", pady=2)
        
        ctk.CTkButton(rot_buttons, text="↶ 90°", width=60, command=lambda: self.quick_rotate(-90)).pack(side="left", padx=2)
        ctk.CTkButton(rot_buttons, text="↷ 90°", width=60, command=lambda: self.quick_rotate(90)).pack(side="left", padx=2)
        
        # Flip operations
        flip_frame = ctk.CTkFrame(transform_frame)
        flip_frame.pack(fill="x", pady=5)
        
        ctk.CTkLabel(flip_frame, text="Flip:").pack()
        flip_buttons = ctk.CTkFrame(flip_frame)
        flip_buttons.pack(fill="x", pady=2)
        
        ctk.CTkButton(flip_buttons, text="↔ Horizontal", width=70, command=self.flip_horizontal).pack(side="left", padx=2)
        ctk.CTkButton(flip_buttons, text="↕ Vertical", width=70, command=self.flip_vertical).pack(side="left", padx=2)
        
    def setup_center_panel(self):
        """Setup center panel with image display and controls"""
        
        # Top toolbar
        toolbar = ctk.CTkFrame(self.center_panel, height=50)
        toolbar.pack(fill="x", padx=10, pady=(10, 5))
        toolbar.pack_propagate(False)
        
        # Zoom controls
        zoom_frame = ctk.CTkFrame(toolbar)
        zoom_frame.pack(side="left", padx=10, pady=10)
        
        ctk.CTkButton(zoom_frame, text="🔍+", width=40, command=self.zoom_in).pack(side="left", padx=2)
        ctk.CTkButton(zoom_frame, text="🔍-", width=40, command=self.zoom_out).pack(side="left", padx=2)
        ctk.CTkButton(zoom_frame, text="Fit", width=40, command=self.fit_to_window).pack(side="left", padx=2)
        
        self.zoom_label = ctk.CTkLabel(toolbar, text="100%")
        self.zoom_label.pack(side="left", padx=10)
        
        # Image info
        self.info_label = ctk.CTkLabel(toolbar, text="No image loaded")
        self.info_label.pack(side="right", padx=10)
        
        # Canvas container with scrollbars
        canvas_container = ctk.CTkFrame(self.center_panel)
        canvas_container.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        # Canvas for image display
        self.canvas = tk.Canvas(canvas_container, bg="#2b2b2b", highlightthickness=0)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(canvas_container, orient="vertical", command=self.canvas.yview)
        h_scrollbar = ttk.Scrollbar(canvas_container, orient="horizontal", command=self.canvas.xview)
        
        self.canvas.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Pack scrollbars and canvas
        v_scrollbar.pack(side="right", fill="y")
        h_scrollbar.pack(side="bottom", fill="x")
        self.canvas.pack(side="left", fill="both", expand=True)
        
    def setup_right_panel(self):
        """Setup right panel with image adjustments and filters"""
        
        # Image Adjustments
        adj_frame = ctk.CTkFrame(self.right_panel)
        adj_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(adj_frame, text="🎛️ Adjustments", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=5)
        
        # Brightness
        bright_frame = ctk.CTkFrame(adj_frame)
        bright_frame.pack(fill="x", pady=2)
        ctk.CTkLabel(bright_frame, text="Brightness:").pack()
        self.brightness_slider = ctk.CTkSlider(bright_frame, from_=0.1, to=3.0, command=self.adjust_brightness)
        self.brightness_slider.pack(fill="x", pady=2)
        self.brightness_slider.set(1.0)
        
        # Contrast
        contrast_frame = ctk.CTkFrame(adj_frame)
        contrast_frame.pack(fill="x", pady=2)
        ctk.CTkLabel(contrast_frame, text="Contrast:").pack()
        self.contrast_slider = ctk.CTkSlider(contrast_frame, from_=0.1, to=3.0, command=self.adjust_contrast)
        self.contrast_slider.pack(fill="x", pady=2)
        self.contrast_slider.set(1.0)
        
        # Saturation
        sat_frame = ctk.CTkFrame(adj_frame)
        sat_frame.pack(fill="x", pady=2)
        ctk.CTkLabel(sat_frame, text="Saturation:").pack()
        self.saturation_slider = ctk.CTkSlider(sat_frame, from_=0.0, to=3.0, command=self.adjust_saturation)
        self.saturation_slider.pack(fill="x", pady=2)
        self.saturation_slider.set(1.0)
        
        # Sharpness
        sharp_frame = ctk.CTkFrame(adj_frame)
        sharp_frame.pack(fill="x", pady=2)
        ctk.CTkLabel(sharp_frame, text="Sharpness:").pack()
        self.sharpness_slider = ctk.CTkSlider(sharp_frame, from_=0.1, to=3.0, command=self.adjust_sharpness)
        self.sharpness_slider.pack(fill="x", pady=2)
        self.sharpness_slider.set(1.0)
        
        # Reset adjustments
        ctk.CTkButton(adj_frame, text="Reset Adjustments", command=self.reset_adjustments).pack(fill="x", pady=5)
        
        # Filters
        filter_frame = ctk.CTkFrame(self.right_panel)
        filter_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(filter_frame, text="🎭 Filters", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=5)
        
        filter_buttons = [
            ("Blur", self.apply_blur),
            ("Sharpen", self.apply_sharpen),
            ("Edge Enhance", self.apply_edge_enhance),
            ("Emboss", self.apply_emboss),
            ("Smooth", self.apply_smooth),
            ("Find Edges", self.apply_find_edges)
        ]
        
        for text, command in filter_buttons:
            ctk.CTkButton(filter_frame, text=text, command=command).pack(fill="x", pady=1)
        
        # Advanced Features
        advanced_frame = ctk.CTkFrame(self.right_panel)
        advanced_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(advanced_frame, text="🔬 Advanced", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=5)
        
        advanced_buttons = [
            ("Auto Enhance", self.auto_enhance),
            ("Noise Reduction", self.noise_reduction),
            ("Histogram Eq", self.histogram_equalization),
            ("Color Balance", self.color_balance)
        ]
        
        for text, command in advanced_buttons:
            ctk.CTkButton(advanced_frame, text=text, command=command).pack(fill="x", pady=1)
        
        # Batch Operations
        batch_frame = ctk.CTkFrame(self.right_panel)
        batch_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(batch_frame, text="📦 Batch", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=5)
        
        ctk.CTkButton(batch_frame, text="Batch Crop", command=self.batch_crop).pack(fill="x", pady=1)
        ctk.CTkButton(batch_frame, text="Batch Resize", command=self.batch_resize).pack(fill="x", pady=1)
    
    def setup_canvas(self):
        """Setup canvas bindings for cropping"""
        self.canvas.bind("<Button-1>", self.start_crop)
        self.canvas.bind("<B1-Motion>", self.update_crop)
        self.canvas.bind("<ButtonRelease-1>", self.end_crop)
        self.canvas.bind("<MouseWheel>", self.on_mouse_wheel)
        self.canvas.bind("<Button-4>", self.on_mouse_wheel)
        self.canvas.bind("<Button-5>", self.on_mouse_wheel)
    
    def load_templates(self):
        """Load crop templates"""
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
    
    def load_presets(self):
        """Load application presets"""
        try:
            preset_file = "presets.json"
            if os.path.exists(preset_file):
                with open(preset_file, 'r') as f:
                    presets = json.load(f)
                    # Apply saved settings if any
                    print("✅ Presets loaded successfully")
        except Exception as e:
            print(f"⚠️  Could not load presets: {e}")
    
    def save_to_history(self):
        """Save current state to history for undo/redo"""
        if self.current_image:
            # Keep only last 20 states for memory efficiency
            if len(self.history) >= 20:
                self.history.pop(0)
                
            self.history = self.history[:self.history_index + 1]
            self.history.append(self.current_image.copy())
            self.history_index = len(self.history) - 1
    
    def open_image(self):
        """Open and load an image file"""
        if self.processing:
            return
            
        try:
            file_path = filedialog.askopenfilename(
                title="Select an image",
                filetypes=[
                    ("Image files", "*.jpg *.jpeg *.png *.bmp *.gif *.tiff *.webp"),
                    ("All files", "*.*")
                ]
            )
            
            if file_path:
                # Load image
                image = Image.open(file_path)
                
                # Convert to RGB if necessary
                if image.mode in ('RGBA', 'LA', 'P'):
                    image = image.convert('RGB')
                
                self.original_image = image
                self.current_image = image.copy()
                self.history = [image.copy()]
                self.history_index = 0
                
                # Reset adjustments
                self.reset_adjustments_silent()
                
                # Display image
                self.display_image()
                self.update_info_label()
                
                print(f"✅ Image loaded: {file_path}")
                print(f"   Size: {image.size}, Mode: {image.mode}")
                
        except Exception as e:
            messagebox.showerror("Error", f"Could not open image: {str(e)}")
            print(f"❌ Error opening image: {e}")
    
    def save_image(self):
        """Save the current image"""
        if not self.current_image:
            messagebox.showwarning("Warning", "No image to save")
            return
            
        if self.processing:
            return
            
        try:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".jpg",
                filetypes=[
                    ("JPEG files", "*.jpg"),
                    ("PNG files", "*.png"),
                    ("TIFF files", "*.tiff"),
                    ("BMP files", "*.bmp"),
                    ("WebP files", "*.webp")
                ]
            )
            
            if file_path:
                # Save with optimization
                save_kwargs = {"optimize": True}
                if file_path.lower().endswith(('.jpg', '.jpeg')):
                    save_kwargs["quality"] = 95
                    
                self.current_image.save(file_path, **save_kwargs)
                print(f"✅ Image saved: {file_path}")
                messagebox.showinfo("Success", f"Image saved successfully to {file_path}")
                
        except Exception as e:
            messagebox.showerror("Error", f"Could not save image: {str(e)}")
            print(f"❌ Error saving image: {e}")
    
    def export_image(self):
        """Export image with quality settings"""
        if not self.current_image:
            messagebox.showwarning("Warning", "No image to export")
            return
            
        if self.processing:
            return
            
        # Create export dialog
        export_window = ctk.CTkToplevel(self.root)
        export_window.title("Export Settings")
        export_window.geometry("400x300")
        export_window.transient(self.root)
        export_window.grab_set()
        
        # Format selection
        format_frame = ctk.CTkFrame(export_window)
        format_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(format_frame, text="Format:", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w")
        format_var = ctk.StringVar(value="JPEG")
        format_menu = ctk.CTkOptionMenu(format_frame, variable=format_var, 
                                       values=["JPEG", "PNG", "TIFF", "BMP", "WebP"])
        format_menu.pack(fill="x", pady=5)
        
        # Quality settings
        quality_frame = ctk.CTkFrame(export_window)
        quality_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(quality_frame, text="Quality (JPEG only):", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w")
        quality_var = ctk.IntVar(value=95)
        quality_slider = ctk.CTkSlider(quality_frame, from_=10, to=100, variable=quality_var)
        quality_slider.pack(fill="x", pady=5)
        quality_label = ctk.CTkLabel(quality_frame, text="95%")
        quality_label.pack()
        
        def update_quality_label(value):
            quality_label.configure(text=f"{int(float(value))}%")
        
        quality_slider.configure(command=update_quality_label)
        
        # Buttons
        button_frame = ctk.CTkFrame(export_window)
        button_frame.pack(fill="x", padx=20, pady=20)
        
        def do_export():
            try:
                file_path = filedialog.asksaveasfilename(
                    defaultextension=f".{format_var.get().lower()}",
                    filetypes=[(f"{format_var.get()} files", f"*.{format_var.get().lower()}")]
                )
                
                if file_path:
                    save_kwargs = {"optimize": True}
                    if format_var.get() == "JPEG":
                        save_kwargs["quality"] = quality_var.get()
                    
                    self.current_image.save(file_path, format=format_var.get(), **save_kwargs)
                    print(f"✅ Image exported: {file_path}")
                    messagebox.showinfo("Success", f"Image exported successfully!")
                    export_window.destroy()
                    
            except Exception as e:
                messagebox.showerror("Error", f"Export failed: {str(e)}")
        
        ctk.CTkButton(button_frame, text="Export", command=do_export).pack(side="left", padx=5)
        ctk.CTkButton(button_frame, text="Cancel", command=export_window.destroy).pack(side="right", padx=5)
    
    def display_image(self):
        """Display current image on canvas"""
        if not self.current_image:
            return
            
        try:
            # Calculate display size
            canvas_width = self.canvas.winfo_width()
            canvas_height = self.canvas.winfo_height()
            
            if canvas_width <= 1 or canvas_height <= 1:
                self.root.after(100, self.display_image)
                return
            
            img_width, img_height = self.current_image.size
            display_width = int(img_width * self.zoom_factor)
            display_height = int(img_height * self.zoom_factor)
            
            # Resize image for display
            if display_width > 0 and display_height > 0:
                self.displayed_image = self.current_image.resize(
                    (display_width, display_height), 
                    Image.Resampling.LANCZOS
                )
                self.tk_image = ImageTk.PhotoImage(self.displayed_image)
                
                # Clear canvas and display image
                self.canvas.delete("all")
                self.canvas.create_image(
                    display_width // 2, 
                    display_height // 2, 
                    anchor="center", 
                    image=self.tk_image
                )
                
                # Update scroll region
                self.canvas.configure(scrollregion=(0, 0, display_width, display_height))
                
                # Update zoom label
                zoom_percent = int(self.zoom_factor * 100)
                self.zoom_label.configure(text=f"{zoom_percent}%")
                
        except Exception as e:
            print(f"❌ Error displaying image: {e}")
    
    def update_info_label(self):
        """Update image information label"""
        if self.current_image:
            width, height = self.current_image.size
            mode = self.current_image.mode
            self.info_label.configure(text=f"{width}×{height} | {mode}")
        else:
            self.info_label.configure(text="No image loaded")
    
    # Zoom and navigation functions
    def zoom_in(self):
        """Zoom in on the image"""
        if self.current_image:
            self.zoom_factor = min(self.zoom_factor * 1.2, 10.0)
            self.display_image()
    
    def zoom_out(self):
        """Zoom out of the image"""
        if self.current_image:
            self.zoom_factor = max(self.zoom_factor / 1.2, 0.1)
            self.display_image()
    
    def fit_to_window(self):
        """Fit image to window size"""
        if not self.current_image:
            return
            
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        img_width, img_height = self.current_image.size
        
        if canvas_width > 0 and canvas_height > 0:
            zoom_x = canvas_width / img_width
            zoom_y = canvas_height / img_height
            self.zoom_factor = min(zoom_x, zoom_y) * 0.9  # Leave some margin
            self.display_image()
    
    def on_mouse_wheel(self, event):
        """Handle mouse wheel scrolling for zoom"""
        if event.delta > 0 or event.num == 4:
            self.zoom_in()
        else:
            self.zoom_out()
    
    # Crop functionality
    def start_crop(self, event):
        """Start crop selection"""
        if not self.current_image:
            return
            
        self.start_x = self.canvas.canvasx(event.x)
        self.start_y = self.canvas.canvasy(event.y)
        
        if self.rect:
            self.canvas.delete(self.rect)
    
    def update_crop(self, event):
        """Update crop selection"""
        if not self.current_image or not self.start_x:
            return
            
        cur_x = self.canvas.canvasx(event.x)
        cur_y = self.canvas.canvasy(event.y)
        
        if self.rect:
            self.canvas.delete(self.rect)
            
        self.rect = self.canvas.create_rectangle(
            self.start_x, self.start_y, cur_x, cur_y,
            outline="red", width=2
        )
    
    def end_crop(self, event):
        """End crop selection"""
        if not self.current_image or not self.start_x:
            return
            
        end_x = self.canvas.canvasx(event.x)
        end_y = self.canvas.canvasy(event.y)
        
        # Calculate crop coordinates
        img_width, img_height = self.current_image.size
        display_width = int(img_width * self.zoom_factor)
        display_height = int(img_height * self.zoom_factor)
        
        # Convert canvas coordinates to image coordinates
        x1 = max(0, min(self.start_x, end_x) / self.zoom_factor)
        y1 = max(0, min(self.start_y, end_y) / self.zoom_factor)
        x2 = min(img_width, max(self.start_x, end_x) / self.zoom_factor)
        y2 = min(img_height, max(self.start_y, end_y) / self.zoom_factor)
        
        if abs(x2 - x1) > 10 and abs(y2 - y1) > 10:  # Minimum selection size
            self.crop_coords = (int(x1), int(y1), int(x2), int(y2))
        
    def crop_image(self):
        """Crop the image based on selection"""
        if not self.current_image or not self.crop_coords:
            messagebox.showwarning("Warning", "Please make a selection first")
            return
            
        try:
            self.save_to_history()
            self.current_image = self.current_image.crop(self.crop_coords)
            self.display_image()
            self.update_info_label()
            self.crop_coords = None
            if self.rect:
                self.canvas.delete(self.rect)
                self.rect = None
            print("✅ Image cropped successfully")
            
        except Exception as e:
            messagebox.showerror("Error", f"Could not crop image: {str(e)}")
    
    def apply_template(self, template):
        """Apply a crop template"""
        if template == "Custom":
            return
            
        if template in self.templates:
            ratio_w, ratio_h = self.templates[template]
            
            # Update entry fields
            self.width_entry.delete(0, 'end')
            self.height_entry.delete(0, 'end')
            
            if self.current_image:
                img_w, img_h = self.current_image.size
                
                # Calculate dimensions maintaining aspect ratio
                if img_w / img_h > ratio_w / ratio_h:
                    # Image is wider, constrain by height
                    new_h = img_h
                    new_w = int(img_h * ratio_w / ratio_h)
                else:
                    # Image is taller, constrain by width
                    new_w = img_w
                    new_h = int(img_w * ratio_h / ratio_w)
                
                self.width_entry.insert(0, str(new_w))
                self.height_entry.insert(0, str(new_h))
                
                # Auto-apply template
                self.apply_custom_dimensions()
    
    def apply_custom_dimensions(self):
        """Apply custom crop dimensions"""
        try:
            width = int(self.width_entry.get())
            height = int(self.height_entry.get())
            
            if width > 0 and height > 0 and self.current_image:
                img_w, img_h = self.current_image.size
                
                # Center the crop
                x1 = max(0, (img_w - width) // 2)
                y1 = max(0, (img_h - height) // 2)
                x2 = min(img_w, x1 + width)
                y2 = min(img_h, y1 + height)
                
                self.crop_coords = (x1, y1, x2, y2)
                
                # Visualize crop area
                display_width = int(img_w * self.zoom_factor)
                display_height = int(img_h * self.zoom_factor)
                
                canvas_x1 = x1 * self.zoom_factor
                canvas_y1 = y1 * self.zoom_factor
                canvas_x2 = x2 * self.zoom_factor
                canvas_y2 = y2 * self.zoom_factor
                
                if self.rect:
                    self.canvas.delete(self.rect)
                
                self.rect = self.canvas.create_rectangle(
                    canvas_x1, canvas_y1, canvas_x2, canvas_y2,
                    outline="red", width=2
                )
                
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numeric dimensions")
    
    # Transform operations
    def rotate_image(self, angle):
        """Rotate image by specified angle"""
        if not self.current_image or self.processing:
            return
            
        try:
            angle_deg = float(angle)
            if abs(angle_deg - self.rotation_angle) > 0.5:  # Reduce sensitivity
                self.processing = True
                self.save_to_history()
                self.rotation_angle = angle_deg
                
                # Rotate image with expansion to prevent cropping
                rotated = self.current_image.rotate(-angle_deg, expand=True, fillcolor=(255, 255, 255))
                self.current_image = rotated
                self.display_image()
                self.update_info_label()
                self.processing = False
                
        except Exception as e:
            self.processing = False
            print(f"❌ Rotation error: {e}")
    
    def quick_rotate(self, angle):
        """Quick rotate by 90 degree increments"""
        if not self.current_image:
            return
            
        try:
            self.save_to_history()
            if angle == -90:
                self.current_image = self.current_image.rotate(90, expand=True)
            elif angle == 90:
                self.current_image = self.current_image.rotate(-90, expand=True)
            
            self.display_image()
            self.update_info_label()
            print(f"✅ Image rotated {angle}°")
            
        except Exception as e:
            messagebox.showerror("Error", f"Could not rotate image: {str(e)}")
    
    def flip_horizontal(self):
        """Flip image horizontally"""
        if not self.current_image:
            return
            
        try:
            self.save_to_history()
            self.current_image = self.current_image.transpose(Image.FLIP_LEFT_RIGHT)
            self.display_image()
            print("✅ Image flipped horizontally")
            
        except Exception as e:
            messagebox.showerror("Error", f"Could not flip image: {str(e)}")
    
    def flip_vertical(self):
        """Flip image vertically"""
        if not self.current_image:
            return
            
        try:
            self.save_to_history()
            self.current_image = self.current_image.transpose(Image.FLIP_TOP_BOTTOM)
            self.display_image()
            print("✅ Image flipped vertically")
            
        except Exception as e:
            messagebox.showerror("Error", f"Could not flip image: {str(e)}")
    
    # Image adjustment functions
    def adjust_brightness(self, value):
        """Adjust image brightness"""
        if not self.original_image or self.processing:
            return
        self.apply_all_adjustments()
    
    def adjust_contrast(self, value):
        """Adjust image contrast"""
        if not self.original_image or self.processing:
            return
        self.apply_all_adjustments()
    
    def adjust_saturation(self, value):
        """Adjust image saturation"""
        if not self.original_image or self.processing:
            return
        self.apply_all_adjustments()
    
    def adjust_sharpness(self, value):
        """Adjust image sharpness"""
        if not self.original_image or self.processing:
            return
        self.apply_all_adjustments()
    
    def apply_all_adjustments(self):
        """Apply all image adjustments"""
        if not self.original_image:
            return
            
        try:
            # Get current adjustment values
            brightness = self.brightness_slider.get()
            contrast = self.contrast_slider.get()
            saturation = self.saturation_slider.get()
            sharpness = self.sharpness_slider.get()
            
            # Apply adjustments
            img = self.original_image.copy()
            
            # Brightness
            if abs(brightness - 1.0) > 0.01:
                enhancer = ImageEnhance.Brightness(img)
                img = enhancer.enhance(brightness)
            
            # Contrast
            if abs(contrast - 1.0) > 0.01:
                enhancer = ImageEnhance.Contrast(img)
                img = enhancer.enhance(contrast)
            
            # Saturation
            if abs(saturation - 1.0) > 0.01:
                enhancer = ImageEnhance.Color(img)
                img = enhancer.enhance(saturation)
            
            # Sharpness
            if abs(sharpness - 1.0) > 0.01:
                enhancer = ImageEnhance.Sharpness(img)
                img = enhancer.enhance(sharpness)
            
            self.current_image = img
            self.display_image()
            
        except Exception as e:
            print(f"❌ Adjustment error: {e}")
    
    def reset_adjustments(self):
        """Reset all image adjustments"""
        self.brightness_slider.set(1.0)
        self.contrast_slider.set(1.0)
        self.saturation_slider.set(1.0)
        self.sharpness_slider.set(1.0)
        
        if self.original_image:
            self.current_image = self.original_image.copy()
            self.display_image()
        print("✅ Adjustments reset")
    
    def reset_adjustments_silent(self):
        """Reset adjustments without logging"""
        self.brightness_slider.set(1.0)
        self.contrast_slider.set(1.0)
        self.saturation_slider.set(1.0)
        self.sharpness_slider.set(1.0)
    
    # Filter functions
    def apply_blur(self):
        """Apply blur filter"""
        if not self.current_image:
            return
        try:
            self.save_to_history()
            self.current_image = self.current_image.filter(ImageFilter.BLUR)
            self.display_image()
            print("✅ Blur filter applied")
        except Exception as e:
            messagebox.showerror("Error", f"Could not apply blur: {str(e)}")
    
    def apply_sharpen(self):
        """Apply sharpen filter"""
        if not self.current_image:
            return
        try:
            self.save_to_history()
            self.current_image = self.current_image.filter(ImageFilter.SHARPEN)
            self.display_image()
            print("✅ Sharpen filter applied")
        except Exception as e:
            messagebox.showerror("Error", f"Could not apply sharpen: {str(e)}")
    
    def apply_edge_enhance(self):
        """Apply edge enhance filter"""
        if not self.current_image:
            return
        try:
            self.save_to_history()
            self.current_image = self.current_image.filter(ImageFilter.EDGE_ENHANCE)
            self.display_image()
            print("✅ Edge enhance filter applied")
        except Exception as e:
            messagebox.showerror("Error", f"Could not apply edge enhance: {str(e)}")
    
    def apply_emboss(self):
        """Apply emboss filter"""
        if not self.current_image:
            return
        try:
            self.save_to_history()
            self.current_image = self.current_image.filter(ImageFilter.EMBOSS)
            self.display_image()
            print("✅ Emboss filter applied")
        except Exception as e:
            messagebox.showerror("Error", f"Could not apply emboss: {str(e)}")
    
    def apply_smooth(self):
        """Apply smooth filter"""
        if not self.current_image:
            return
        try:
            self.save_to_history()
            self.current_image = self.current_image.filter(ImageFilter.SMOOTH)
            self.display_image()
            print("✅ Smooth filter applied")
        except Exception as e:
            messagebox.showerror("Error", f"Could not apply smooth: {str(e)}")
    
    def apply_find_edges(self):
        """Apply find edges filter"""
        if not self.current_image:
            return
        try:
            self.save_to_history()
            self.current_image = self.current_image.filter(ImageFilter.FIND_EDGES)
            self.display_image()
            print("✅ Find edges filter applied")
        except Exception as e:
            messagebox.showerror("Error", f"Could not apply find edges: {str(e)}")
    
    # Advanced processing functions
    def auto_enhance(self):
        """Apply automatic enhancement using CLAHE"""
        if not self.current_image:
            return
            
        try:
            self.save_to_history()
            
            # Convert PIL to OpenCV
            cv_image = cv2.cvtColor(np.array(self.current_image), cv2.COLOR_RGB2BGR)
            
            # Convert to LAB color space
            lab = cv2.cvtColor(cv_image, cv2.COLOR_BGR2LAB)
            l, a, b = cv2.split(lab)
            
            # Apply CLAHE to L channel
            clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
            l_enhanced = clahe.apply(l)
            
            # Merge channels
            enhanced_lab = cv2.merge([l_enhanced, a, b])
            enhanced_bgr = cv2.cvtColor(enhanced_lab, cv2.COLOR_LAB2BGR)
            enhanced_rgb = cv2.cvtColor(enhanced_bgr, cv2.COLOR_BGR2RGB)
            
            # Convert back to PIL
            self.current_image = Image.fromarray(enhanced_rgb)
            self.display_image()
            print("✅ Auto enhancement applied")
            
        except Exception as e:
            messagebox.showerror("Error", f"Could not apply auto enhancement: {str(e)}")
    
    def noise_reduction(self):
        """Apply noise reduction using Non-local Means Denoising"""
        if not self.current_image:
            return
            
        try:
            self.save_to_history()
            
            # Convert PIL to OpenCV
            cv_image = cv2.cvtColor(np.array(self.current_image), cv2.COLOR_RGB2BGR)
            
            # Apply denoising
            denoised = cv2.fastNlMeansDenoisingColored(cv_image, None, 10, 10, 7, 21)
            denoised_rgb = cv2.cvtColor(denoised, cv2.COLOR_BGR2RGB)
            
            # Convert back to PIL
            self.current_image = Image.fromarray(denoised_rgb)
            self.display_image()
            print("✅ Noise reduction applied")
            
        except Exception as e:
            messagebox.showerror("Error", f"Could not apply noise reduction: {str(e)}")
    
    def histogram_equalization(self):
        """Apply histogram equalization"""
        if not self.current_image:
            return
            
        try:
            self.save_to_history()
            
            # Convert PIL to OpenCV
            cv_image = cv2.cvtColor(np.array(self.current_image), cv2.COLOR_RGB2BGR)
            
            # Convert to YUV
            yuv = cv2.cvtColor(cv_image, cv2.COLOR_BGR2YUV)
            yuv[:,:,0] = cv2.equalizeHist(yuv[:,:,0])
            
            # Convert back to BGR then RGB
            equalized_bgr = cv2.cvtColor(yuv, cv2.COLOR_YUV2BGR)
            equalized_rgb = cv2.cvtColor(equalized_bgr, cv2.COLOR_BGR2RGB)
            
            # Convert back to PIL
            self.current_image = Image.fromarray(equalized_rgb)
            self.display_image()
            print("✅ Histogram equalization applied")
            
        except Exception as e:
            messagebox.showerror("Error", f"Could not apply histogram equalization: {str(e)}")
    
    def color_balance(self):
        """Apply automatic color balance using gray world assumption"""
        if not self.current_image:
            return
            
        try:
            self.save_to_history()
            
            # Convert PIL to numpy array
            img_array = np.array(self.current_image).astype(np.float32)
            
            # Calculate mean for each channel
            mean_r = np.mean(img_array[:,:,0])
            mean_g = np.mean(img_array[:,:,1])
            mean_b = np.mean(img_array[:,:,2])
            
            # Calculate gray world average
            gray_world = (mean_r + mean_g + mean_b) / 3
            
            # Calculate correction factors
            scale_r = gray_world / mean_r if mean_r > 0 else 1
            scale_g = gray_world / mean_g if mean_g > 0 else 1
            scale_b = gray_world / mean_b if mean_b > 0 else 1
            
            # Apply corrections
            img_array[:,:,0] *= scale_r
            img_array[:,:,1] *= scale_g
            img_array[:,:,2] *= scale_b
            
            # Clip values and convert back
            img_array = np.clip(img_array, 0, 255).astype(np.uint8)
            self.current_image = Image.fromarray(img_array)
            self.display_image()
            print("✅ Color balance applied")
            
        except Exception as e:
            messagebox.showerror("Error", f"Could not apply color balance: {str(e)}")
    
    # Batch processing functions
    def batch_crop(self):
        """Batch crop multiple images"""
        if not self.crop_coords:
            messagebox.showwarning("Warning", "Please set crop area first")
            return
            
        try:
            input_folder = filedialog.askdirectory(title="Select input folder")
            if not input_folder:
                return
                
            output_folder = filedialog.askdirectory(title="Select output folder")
            if not output_folder:
                return
            
            # Get image files
            image_extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp')
            image_files = [f for f in os.listdir(input_folder) 
                          if f.lower().endswith(image_extensions)]
            
            if not image_files:
                messagebox.showinfo("Info", "No image files found in selected folder")
                return
            
            # Process images
            processed = 0
            for filename in image_files:
                try:
                    input_path = os.path.join(input_folder, filename)
                    output_path = os.path.join(output_folder, f"cropped_{filename}")
                    
                    # Load and crop image
                    img = Image.open(input_path)
                    if img.mode in ('RGBA', 'LA', 'P'):
                        img = img.convert('RGB')
                    
                    cropped = img.crop(self.crop_coords)
                    cropped.save(output_path, optimize=True, quality=95)
                    processed += 1
                    
                except Exception as e:
                    print(f"Error processing {filename}: {e}")
                    continue
            
            messagebox.showinfo("Success", f"Batch crop completed! Processed {processed} images.")
            print(f"✅ Batch crop completed: {processed} images processed")
            
        except Exception as e:
            messagebox.showerror("Error", f"Batch crop failed: {str(e)}")
    
    def batch_resize(self):
        """Batch resize multiple images"""
        try:
            # Create resize dialog
            resize_window = ctk.CTkToplevel(self.root)
            resize_window.title("Batch Resize Settings")
            resize_window.geometry("400x250")
            resize_window.transient(self.root)
            resize_window.grab_set()
            
            # Size input
            size_frame = ctk.CTkFrame(resize_window)
            size_frame.pack(fill="x", padx=20, pady=10)
            
            ctk.CTkLabel(size_frame, text="New Size:", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w")
            
            size_input_frame = ctk.CTkFrame(size_frame)
            size_input_frame.pack(fill="x", pady=5)
            
            width_entry = ctk.CTkEntry(size_input_frame, placeholder_text="Width", width=80)
            width_entry.pack(side="left", padx=2)
            
            ctk.CTkLabel(size_input_frame, text="×").pack(side="left", padx=5)
            
            height_entry = ctk.CTkEntry(size_input_frame, placeholder_text="Height", width=80)
            height_entry.pack(side="left", padx=2)
            
            # Maintain aspect ratio option
            maintain_ratio = ctk.BooleanVar(value=True)
            ctk.CTkCheckBox(size_frame, text="Maintain aspect ratio", variable=maintain_ratio).pack(anchor="w", pady=5)
            
            def do_batch_resize():
                try:
                    new_width = int(width_entry.get())
                    new_height = int(height_entry.get())
                    
                    input_folder = filedialog.askdirectory(title="Select input folder")
                    if not input_folder:
                        return
                        
                    output_folder = filedialog.askdirectory(title="Select output folder")
                    if not output_folder:
                        return
                    
                    # Get image files
                    image_extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp')
                    image_files = [f for f in os.listdir(input_folder) 
                                  if f.lower().endswith(image_extensions)]
                    
                    processed = 0
                    for filename in image_files:
                        try:
                            input_path = os.path.join(input_folder, filename)
                            output_path = os.path.join(output_folder, f"resized_{filename}")
                            
                            img = Image.open(input_path)
                            if img.mode in ('RGBA', 'LA', 'P'):
                                img = img.convert('RGB')
                            
                            if maintain_ratio.get():
                                img.thumbnail((new_width, new_height), Image.Resampling.LANCZOS)
                            else:
                                img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                            
                            img.save(output_path, optimize=True, quality=95)
                            processed += 1
                            
                        except Exception as e:
                            print(f"Error processing {filename}: {e}")
                            continue
                    
                    messagebox.showinfo("Success", f"Batch resize completed! Processed {processed} images.")
                    resize_window.destroy()
                    
                except ValueError:
                    messagebox.showerror("Error", "Please enter valid numeric dimensions")
                except Exception as e:
                    messagebox.showerror("Error", f"Batch resize failed: {str(e)}")
            
            # Buttons
            button_frame = ctk.CTkFrame(resize_window)
            button_frame.pack(fill="x", padx=20, pady=20)
            
            ctk.CTkButton(button_frame, text="Resize", command=do_batch_resize).pack(side="left", padx=5)
            ctk.CTkButton(button_frame, text="Cancel", command=resize_window.destroy).pack(side="right", padx=5)
            
        except Exception as e:
            messagebox.showerror("Error", f"Could not open batch resize: {str(e)}")
    
    # History functions
    def undo(self):
        """Undo last operation"""
        if self.history_index > 0:
            self.history_index -= 1
            self.current_image = self.history[self.history_index].copy()
            self.display_image()
            self.update_info_label()
            print("✅ Undo successful")
        else:
            print("⚠️  Nothing to undo")
    
    def redo(self):
        """Redo last undone operation"""
        if self.history_index < len(self.history) - 1:
            self.history_index += 1
            self.current_image = self.history[self.history_index].copy()
            self.display_image()
            self.update_info_label()
            print("✅ Redo successful")
        else:
            print("⚠️  Nothing to redo")
    
    def reset_image(self):
        """Reset image to original state"""
        if self.original_image:
            self.current_image = self.original_image.copy()
            self.reset_adjustments()
            self.display_image()
            self.update_info_label()
            self.zoom_factor = 1.0
            self.rotation_angle = 0
            self.rotation_slider.set(0)
            print("✅ Image reset to original")
    
    def run(self):
        """Run the application"""
        try:
            # Load test image automatically for demo
            test_image_path = "/home/desmond/Pictures/Penguins Of Madagascar/Kowalski.png"
            if os.path.exists(test_image_path):
                self.root.after(1000, lambda: self.load_test_image(test_image_path))
            
            self.root.mainloop()
        except KeyboardInterrupt:
            print("\\n🛑 Application interrupted by user")
        except Exception as e:
            print(f"❌ Application error: {e}")
        finally:
            # Cleanup
            self.cleanup()
    
    def load_test_image(self, path):
        """Load test image for demonstration"""
        try:
            image = Image.open(path)
            if image.mode in ('RGBA', 'LA', 'P'):
                image = image.convert('RGB')
            
            self.original_image = image
            self.current_image = image.copy()
            self.history = [image.copy()]
            self.history_index = 0
            
            self.reset_adjustments_silent()
            self.display_image()
            self.update_info_label()
            self.fit_to_window()
            
            print(f"🐧 Kowalski test image loaded: {path}")
            
        except Exception as e:
            print(f"⚠️  Could not load test image: {e}")
    
    def cleanup(self):
        """Clean up resources"""
        try:
            # Force garbage collection
            gc.collect()
            print("🧹 Resources cleaned up")
        except Exception as e:
            print(f"⚠️  Cleanup error: {e}")


def main():
    """Main function to run the Enhanced Image Cropper"""
    try:
        app = EnhancedImageCropper()
        app.run()
    except Exception as e:
        print(f"❌ Failed to start application: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
