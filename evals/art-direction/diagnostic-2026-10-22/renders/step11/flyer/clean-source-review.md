# T7 — clean sleeve source review

The Paso 9 B blank sleeve is nearly frontal: its measured top and bottom angles are about 1.1° and 0.2°, with opposite signs, and its keystone is about 2.4%. It fails the frozen angle and keystone checks.

Ordinal 5 produced a warm photorealistic scene with a blank sleeve and visible record/tonearm. Its sleeve horizontal edges initially had opposite slope signs. Ordinal 6 was logged as R1 and attempted a specific correction; the R1 result still had opposing top/bottom slopes. Both images are preserved at `flyer/rounds/R0/` and `flyer/rounds/R1/`.

R2 applies one homography to the entire R1 photograph, then a uniform Lanczos fit. The first two parameter previews were rejected and preserved. The selected R2 v2 clean source in `flyer/clean-source.png` was inspected at 100%; it preserves a continuous room/table/turntable photograph, all sleeve corners, and recognizable grooves, platter and tonearm. A further uniform 1.15x crop is approved as `flyer/clean-source-crop.png`; it enlarges the sleeve face while keeping all corners inside the canvas and the record details recognizable. No sleeve-only geometry or lettering was edited.

The builder-fitted sleeve corners after both transforms are recorded in `plane-plan.json` and `plane-annotations.png`. The top and bottom angles are both above 5° with the same down-right slope; side-length keystone is above 4%. T7 is PASS at builder level; T15 must fit these edges independently. Image generation is 6/6; correction rounds used: R1 and R2.
