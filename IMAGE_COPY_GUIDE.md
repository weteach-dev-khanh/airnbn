# Image Copy Guide

## Manual Image Copy Instructions

Since the automatic copy commands didn't work as expected, here's how to manually copy images:

### Step 1: Copy Avatar Images
1. Navigate to: `c:\Users\Admin\Documents\Github\airnbn\nguyenvietanhnov-main\public\images\`
2. Copy `avatar.jpg` to: `c:\Users\Admin\Documents\Github\airnbn\core\static\core\images\`
3. Copy `avatar-2.png` to: `c:\Users\Admin\Documents\Github\airnbn\core\static\core\images\`

### Step 2: Copy Airbnb Property Images
1. Navigate to: `c:\Users\Admin\Documents\Github\airnbn\nguyenvietanhnov-main\public\images\airbnb\`
2. Copy ALL files (*.jpg) to: `c:\Users\Admin\Documents\Github\airnbn\core\static\core\images\airbnb\`

### Step 3: Copy Course Images
1. Navigate to: `c:\Users\Admin\Documents\Github\airnbn\nguyenvietanhnov-main\public\images\courses\`
2. Copy ALL files (*.jpg) to: `c:\Users\Admin\Documents\Github\airnbn\core\static\core\images\courses\`

### Step 4: Copy Blog Images (if any)
1. Navigate to: `c:\Users\Admin\Documents\Github\airnbn\nguyenvietanhnov-main\public\images\blog\`
2. Copy ALL files to: `c:\Users\Admin\Documents\Github\airnbn\core\static\core\images\blog\`

### Important Files to Copy:
- avatar.jpg (main profile image)
- avatar-2.png (about section image)
- danang-villa.jpg (Da Nang property)
- nhatrang-penthouse.jpg (Nha Trang property)
- dalat-villa.jpg (Da Lat property)
- All course images for the courses section

## Alternative: Use File Explorer
1. Open two File Explorer windows
2. Source: `c:\Users\Admin\Documents\Github\airnbn\nguyenvietanhnov-main\public\images\`
3. Destination: `c:\Users\Admin\Documents\Github\airnbn\core\static\core\images\`
4. Drag and drop files/folders

## After Copying Images:
1. Run `python manage.py collectstatic` to update static files
2. Refresh the Django website to see images
3. Update template files to remove `.placeholder` extensions if needed
