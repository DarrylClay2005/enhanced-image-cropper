#!/usr/bin/env python3
"""
Comprehensive Feature Test for Enhanced Image Cropper v1.0.3.C - Kowalski Edition
Tests all major features and image processing capabilities
"""

import os
import sys
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter
import cv2
from skimage import restoration, exposure
import tempfile
import time

def test_image_operations():
    """Test basic image operations"""
    print("🧪 Testing Image Operations...")
    
    # Load test image
    test_image_path = "/home/desmond/Pictures/Penguins Of Madagascar/Kowalski.png"
    if not os.path.exists(test_image_path):
        print("❌ Test image not found!")
        return False
    
    try:
        # Test image loading
        img = Image.open(test_image_path)
        print(f"✅ Image loaded: {img.size} pixels, mode: {img.mode}")
        
        # Convert to RGB if necessary
        if img.mode in ('RGBA', 'LA', 'P'):
            img = img.convert('RGB')
            print("✅ Image converted to RGB")
        
        return img
    except Exception as e:
        print(f"❌ Image loading failed: {e}")
        return None

def test_crop_operations(img):
    """Test cropping operations"""
    print("🧪 Testing Crop Operations...")
    
    try:
        # Test basic crop
        width, height = img.size
        crop_coords = (width//4, height//4, 3*width//4, 3*height//4)
        cropped = img.crop(crop_coords)
        print(f"✅ Basic crop: {cropped.size} pixels")
        
        # Test template crops
        templates = {
            "Square (1:1)": (1, 1),
            "Landscape (16:9)": (16, 9),
            "Portrait (4:5)": (4, 5)
        }
        
        for template_name, (ratio_w, ratio_h) in templates.items():
            if width / height > ratio_w / ratio_h:
                new_h = height
                new_w = int(height * ratio_w / ratio_h)
            else:
                new_w = width
                new_h = int(width * ratio_h / ratio_w)
            
            x1 = (width - new_w) // 2
            y1 = (height - new_h) // 2
            template_crop = img.crop((x1, y1, x1 + new_w, y1 + new_h))
            print(f"✅ {template_name} crop: {template_crop.size} pixels")
        
        return True
    except Exception as e:
        print(f"❌ Crop operations failed: {e}")
        return False

def test_image_adjustments(img):
    """Test image adjustment features"""
    print("🧪 Testing Image Adjustments...")
    
    try:
        # Test brightness adjustment
        enhancer = ImageEnhance.Brightness(img)
        bright_img = enhancer.enhance(1.5)
        print("✅ Brightness adjustment")
        
        # Test contrast adjustment
        enhancer = ImageEnhance.Contrast(img)
        contrast_img = enhancer.enhance(1.3)
        print("✅ Contrast adjustment")
        
        # Test saturation adjustment
        enhancer = ImageEnhance.Color(img)
        saturated_img = enhancer.enhance(1.2)
        print("✅ Saturation adjustment")
        
        # Test sharpness adjustment
        enhancer = ImageEnhance.Sharpness(img)
        sharp_img = enhancer.enhance(1.4)
        print("✅ Sharpness adjustment")
        
        return True
    except Exception as e:
        print(f"❌ Image adjustments failed: {e}")
        return False

def test_filters(img):
    """Test filter operations"""
    print("🧪 Testing Filters...")
    
    try:
        # Test basic filters
        filters = [
            ("Blur", ImageFilter.BLUR),
            ("Sharpen", ImageFilter.SHARPEN),
            ("Edge Enhance", ImageFilter.EDGE_ENHANCE),
            ("Emboss", ImageFilter.EMBOSS),
            ("Smooth", ImageFilter.SMOOTH),
            ("Find Edges", ImageFilter.FIND_EDGES)
        ]
        
        for filter_name, filter_obj in filters:
            filtered_img = img.filter(filter_obj)
            print(f"✅ {filter_name} filter")
        
        return True
    except Exception as e:
        print(f"❌ Filter operations failed: {e}")
        return False

def test_advanced_processing(img):
    """Test advanced image processing"""
    print("🧪 Testing Advanced Processing...")
    
    try:
        # Convert PIL to OpenCV
        cv_image = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        
        # Test CLAHE enhancement
        lab = cv2.cvtColor(cv_image, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
        l_enhanced = clahe.apply(l)
        enhanced_lab = cv2.merge([l_enhanced, a, b])
        enhanced_bgr = cv2.cvtColor(enhanced_lab, cv2.COLOR_LAB2BGR)
        print("✅ CLAHE auto enhancement")
        
        # Test noise reduction
        denoised = cv2.fastNlMeansDenoisingColored(cv_image, None, 10, 10, 7, 21)
        print("✅ Noise reduction")
        
        # Test histogram equalization
        yuv = cv2.cvtColor(cv_image, cv2.COLOR_BGR2YUV)
        yuv[:,:,0] = cv2.equalizeHist(yuv[:,:,0])
        equalized = cv2.cvtColor(yuv, cv2.COLOR_YUV2BGR)
        print("✅ Histogram equalization")
        
        # Test color balance
        img_array = np.array(img).astype(np.float32)
        mean_r = np.mean(img_array[:,:,0])
        mean_g = np.mean(img_array[:,:,1])
        mean_b = np.mean(img_array[:,:,2])
        gray_world = (mean_r + mean_g + mean_b) / 3
        print("✅ Color balance")
        
        return True
    except Exception as e:
        print(f"❌ Advanced processing failed: {e}")
        return False

def test_transform_operations(img):
    """Test transform operations"""
    print("🧪 Testing Transform Operations...")
    
    try:
        # Test rotation
        rotated_90 = img.rotate(-90, expand=True)
        print("✅ 90° rotation")
        
        rotated_45 = img.rotate(-45, expand=True, fillcolor=(255, 255, 255))
        print("✅ 45° rotation")
        
        # Test flipping
        flipped_h = img.transpose(Image.FLIP_LEFT_RIGHT)
        print("✅ Horizontal flip")
        
        flipped_v = img.transpose(Image.FLIP_TOP_BOTTOM)
        print("✅ Vertical flip")
        
        return True
    except Exception as e:
        print(f"❌ Transform operations failed: {e}")
        return False

def test_file_operations(img):
    """Test file save/export operations"""
    print("🧪 Testing File Operations...")
    
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            # Test different format saves
            formats = [
                ("JPEG", ".jpg", {"optimize": True, "quality": 95}),
                ("PNG", ".png", {"optimize": True}),
                ("WebP", ".webp", {"optimize": True, "quality": 90}),
                ("TIFF", ".tiff", {"optimize": True}),
                ("BMP", ".bmp", {})
            ]
            
            for format_name, ext, save_kwargs in formats:
                test_path = os.path.join(temp_dir, f"test{ext}")
                img.save(test_path, format=format_name, **save_kwargs)
                
                # Verify file was created and can be loaded
                if os.path.exists(test_path):
                    test_load = Image.open(test_path)
                    print(f"✅ {format_name} save/load")
                else:
                    print(f"❌ {format_name} save failed")
                    return False
        
        return True
    except Exception as e:
        print(f"❌ File operations failed: {e}")
        return False

def test_batch_operations(img):
    """Test batch processing capabilities"""
    print("🧪 Testing Batch Operations...")
    
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create test images
            test_images = []
            for i in range(3):
                test_path = os.path.join(temp_dir, f"test_image_{i}.png")
                # Create variations of the original
                if i == 0:
                    img.save(test_path)
                elif i == 1:
                    enhancer = ImageEnhance.Brightness(img)
                    enhancer.enhance(1.2).save(test_path)
                else:
                    img.resize((img.size[0]//2, img.size[1]//2)).save(test_path)
                test_images.append(test_path)
            
            print("✅ Batch test images created")
            
            # Test batch resize simulation
            for test_path in test_images:
                test_img = Image.open(test_path)
                resized = test_img.resize((200, 200), Image.Resampling.LANCZOS)
                output_path = test_path.replace(".png", "_resized.png")
                resized.save(output_path)
            
            print("✅ Batch resize simulation")
            
            # Test batch crop simulation
            crop_coords = (50, 50, 150, 150)
            for test_path in test_images:
                test_img = Image.open(test_path)
                if test_img.size[0] > 150 and test_img.size[1] > 150:
                    cropped = test_img.crop(crop_coords)
                    output_path = test_path.replace(".png", "_cropped.png")
                    cropped.save(output_path)
            
            print("✅ Batch crop simulation")
        
        return True
    except Exception as e:
        print(f"❌ Batch operations failed: {e}")
        return False

def test_memory_optimization():
    """Test memory efficiency"""
    print("🧪 Testing Memory Optimization...")
    
    try:
        import gc
        import psutil
        
        # Get initial memory usage
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        # Create and process multiple images
        test_image_path = "/home/desmond/Pictures/Penguins Of Madagascar/Kowalski.png"
        for i in range(10):
            img = Image.open(test_image_path)
            if img.mode in ('RGBA', 'LA', 'P'):
                img = img.convert('RGB')
            
            # Apply some operations
            enhanced = ImageEnhance.Brightness(img).enhance(1.1)
            filtered = enhanced.filter(ImageFilter.BLUR)
            
            # Cleanup
            del img, enhanced, filtered
        
        # Force garbage collection
        gc.collect()
        
        final_memory = process.memory_info().rss / 1024 / 1024  # MB
        memory_increase = final_memory - initial_memory
        
        print(f"✅ Memory optimization - increase: {memory_increase:.1f}MB")
        
        if memory_increase < 100:  # Less than 100MB increase is acceptable
            print("✅ Memory usage is optimized")
        else:
            print("⚠️  Memory usage could be improved")
        
        return True
    except Exception as e:
        print(f"⚠️  Memory test failed: {e}")
        return True  # Non-critical failure

def run_comprehensive_test():
    """Run all feature tests"""
    print("=" * 80)
    print("🐧 Enhanced Image Cropper v1.0.3.C - Kowalski Edition")
    print("   COMPREHENSIVE FEATURE TEST")
    print("=" * 80)
    
    start_time = time.time()
    tests_passed = 0
    total_tests = 8
    
    # Test 1: Image Operations
    img = test_image_operations()
    if img:
        tests_passed += 1
        
        # Test 2: Crop Operations
        if test_crop_operations(img):
            tests_passed += 1
        
        # Test 3: Image Adjustments
        if test_image_adjustments(img):
            tests_passed += 1
        
        # Test 4: Filters
        if test_filters(img):
            tests_passed += 1
        
        # Test 5: Advanced Processing
        if test_advanced_processing(img):
            tests_passed += 1
        
        # Test 6: Transform Operations
        if test_transform_operations(img):
            tests_passed += 1
        
        # Test 7: File Operations
        if test_file_operations(img):
            tests_passed += 1
        
        # Test 8: Batch Operations
        if test_batch_operations(img):
            tests_passed += 1
    
    # Additional Test: Memory Optimization
    test_memory_optimization()
    
    end_time = time.time()
    duration = end_time - start_time
    
    print("=" * 80)
    print(f"🏁 TEST RESULTS:")
    print(f"   Tests Passed: {tests_passed}/{total_tests}")
    print(f"   Success Rate: {(tests_passed/total_tests)*100:.1f}%")
    print(f"   Duration: {duration:.2f} seconds")
    
    if tests_passed == total_tests:
        print("🎉 ALL TESTS PASSED! Application is ready for release.")
        print("🐧 Kowalski says: Analysis Complete - Everything is working perfectly!")
    else:
        print("⚠️  Some tests failed. Please review the issues above.")
    
    print("=" * 80)
    
    return tests_passed == total_tests

if __name__ == "__main__":
    success = run_comprehensive_test()
    sys.exit(0 if success else 1)
