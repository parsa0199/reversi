import os

# get files name
def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext

# get thumbnails name
def upload_thumbnail_path(instance, filename):
    name, ext = get_filename_ext(filename)
    final_name = f"{instance.id}{ext}"
    return f"uploads/thumbnail/{final_name}"

# get images name
def upload_image_path(instance, filename):
    name, ext = get_filename_ext(filename)
    final_name = f"{instance.id}{ext}"
    return f"uploads/image/{final_name}"

# get videos name
def upload_video_path(instance, filename):
    name, ext = get_filename_ext(filename)
    final_name = f"{instance.id}{ext}"
    return f"uploads/video/{final_name}"