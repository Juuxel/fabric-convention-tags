# Fabric Convention Tags

This repository aims to collect [Minecraft tags](https://minecraft.gamepedia.com/Tag) in the convention namespace `c`, which may be used by multiple mods to express similar things.

# Use

Drop the mod jar files you want to extract tags from into a `mods` subfolder and run the `collect_mod_tags.py` script.

This will update the tags.json file (incrementally, existing tags will not be removed). 

Then run `to_mediawiki.py` to generate the Mediawiki text for the wiki.
