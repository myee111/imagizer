# Image Size Validation Guide

## Overview

The application automatically validates and optimizes images before sending them to the API. This prevents errors, saves costs, and ensures reliable operation.

## Automatic Validation

All images are checked for:

✅ **File Size** - Maximum 5MB
✅ **Dimensions** - Maximum 8000x8000 pixels
✅ **Encoded Size** - Validates after base64 encoding

## What Happens Automatically

### 1. Dimension Check
If your image exceeds 8000 pixels on either side:
- ✅ Image is **automatically resized** to fit within limits
- ✅ Aspect ratio is **maintained**
- ✅ High-quality resampling is used
- ℹ️  You'll see a message: "Image dimensions exceed maximum, resizing..."

**Example:**
```
⚠️  Image dimensions (10000x5000) exceed maximum (8000px)
   Resizing to fit within 8000px...
   New dimensions: 8000x4000
```

### 2. File Size Check
If your image exceeds 5MB:
- ✅ For HEIC/JPEG: **Automatically reduces quality** from 95 to 85
- ✅ Tries to compress within limits
- ❌ If still too large: **Clear error message** with suggestions

**Example:**
```
⚠️  Encoded image too large (6.2MB), reducing quality...
   Compressed to 4.8MB
```

### 3. Format Optimization
- HEIC/HEIF images are converted to JPEG
- Large PNGs may be resized
- Quality is optimized for API transmission

## Error Messages

### "Image file is too large"
```
Image file is too large: 8.5MB (max: 5.0MB)
Suggestions:
  - Compress the image before uploading
  - Resize to smaller dimensions
  - Convert to JPEG with lower quality
  - Use an image editing tool
```

**Quick Fix:**
```bash
# Using ImageMagick
convert large_image.jpg -resize 50% -quality 85 smaller_image.jpg

# Using Python/PIL
from PIL import Image
img = Image.open('large_image.jpg')
img.thumbnail((4000, 4000))
img.save('smaller_image.jpg', quality=85)
```

### "Image dimensions exceed maximum"
This is handled automatically! The image will be resized for you.

## Configuration

You can customize limits when calling the function directly:

```python
from claude_client import load_and_encode_image

# Custom limits
data, mime = load_and_encode_image(
    'myimage.jpg',
    max_size_mb=10.0,      # Allow up to 10MB
    max_dimension=5000      # Max 5000x5000 pixels
)
```

**Default Limits:**
- `max_size_mb`: 5.0 MB
- `max_dimension`: 8000 pixels

## Best Practices

### ✅ Recommended Image Specs

| Use Case | Recommended Size | Max Dimensions | Format |
|----------|-----------------|----------------|--------|
| General photos | < 2MB | 2000x2000 | JPEG, PNG |
| High detail images | < 4MB | 4000x4000 | JPEG |
| Screenshots | < 1MB | 1920x1080 | PNG, JPEG |
| Documents/OCR | < 2MB | 3000x3000 | JPEG, PNG |

### ✅ Tips for Best Results

1. **Use appropriate resolution**
   - Don't send 20MP photos when 2MP will work
   - Match resolution to your use case

2. **Choose the right format**
   - JPEG for photos (smaller file size)
   - PNG for screenshots with text
   - Let HEIC convert automatically

3. **Pre-compress if needed**
   - Use 85-90% quality for JPEG
   - Many image editors can batch compress

4. **Test with your images**
   - Run `./run.sh` → option 1 to test
   - Check console for any resize warnings

## Examples

### Example 1: Normal Usage (No Changes Needed)
```python
from claude_client import load_and_encode_image

# This works automatically
data, mime = load_and_encode_image('photo.jpg')
# ✅ Photo is 1.2MB, dimensions 2400x1800 - no changes needed
```

### Example 2: Large Image (Auto-Resized)
```python
data, mime = load_and_encode_image('huge_photo.jpg')
# ⚠️  Image dimensions (12000x8000) exceed maximum (8000px)
#    Resizing to fit within 8000px...
#    New dimensions: 8000x5333
# ✅ Image auto-resized and ready to use
```

### Example 3: Oversized File (Error with Guidance)
```python
try:
    data, mime = load_and_encode_image('massive.jpg')
except ValueError as e:
    print(e)
    # Shows clear instructions on how to fix
```

## Troubleshooting

### "Image still too large after compression"

**Problem:** Even after auto-compression, image exceeds limits

**Solutions:**
1. Manually resize the image first:
   ```bash
   convert input.jpg -resize 2000x2000 -quality 85 output.jpg
   ```

2. Use a different image
3. Crop to the relevant area
4. Convert to JPEG if it's a PNG

### "Decompression bomb warning"

This is a PIL safety warning for extremely large images (100+ megapixels). The validation will resize these automatically.

### Image quality degradation

If you notice quality loss:
- The image exceeded size limits and was auto-compressed
- Pre-compress your image manually for better control
- Use higher quality source images

## Technical Details

### Size Calculation
```
Original File → Load into Memory → Resize if needed →
Compress if needed → Base64 Encode → Validate final size
```

### Why These Limits?

**5MB File Limit:**
- Claude API maximum is ~5MB for images
- Leaves headroom for base64 encoding overhead (~33%)
- Prevents timeout errors
- Keeps costs reasonable

**8000px Dimension Limit:**
- Balances quality vs. file size
- Handles 4K+ images comfortably
- Prevents memory issues
- Matches typical API limits

### Encoding Overhead

Base64 encoding increases size by ~33%:
- 3MB image → ~4MB base64
- 5MB image → ~6.6MB base64 (may exceed API limits)

The validation accounts for this automatically.

## Monitoring

When images are processed, you'll see:

**No warnings** = Image is within limits ✅
```
[Claude Client] Using Vertex AI Claude...
```

**Auto-resize** = Dimensions too large ⚠️
```
⚠️  Image dimensions (10000x8000) exceed maximum (8000px)
   Resizing to fit within 8000px...
   New dimensions: 8000x6400
```

**Auto-compress** = File too large ⚠️
```
⚠️  Encoded image too large (6.2MB), reducing quality...
   Compressed to 4.8MB
```

## Summary

✅ **Automatic validation and optimization**
✅ **Clear error messages with solutions**
✅ **Maintains image quality where possible**
✅ **Prevents API errors before they happen**
✅ **Configurable limits for advanced users**

Your images are automatically optimized for the best experience!
