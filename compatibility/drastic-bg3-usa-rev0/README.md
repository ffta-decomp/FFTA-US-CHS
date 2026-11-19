# FFTA2 USA Rev 0 DraStic graphics compatibility patch

[Download the r1 BPS patch](ffta2-usa-drastic-bg3-wrap-r1.bps?raw=true)

This optional patch is for the original North American release of *Final Fantasy Tactics A2: Grimoire of the Rift* (A6FE, revision 0). Apply it to a clean copy of your own ROM with a BPS patcher. Back up your in-game save and start a fresh emulator session. The patch preserves the original language options. **Compatibility on the original DraStic build remains unverified.**

| File | SHA-256 |
| --- | --- |
| Original USA Rev 0 ROM | `3b5d469aae5d351de31a89cf2bf592c98cb5b68cb4efc30b34426a119fee2372` |
| r1 BPS | `9c3957d39b7dbd94ee1100841ae203e184fa1950076d3b3819a426969abaf70d` |
| Patched USA Rev 0 ROM | `960e946f01f34d905db907a8db33aec33112bbad0bb33a88728c888942b7a2b9` |

## Reproduction and observations

1. Start a new game with the unmodified USA Rev 0 ROM. Play through the prologue into the first forest battle against Klesta. Watch the arrival sequence before issuing a battle command. A battle suspend save can skip part of that sequence.
2. Repeat the route with r1 and the same inputs. In a replay using the instrumented melonDS 0.9.5 software renderer, the original entered the relevant BG3 clipping path during the prologue and Klesta's arrival. Both runs reached the first-battle dialogue. The patched run completed the same **24,346 frames** with zero matching clipping records.
3. For a separate spell test, compare Thunder casts that hit one, two, and three units. Controlled replays on a Plus build entered the same clipping path for all three target counts. This included a three-target case in which every target survived and double speed was disabled. Applying the same two instruction changes preserved the measured damage.

A separate Blue Mage test on Plus successfully learned the skill and returned to the command menu. The tested learning case and its miss control produced zero matching clipping records. Other skills, camera angles, and battle states remain open.

These comparisons reproduce the graphics condition in a diagnostic core. A matching clipping record counts a rendering observation. Original DraStic crash reproduction remains pending.

## Rendering behavior and workaround

Some battle and cutscene effects share an 8-bit indexed affine bitmap on the main display engine's BG3 layer. When a transform puts a screen pixel outside a bitmap with wrapping disabled, native DS rendering treats that pixel as transparent. Earlier reports point to this clipping path in DraStic.

r1 changes two ARM9 instructions in the shared bitmap setup. The 128×128 and 256×256 indexed branches enable wrapping so that out-of-range coordinates map to the opposite edge. The direct-color branch, effect assets, battle rules, and save format stay as in the original.

Some frames can show extra flashes or repeated edges where the original would show transparency. This was visible during Fire and Klesta's arrival. The long-term emulator fix is to treat out-of-range pixels in non-wrapping bitmaps as transparent before fetching the pixel.

## Test coverage

The structural scan covered all **421 recognized EFX containers** in the USA Rev 0 archive index. It found **192** candidates with 128×128 indexed bitmaps, **167** of them associated with registered magic effects. Runtime coordinates depend on the animation, camera, and targets.

The 31 diagnostic runs covered cold prologue replays, Fire, four Klesta animation records, Thunder with several target counts, and eight additional effect spot checks. The 256×256 setup branch passed instruction-level checks. All matching bitmaps found in the archive were 128×128. Full gameplay and original DraStic validation remain open.

## Appendix — Original reproduction materials

| Supplied material | How it informed the tests |
| --- | --- |
| *FFTA2 ROM Crash Investigation*, revision 2, 2026-11-19 | The report analyzed a publicly reported European-version DraStic crash and proposed indexed bitmap clipping as a candidate mechanism. Player reports mentioned multi-target Thunder, bird attacks, and summons. The report also recorded roughly 300 enemy attacks on a Mac without a crash, with incomplete equivalence to the reported setups. These observations motivated checking both the arrival sequence and spell animations. The European report and the USA Rev 0 replay provide separate evidence. |
| First-battle suspend save | The supplied save cold-loaded into the Klesta battle. The observed continuation produced zero matching clipping records. The clean new-game replay was used to capture the earlier arrival sequence. |
| Ordinary save after the first quest | The second supplied save records one completed quest. It was inspected as a progress reference. The Klesta arrival and Thunder results above came from their own qualified inputs. |

For visual reports, capture both DS screens side by side in landscape. Use the same layout for the original and patched ROMs, and record the lead-in, the effect, and what happens afterward.
