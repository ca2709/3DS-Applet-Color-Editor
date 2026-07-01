# 3DS Applet Color Editor (3DS-ACE)

*A dead simple program to recolor home screen icons using your home screen's romfs (for those of us who dont want to use a hex editor ;D)*

<sup>This should be self-explanitory, but your 3DS *must* have CFW with GM9 and Luma3DS.</sup>

## How to set up

> This is not a comprehensive guide! Some details may be missing or incomplete.

### You need:

- Luma3DS and GM9 on a modded system
- [HMRT](https://github.com/schrmh/HMRT)

To start, dump your `HomeMenu.cia` using GodMode9:
1. Enter GM9 by holding START while booting
    - Navigate through `[1:] SYSNAND CTRNAND ` → `title` → `00040030`
2. Navigate to the appropriate folder depending on your region:
    - JPN: `00008202`
    - USA: `00008F02`
    - EUR: `00009802`
    - CHN: `0000A102`
    - KOR: `0000A902`
    - TWN: `0000B102`
3. Navigate to `content`
4. Select the `.tmd`, then choose `TMD File Options...` → `Build CIA (standard)`
5. Insert your SD/MicroSD into your computer
6. Backup the new `.cia` in the card's `gm9/out` folder, and rename it to `HomeMenu.cia`.
7. Place that new file in your `HMRT-master` folder and open the folder in CMD.
8. Run the command `HMRT`. This should give you the HMRT menu. Select option 1, then once that's done, option 5.

You should now have a decompressed romfs folder titled `ExtractedRomFS`. You can now use 3DS-ACE to change the colors of your applets to match whatever theme you have! When you save, backups of all the edited files will be saved under `[FILENAME].LZ.bak`. To restore them, delete the edited file and remove the `.bak` extension.

## How to apply

> this carries no bricking risk and is 100% reversible, but there is another method done by rebuilding the CIA. I will not be providing that here, but if for whatever reason you want to risk a soft brick, you can find it easily online.

1. Copy the contents of your `ExtractedRomFS` folder and paste them in whichever directory matches your reigon:
    - JPN: `luma/titles/0004003000008202/romfs`
    - USA: `luma/titles/0004003000008F02/romfs`
    - EUR: `luma/titles/0004003000009802/romfs`
    - CHN: `luma/titles/000400300000A102/romfs`
    - KOR: `luma/titles/000400300000A902/romfs`
    - TWN: `luma/titles/000400300000B102/romfs`

<sup>note: create any directories that don't exist</sup>

2. Hold SELECT while booting your 3DS to get to the Luma menu
3. Navigate to `( ) Enable game patching` and press (A) to tick it
4. Restart your system
5. You're done! The home menu should reflect your changes.
