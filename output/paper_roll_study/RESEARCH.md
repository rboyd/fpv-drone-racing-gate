# Paper-roll gate: joinery research and experiment plan

Baseline committed as `732f592`. This is a separate experimental iteration, not a replacement production kit.

## Sources checked 2026-09-17

- [Kato: Unitrack system](https://www.unitrack-kato.com/) and [assembly instructions](https://www.unitrack-kato.com/how-to-use-jp). Kato uses a replaceable joiner; its instructions call for straight engagement and controlled in-plane separation. Design inference: make the wear item replaceable and give the joint rigid alignment features. The proposed parts are original geometry, not a dimensional copy or compatible Kato part.
- [Protolabs Network: snap-fit design](https://www.hubs.com/knowledge-base/how-design-snap-fit-joints-3d-printing/). Relevant guidance: fillet beam roots, avoid persistent spring deflection, choose favorable print direction, allow measured clearance, and use locating features to share shear. It identifies PETG among ductile snap-fit choices. The suggested clearances are starting points, not guaranteed A1 Mini fits. Our test compares clearances; no fatigue life is assumed.
- [Prusa PETG material guide](https://help.prusa3d.com/article/petg_2059). PETG is the working filament. Actual brand, drying, calibration and print orientation remain test variables.
- [K&J: magnetic closures](https://www.kjmagnetics.com/blog/magnetic-closures). More separation reduces attraction; a magnet pair and a magnet-to-steel contact are different configurations. Use thin local skins rather than separating magnets by a full structural beam. Measure the actual assembled clamp.
- [K&J: shear force](https://www.kjmagnetics.com/blog/magnet-shear-force). Sliding resistance depends on the contact interface and is not the same as normal pull. Design inference: locating pins/keys carry in-plane joint loads; do not treat magnet pull as a structural shear rating.
- [Supermagnete S-06-02-N datasheet](https://www.supermagnete.de/eng/data_sheet_S-06-02-N.pdf). One specific 6 × 2 mm disc is axially magnetized N45, with ±0.1 mm stated dimensional tolerance and approximately 740 g advertised holding force. That is not a rating for unspecified magnets, a pair through plastic/paper, or peeling paper. Measure your purchased magnets and test pocket fit.
- [User-linked RUSPEPA orange roll](https://www.amazon.com/RUSPEPA-Orange-Kraft-Paper-Roll/dp/B0CYNZ282B/). Listing identifies 24 inches × 100 feet; retrieved page shows $32.99 for the linked item. Price is an observation, not a purchase quote. Paper thickness/GSM was not confirmed; measure a sample. No water resistance is assumed.

## Three combinations to compare

A. Mechanical frame joints + removable snap battens for paper. No magnets or zip ties in the tested joints.
B. Keyed, magnet-held frame splices + magnetic paper pads. Most tool-free; the frame splice can release in peel and needs testing.
C. Mechanical frame joints + magnetic paper pads. Recommended experiment: a positive mechanical frame connection and a separately replaceable paper face.

The backing remains one PVC square with four corner braces. A split printed collar with two purchased M3 bolts/nuts is included as a no-zip-tie mounting experiment. A mating bolted receiver, pinch-release tongue and frame node are exported and shown assembled. Production rail endpoints, corner/diagonal nodes, angled PVC-brace nodes and full-gate counts remain to be integrated after coupon tests; the overall gate remains an architecture study.

## User-supplied picture-frame precedent

[Tony Youngblood: Snap-Together Modular Picture Frame](https://printables.com/model/150138-snap-together-modular-picture-frame-fits-any-size), inspected directly from the supplied ZIP, including STL meshes and its documentation PDF. The supplied license is CC BY-SA 4.0. The reference scene credits its author; retained source files and attribution are in `reference/picture_frame/`. Relevant observations: modular snap teeth, straight/corner members and a small calibration print; the original instructions call for supports beneath some edges. We use it to inform the connection and calibration workflow, with original gate-coupon geometry and an exposed pinch release.

## Diagonal and stacked manufacturing

[Bambu A1 Mini specifications](https://us.store.bambulab.com/products/a1-mini?id=543566369394393101) specify 180 × 180 × 180 mm. Diagonal envelopes, rail lengths and stack heights are calculated from our meshes and verified in Bambu Studio. No published source or slicer result is taken as proof that fused PETG necks will break cleanly. Initial 0.4 mm necks were omitted by the standard slicing profile; current continuous samples use 0.6/0.8 mm. Adding end tabs to the tabbed comparison removed an initial cantilever warning. All current supplied slices have supports disabled and no warnings; bridge quality remains to be tested.
