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
- 1080 x 1920 canvas metadata

Uploaded media, colors, and wording are supported by the current APK. Canvas movement and custom layers are exported as design metadata but are not applied by the APK yet. **Hide original machine media** makes empty welcome product and promotion slots blank instead of retaining Huaxin or server media.

## Validate a package

The validator uses only the Python standard library:

```sh
python3 validate_theme.py path/to/theme.ice-theme
```

Package limits are 100 MB expanded, 80 MB per file, and 64 entries.
