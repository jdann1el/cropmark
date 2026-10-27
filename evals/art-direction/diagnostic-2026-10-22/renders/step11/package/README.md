# Paso 11 portable reproduction package

Self-contained inputs and Pillow composition scripts for the Paso 11 thumbnail, flyer, and three carousel slides. Python dependencies: Pillow, NumPy, and OpenCV (cv2). Run from this directory or any working directory:

```sh
python3 thumbnail/render.py
python3 flyer/render.py
python3 carousel/render.py
```

Each script writes its final artwork and editable text metadata beside itself. The candidate compositions use bundled inputs and fonts only. The `baseline/` directory retains direct baseline source rasters and their normalized comparison rasters; `baseline/thumbnail-A.*` and `baseline/flyer-A.*` retain the reused direct controls.

Fonts are redistributed under SIL Open Font License 1.1; the corresponding license texts are in `fonts/licenses/`. Source photographs/raster assets are included as static composition inputs. No reference-cache or Behance material is included.
