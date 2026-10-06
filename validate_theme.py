#!/usr/bin/env python3
"""Validate a More Ice .ice-theme package without external dependencies."""

import json
import re
import sys
import zipfile
from pathlib import PurePosixPath

MAX_PACKAGE = 100 * 1024 * 1024
MAX_FILE = 80 * 1024 * 1024
MAX_ENTRIES = 64
ID = re.compile(r"^[a-z0-9][a-z0-9._-]{1,63}$")
COLOR = re.compile(r"^#[0-9a-fA-F]{6}([0-9a-fA-F]{2})?$")
KEY = re.compile(r"^[a-z0-9_]{1,80}$")


def validate(path):
    if path.stat().st_size > MAX_PACKAGE:
        raise ValueError("package exceeds 100 MB")
    with zipfile.ZipFile(path) as package:
        entries = package.infolist()
        if len(entries) > MAX_ENTRIES:
            raise ValueError("package has too many files")
        names = set()
        total = 0
        for entry in entries:
            name = PurePosixPath(entry.filename)
            if name.is_absolute() or ".." in name.parts:
                raise ValueError(f"unsafe path: {entry.filename}")
            if entry.file_size > MAX_FILE:
                raise ValueError(f"file exceeds 80 MB: {entry.filename}")
            total += entry.file_size
            if total > MAX_PACKAGE:
                raise ValueError("expanded package exceeds 100 MB")
            names.add(entry.filename)
        manifest = json.loads(package.read("manifest.json"))
        if manifest.get("formatVersion") != 1:
            raise ValueError("unsupported formatVersion")
        if manifest.get("template") != "new":
            raise ValueError("unsupported template")
        if not ID.fullmatch(manifest.get("id", "")):
            raise ValueError("invalid theme id")
        if not 1 <= len(manifest.get("name", "")) <= 80:
            raise ValueError("invalid theme name")
        if not isinstance(manifest.get("version"), int) or manifest["version"] < 1:
            raise ValueError("invalid version")
        position = manifest.get("welcomeProductPosition", 0)
        if not isinstance(position, int) or not 0 <= position <= 7:
            raise ValueError("invalid welcome product position")
        for key, asset in manifest.get("assets", {}).items():
            if asset not in names:
                raise ValueError(f"missing asset {key}: {asset}")
        resources = manifest.get("resources")
        if not isinstance(resources, dict) or not resources:
            raise ValueError("theme has no screen resources")
        for key, value in resources.items():
            if key.startswith("color_new_"):
                if not isinstance(value, str) or not COLOR.fullmatch(value):
                    raise ValueError(f"invalid color {key}")
            elif key.startswith("ui_new_"):
                if value not in names:
                    raise ValueError(f"missing image {key}: {value}")
            else:
                raise ValueError(f"unknown resource: {key}")
        for key, value in manifest.get("labels", {}).items():
            if not KEY.fullmatch(key) or not isinstance(value, str) or len(value) > 120:
                raise ValueError(f"invalid wording: {key}")
        for screen, layers in manifest.get("layout", {}).items():
            if not KEY.fullmatch(screen) or not isinstance(layers, dict):
                raise ValueError(f"invalid layout screen: {screen}")
            for layer, geometry in layers.items():
                if not KEY.fullmatch(layer) or not isinstance(geometry, dict):
                    raise ValueError(f"invalid layout layer: {layer}")
                x, y = geometry.get("x"), geometry.get("y")
                width, height = geometry.get("width"), geometry.get("height")
                if not all(isinstance(value, (int, float)) for value in (x, y, width, height)):
                    raise ValueError(f"invalid geometry: {screen}.{layer}")
                if x < 0 or y < 0 or width < 20 or height < 20 or x + width > 1080 or y + height > 1920:
                    raise ValueError(f"layout outside canvas: {screen}.{layer}")
                if not isinstance(geometry.get("visible"), bool):
                    raise ValueError(f"invalid visibility: {screen}.{layer}")
    return manifest


if __name__ == "__main__":
    from pathlib import Path

    if len(sys.argv) != 2:
        raise SystemExit("usage: validate_theme.py THEME.ice-theme")
    result = validate(Path(sys.argv[1]))
    print(f"valid: {result['name']} ({result['id']} v{result['version']})")
