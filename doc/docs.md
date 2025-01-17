## tester.sh
The script determines its own directory, saves the current working directory, optionally checks for updates (without logic), returns to the original directory, activates a Python virtual environment, and runs a Python script (main.py) with any provided arguments.

## clean_cache.sh
This script cleans up unnecessary files and caches on a macOS system, focusing on 42 School-related files, browser caches, and other temporary data, while displaying a banner, calculating and showing available storage before and after cleaning, and providing contact information for reporting issues.

## install.sh
This script automates the setup of the Francinette tester by cloning its repository, installing necessary dependencies, creating a Python virtual environment, adding shell aliases for easy access, and restarting the shell to apply changes, while reminding users that the tester is not a replacement for their own tests.

## sync_utils.sh
This script updates utility files in specific project directories (libft, get_next_line, and printf) by copying them from a central tests/utils folder, while checking for changes in the target directories and skipping updates if changes are detected unless the -f flag is used to force the update.

## update.sh
This script updates the Francinette tester by fetching the latest changes from the repository, resetting to the latest version, updating submodules, activating the Python virtual environment, installing updated dependencies, and reminding users that the tester is not a replacement for their own tests.


