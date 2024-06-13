# A godot decomp/recovery utility

Moves C# files from a dll decomp to the scripts folder, attempting to copy the original directory structure.

---

## How to use

Open the .exe in GDRE_tools to generate the Godot project structure.

Open the game.dll in dnSpy and "Export to Project" to generate the dll decomp.

Move or copy the "GAME" folder from the dll decomp to the Godot project root (where the project.godot file is)

MAKE A BACKUP OF THE SCRIPTS FOLDER IN THE GODOT PROJECT ROOT!

Put this script in the Godot project root and run it.

Take note of what gets printed in the console; it'll tell you what files were unable to be matched and will need to be fixed manually.

The first section is what was found in the decomp that was unmatched in the godot project structure.

The second section is what was found in the godot project structure that was unmatched in the decomp.

---

## license

Consider the license CC0, as I have no interest in any copyright nonsense, and offer no support whatsoever. Frankly I wasn't even going to write the "How to use" until I realized I may need to document it so I know what the hell it does once I forget about it.

---
