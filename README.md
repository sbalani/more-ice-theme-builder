# More Ice Theme Builder

Browser-based editor for creating `.ice-theme` packages for the More Ice application.

## Use

Open `index.html` directly or serve this directory with any static web server:

```sh
python3 -m http.server 8765
```

The editor runs entirely in the browser. It does not upload theme data or require a backend.

## Softlife integration

Host `index.html`, `app.js`, and `styles.css` together at any route in the Softlife platform. All asset paths are relative, and there is no build step or runtime dependency.

The exported file is a ZIP-compatible `.ice-theme` package containing:

- `manifest.json`
- Uploaded images or MP4 promotion media under `images/`
- New-theme resource colors and wording
- Fixed-slot media, colors, and wording

The preview uses the APK's fixed New-theme slots. Uploaded media, colors, and wording are applied to those same slots; empty media slots retain the machine's existing artwork. Free-position layers are intentionally not offered because the APK does not support them.

The welcome product slot can use the machine's main product, live product position 1-7, or an uploaded custom image. A custom upload wins and may be a product shot, logo, or other artwork.

## Validate a package

The validator uses only the Python standard library:

```sh
python3 validate_theme.py path/to/theme.ice-theme
```

Package limits are 100 MB expanded, 80 MB per file, and 64 entries.
