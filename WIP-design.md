The binding constraint is the sheet, not the printer. An 8×4 ft Coroplast sheet is **2438 × 1219 mm**. Your outer face is **2700 mm**, so every 2700 mm edge must be spliced. The 4 ft width is almost exactly two 600 mm borders:

\[
1219 - 600 - 600 = 19\ \text{mm}
\]

That leftover is kerf. Cut two **600 × 2438 mm** strips per sheet and treat 2700 as **2438 + 262**.

Use **¾″ Schedule 40 PVC**. Outside diameter is **26.67 mm** — that is the number every clip is sized to, not “¾ inch.”

---

## Architecture

Two identical PVC squares, 260 mm apart, with the Coroplast ring hung on the **front** square. The sheet is the shear web; the prints only locate pipe and sheet. Do not try to 3D-print the 2.7 m structure.

```
FRONT                          REAR (pipe only)
2700 PVC square                2700 PVC square
Coroplast ring clipped on      optional second ring
        | 260 mm printed standoffs |
        feet on the bottom pipe
```

Inner 1500 mm hole is cut in the sheet. A printed inner-corner set keeps that hole square and can hold the 140 mm lip from your drawing.

---

## Coroplast cut list — 3 sheets per gate (recommended)

**Why 3:** 2 sheets cover the front ring; the third gives splice tabs, 140 mm inner returns, and 260 mm tunnel walls on the *inner* opening (the part the drone actually flies through).

All strips are **600 mm wide** except the returns and tunnel walls.

| Piece | Qty | Size (mm) | From |
|---|---|---|---|
| Top long | 1 | 600 × 2438 | Sheet 1 |
| Bottom long | 1 | 600 × 2438 | Sheet 1 |
| Left stile | 1 | 600 × 1500 | Sheet 2 |
| Right stile | 1 | 600 × 1500 | Sheet 2 |
| Splice tabs (complete the 2700 edges) | 2 | 600 × 262 | Sheet 2 remainder |
| Inner returns (140 mm lip) | 4 | 140 × 1500 | Sheet 3 |
| Inner tunnel walls | 4 | 260 × 1500 | Sheet 3 |

**Sheet 1:** two 600 × 2438 strips (top + bottom mains).  
**Sheet 2:** two 600 × 2438 strips → cut 1500 + 262 from each; leftover 676 × 600 × 2 is spare / mid-span patches.  
**Sheet 3:** rip 140 mm and 260 mm strips along the 8 ft edge, then cross-cut to 1500.

Add a **4th sheet** only if you want a matching rear face (looks correct from both approach directions and stiffens the box).

Seam placement: put the 262 mm splice at a **corner**, not mid-span. Then the printed corner handles the joint and you never have a weak butt in the middle of a 2.7 m run.

---

## PVC cut list (¾″ Sch 40)

Printed corners replace store elbows, so pipe is cut to **finished outer size minus socket depth**. Design each printed socket **30 mm deep**. Then:

| Member | Qty | Cut length |
|---|---|---|
| Front outer rails | 4 | 2700 − 2×30 = **2640 mm** |
| Rear outer rails | 4 | **2640 mm** |
| Optional inner square (front) | 4 | 1500 − 2×30 = **1440 mm** |
| Feet (each side) | 4 | 400–500 mm |

Skip the inner PVC square if you want fewer parts — the Coroplast hole + inner-corner prints are enough for vision. Add the inner square only if the 1500 mm hole starts to flutter.

Do not glue. Friction + one zip-tie or M4 through the printed socket. A crash should pop a joint, not snap 2.6 m of pipe.

---

## Printed parts (PLA family)

Design everything around **one pipe OD: 26.7 mm**. Print a 20 mm test ring first; add 0.2–0.3 mm clearance if it will not snap on, or 0.1 mm interference if it is sloppy. PLA creeps — every snap also gets a **zip-tie tunnel** or an **M4 clamp** so the clip cannot walk off.

### 1. Outer corner — print 8 (4 front, 4 rear)

3-way block:

- Two sockets at 90° in the face plane (the 2700 square)
- One socket backward for the 260 mm standoff
- 6 mm slot in the face plane for Coroplast (4–5 mm sheet + 1 mm slop)
- Bosses so the 262 mm splice tab lands *inside* this corner

Keep walls ≥ 3.2 mm (4 perimeters at 0.4 mm). Fillet the slot entry so you can slide the sheet in after the pipe is assembled.

### 2. Mid-edge sheet clip — print 16–20

C-clamp on the 26.7 mm pipe, 180–200° wrap, 40–50 mm long.

- 6 mm Coroplast slot parallel to the pipe
- 5 mm zip-tie slot across the open side of the C
- Optional 4 mm hole to screw into a flute of the Coroplast (do not crush flutes; use a printed barrel nut or a fender washer)

Space about every 400–450 mm on each 2700 mm rail (5 per long edge, 3 per 1500 mm stile). Christmas-display “Coro-to-PVC” clips are the same idea; size yours for ¾″ not ½″.

### 3. Face splice plate — print 2 (or 4 if you also splice stiles)

125 × 80 × 6 mm plate with a 6 mm slot or a sandwich of two plates.

- Sits behind the 262-to-2438 butt
- Four 4 mm holes; #8 × ¾″ screws into flutes, or printed T-nuts
- Alignment pins so the 600 mm border stays coplanar (vision cares about a flat face)

### 4. Inner-corner “picture frame” — print 4

This is the part that makes the gate look like your drawing.

- L-shaped 140 × 140 mm in the face plane
- Slot for the 1500 mm hole edge
- Second slot or tabs for the 140 × 1500 return folded into the opening
- Optional third slot for the 260 × 1500 tunnel wall

Result: sharp inner square, 140 mm visible inner thickness, 260 mm depth, all registered to each other.

### 5. Depth standoff — print 4 (add 4 mid-span if the box wracks)

260 mm clear between front and rear pipe centerlines. Two options:

- **Printed beam** 260 mm between two 26.7 mm saddles (fast, more PLA)
- **PVC nipple** 260 mm with printed saddles at each end (less PLA, stronger)

If you use a PVC nipple, printed part is just two saddles + a set screw.

### 6. Foot tee — print 2

Clips to the bottom front *and* rear pipes so the 260 mm depth becomes a stable base. Add a 20 mm hole for a rebar stake or a sandbag hook.

---

## Print settings (PLA that will get hit)

| Setting | Value |
|---|---|
| Perimeters | 4–5 |
| Infill | 30–40% gyroid |
| Layer | 0.2 mm |
| Orientation | sockets vertical so layer lines are not across the snap |
| Material | PLA is fine if clips are sacrificial; PETG if gates sit in a hot car or sun |

Budget ~400–600 g PLA per gate for the full set. Reprint mid-edge clips after a hard strike; leave corners thicker so you reprint those less often.

---

## Assembly order

1. Print one test C-clip. Confirm snap on your actual pipe.  
2. Cut all Coroplast; dry-fit the ring on the floor (2438 + 262 + 1500 stiles).  
3. Assemble front PVC square in printed corners.  
4. Slide top/bottom 2438 strips into corner slots; add splice tabs; screw splice plates.  
5. Drop in left/right 1500 stiles.  
6. Clip mid-edge clips every ~400 mm.  
7. Fit inner-corner prints + 140 mm returns + 260 mm inner walls.  
8. Stand off the rear square. Add feet.  
9. Measure the hole: target **1500 ± 10 mm** both ways, diagonals equal within 15 mm.

---

## What not to do

- Do not span 2700 mm with a single 8 ft strip and “stretch” it.  
- Do not rely on a PLA snap alone — zip-tie every clip.  
- Do not glue PVC.  
- Do not put the 262 mm seam at mid-span.  
- Do not use ½″ PVC for this span; it will banana unless you add an inner square and more clips.

If you want, next step I can spec the clip in numbers ready to model (socket ID, slot width for 4 mm vs 5 mm Coroplast, and a single parametric corner you can scale if your sheet is 4 mm or 5 mm).
