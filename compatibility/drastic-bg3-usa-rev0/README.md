# FFTA2 USA Rev 0 DraStic graphics compatibility patch

[Download the r1 BPS patch](ffta2-usa-drastic-bg3-wrap-r1.bps?raw=true)

This optional patch is for the original North American release of *Final Fantasy Tactics A2: Grimoire of the Rift*, game code A6FE, revision 0. Apply the BPS to a clean copy of your own ROM with a BPS patcher. Back up your in-game save and start a fresh emulator session. The patched game remains in English.

| File | SHA-256 |
| --- | --- |
| Original USA Rev 0 ROM | `3b5d469aae5d351de31a89cf2bf592c98cb5b68cb4efc30b34426a119fee2372` |
| r1 BPS | `9c3957d39b7dbd94ee1100841ae203e184fa1950076d3b3819a426969abaf70d` |
| Patched USA Rev 0 ROM | `960e946f01f34d905db907a8db33aec33112bbad0bb33a88728c888942b7a2b9` |

## Reproducing the graphics condition

1. Start a new game with an unmodified USA Rev 0 ROM. Play through the prologue into the first forest battle against Klesta. Observe the arrival sequence before issuing a battle command. Loading a battle suspend save can skip the relevant sequence.
2. Repeat with the patched ROM and the same game inputs. In our instrumented melonDS 0.9.5 software-renderer comparison, the original entered the affected clipping path during Klesta's arrival. Both runs reached the first-battle dialogue. The patched run completed the same 24,346-frame replay with zero matching clipping records.
3. In a battle with Thunder available, compare casts that hit one, two, or three units. In controlled replays, all three target counts used the affected path with the original settings. The workaround preserved the measured damage. The three-target case also entered the path with all targets surviving and double speed disabled.

These steps exercise the graphics condition observed in the diagnostic core. Confirmation on the original DraStic build is pending.

## Why it happens

Some battle and cutscene effects use the main display engine's BG3 as an 8-bit indexed affine bitmap. Moving or scaling the bitmap can put a screen pixel outside the texture. With wrapping disabled, the DS rendering behavior is to treat that pixel as transparent. The suspected DraStic defect is in this clipping path. The condition can arise during a cutscene or a spell animation because they share bitmap setup code.

## How r1 avoids it

The patch changes two ARM9 instructions in the common bitmap setup routine. Both the 128×128 and 256×256 indexed branches enable BG3 wrapping, so out-of-range coordinates map back into the texture. The patch leaves the direct-color branch, effect data, battle rules, and save format unchanged.

Wrapping has a visible cost. Some frames show extra or repeated flashes at the screen edges, including in the Fire animation and Klesta's arrival. Use this patch as an opt-in compatibility workaround. The long-term emulator fix is to treat out-of-range pixels in a non-wrapping affine bitmap as transparent before fetching the pixel.

## Coverage

The static scan inspected all 421 recognized EFX containers in the USA Rev 0 archive index. It found 192 matching indexed-bitmap candidates, including 167 registered magic effects. A matching bitmap is a candidate because its coordinates depend on the animation, camera, and targets at runtime.

The 31 diagnostic runs included the cold prologue replay, Fire, four Klesta animation records, Thunder with several target counts, and eight additional effect spot checks. A Blue Mage learning comparison confirmed that learning could complete, with zero matching clipping events in the tested case. Runtime coverage is limited to the scenes and inputs listed here. The 256×256 setup branch was checked at instruction level. Full playthrough and DraStic validation remain pending.
