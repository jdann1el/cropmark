# Supplied photographs and cutouts

For supplied subjects whose identity or exact appearance the brief requires, use the real subject as source pixels: preserve identity, proportions, product marks, printed copy and colour. Generating a similar person or product is a recreation, not a faithful extraction. Retain the unmodified source and identify masks and operations in the editable package. For a redesign of an illustrative reference graphic, use `upgrade.md` to determine permitted reconstruction before applying this identity-preserving extraction route.

## Choose the route
- Existing RGBA with a good mask: preserve alpha by default; inspect its edges before altering it.
- Opaque photo: first try composition with the intact photograph. For a cutout, use a subject mask from an available segmentation tool or a manually editable mask. Inspect holes, logos, white detail, hair and reflections.
- Flat-background generated graphic: `cm.key_out` removes matching background connected to the border. It preserves enclosed matching details, but cannot separate matching subject colours connected to the background. This is a colour key, not semantic segmentation.
- Hair, glass, chrome, liquid or smoke: retain the photo or use a verified material/subject mask. Do not regenerate a real subject merely to avoid difficult edges. Generated conceptual assets can be composed directly on their intended background.

`cm.clean_cutout` preserves pixels/alpha by default. Erosion, feather, key and despill are explicit tools: use only after identifying the corresponding defect. Despill is for demonstrated colour spill, not for naturally green subjects. An edge operation can erase fine alpha or printed identity; compare against the source after each operation.

## Inspect the result
Open the cutout at full resolution on light and dark backgrounds, then inspect the final at feed size. Check silhouette, interior holes, fringe, pale residue, missing logo strokes, altered colour, translucent detail and contact/shadow consistency. Preserve the full useful subject unless the brief permits cropping.

Store source, mask and processed layer separately. If the available assets/tools cannot support a faithful cutout, choose a composition retaining the photo and state the limitation. Synthetic tests or an attractive final do not establish universal photo-cutout accuracy.
