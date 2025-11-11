# Setting Up the App Icon

To use your custom icon image for "AIFF Me Please":

1. **Place your image file** in one of these locations:
   - `resources/icon.png` (recommended)
   - `resources/icon.jpg` or `resources/icon.jpeg`
   - `icon.png` (in the project root)

2. **Supported formats:**
   - PNG (recommended)
   - JPG/JPEG
   - ICNS (macOS icon format)

3. **Image requirements:**
   - Any size (will be automatically resized)
   - Square aspect ratio works best
   - High resolution recommended (512x512 or larger)

4. **For macOS .app bundle:**
   - The icon will appear in the Dock and Finder when the app is built
   - For a proper .app bundle, you may need to convert to .icns format

The app will automatically load the icon on startup if it's found in one of the locations above.


