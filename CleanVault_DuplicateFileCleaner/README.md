# Clean Vault — Duplicate File Cleaner

A Python automation tool that scans a directory and its subdirectories, identifies duplicate files using MD5 checksums, and removes extra copies to help reclaim disk space.

> **Important:** This script permanently deletes duplicate files. Review the target directory and back up important data before running it. The current version deletes duplicates automatically and does not provide a dry-run mode or a recycle-bin recovery option.

## Features

- **Recursive directory scanning:** Checks files in the selected directory and its subdirectories.

- **Checksum-based comparison:** Uses MD5 checksums to identify files with matching content.

- **Memory-conscious file reading:** Reads files in 1 KB chunks instead of loading each entire file into memory.

- **Input validation:** Checks whether the supplied path exists and is a directory.

- **Error handling:** Reports files that cannot be read and continues scanning where possible.

- **Deletion error handling:** Reports failed deletion attempts rather than silently ignoring them.

- **Deletion report:** Displays duplicate groups, duplicate counts, successful deletions, and failed deletions.

- **Timestamped messages:** Records local time for successful and failed deletion attempts.

## Requirements

- Python **3.x**

- No third-party Python packages are required. The script uses Python standard-library modules:

  - `os` — directory traversal, path operations, and file deletion

  - `hashlib` — MD5 checksum calculation

  - `datetime` — timestamps for the report

## Project Structure

```
CleanVault/    
├── CleanVaultDuplicateFileCleaner.py    
└── README.md
```

Your local folder and script filename can differ; adjust the commands below if yours do.

## Installation

### 1. Check Python

Verify that Python 3 is installed:

```
python3 --version
```

On systems where you use a version-specific Python command, you can use that command instead.

### 2. Get the project

Clone your GitHub repository:

```
git clone https://github.com/`AshTech21/Automation\_Projects.git`    
`cd Automation\_Projects/CleanVault\_DuplicateFileCleaner`
```

Replace `YOUR-USERNAME` and `CleanVault` with your GitHub username and repository name.

Alternatively, download the repository ZIP from GitHub and extract it.

## Configuration

In the current script, the target directory is set in `main()`:

```
def main():    
    DirectoryName = "Test"    
    DeleteDuplicate(DirectoryName)
```

Change `"Test"` to the directory you want to scan.

For example, use an absolute path:

```
def main():    
    DirectoryName = "/home/your-user/Documents/Test"    
    DeleteDuplicate(DirectoryName)
```

Or use a relative path, such as `"Test"`. A relative path is resolved from the script's **current working directory**, not necessarily the directory containing the script.

**Double-check the path before execution.** The selected directory and its subdirectories are scanned, and duplicate files may be permanently deleted.

## Usage

Run the script from a terminal:

```
python3 CleanVaultDuplicateFileCleaner.py
```

If you use a specific Python version, run the script with that interpreter, for example:

```
python3.13 CleanVaultDuplicateFileCleaner.py
```

The script scans the configured directory, prints duplicate groups, retains the first file encountered in each group, and attempts to delete the other files.

## How It Works

1. **Validate the directory.** The program checks whether the configured path exists and is a directory.

2. **Traverse folders.** `os.walk()` visits the target directory and its subdirectories.

3. **Calculate checksums.** Each file is opened in binary mode and read in 1 KB chunks. The chunks are fed into `hashlib.md5()`.

4. **Group matching files.** File paths are stored in a dictionary keyed by their checksum.

5. **Identify duplicates.** Groups containing more than one file are considered duplicate groups.

6. **Keep one copy.** The first file in each group is retained; the program attempts to delete the remaining files.

7. **Report results.** The program prints totals for duplicate groups, duplicate files, successful deletions, and failed deletions.

### What does “duplicate” mean here?

The script treats files with matching MD5 checksums as duplicates. This is a practical way to compare file contents, but MD5 is not collision-resistant against deliberate attacks. For important data, a more cautious implementation could also compare file sizes and/or use SHA-256, and verify file contents before deletion.

The script keeps the first file encountered by the directory traversal. It does not choose the newest, oldest, shortest-path, or otherwise preferred copy.

## Example Output

Output varies depending on the files found. A typical report may look like this:

```
Scanning directory: /path/to/Test    
----------------------------------------------------------------------    
    
======================================================================    
           DUPLICATE FILE DELETION REPORT    
======================================================================    
Duplicate groups found : 2    
Duplicate files found  : 3    
    
Starting deletion process...    
    
----------------------------------------------------------------------    
Duplicate Group: 1    
Original file kept: /path/to/Test/report.pdf    
----------------------------------------------------------------------    
    
\\\[DELETED SUCCESSFULLY\\\]    
File name : report-copy.pdf    
Full path : /path/to/Test/backup/report-copy.pdf    
Deleted at: 2026-10-09 12:00:00 IST    
    
======================================================================    
                  FINAL SUMMARY    
======================================================================    
Duplicate groups found       : 2    
Duplicate files found        : 3    
Files deleted successfully   : 3    
Files that failed to delete  : 0    
Process completed at         : 2026-10-09 12:00:01 IST    
======================================================================
```

*The paths, counts, and timestamps above are illustrative examples, not results from a real run.*

## Error Handling

The script handles several common errors:

- **Directory does not exist:** Displays an error and stops the operation.

- **Path is not a directory:** Displays an error and stops the operation.

- **File cannot be read:** Reports the file and reason, then continues scanning other files where possible.

- **Deletion fails:** Reports the file and reason, increments the failure count, and continues processing.

Filesystem permissions, files in use, storage errors, and other operating-system conditions can still prevent operations from succeeding.

## Safety and Limitations

Please understand these behaviors before using the script:

- **Deletion is permanent:** `os.remove()` removes the file; this script does not move it to a trash folder.

- **No confirmation or dry run:** The current version begins deleting duplicates automatically after scanning.

- **First encountered copy is kept:** The retained copy depends on traversal order and is not guaranteed to be the best-named or most useful copy.

- **Checksum collisions are possible:** Matching MD5 checksums are not an absolute mathematical guarantee that two files have identical contents.

- **Symbolic links and special files:** The current implementation does not explicitly filter symbolic links or special file types.

- **Concurrent file changes:** A file may change between scanning and deletion; the current script does not re-check its contents immediately before removal.

- **Test first:** Try the script on a directory containing disposable sample files before using it on valuable data.

## Use Cases

- Finding repeated documents and downloads

- Cleaning duplicate files from backup folders

- Identifying repeated media files

- Learning Python automation, file handling, hashing, and exception handling

## Contributing

Contributions and suggestions are welcome.

1. Fork the repository.

2. Create a branch for your change.

3. Test your changes using disposable sample files.

4. Submit a pull request explaining the improvement.

For deletion-related changes, test carefully to ensure that unique files are never removed unintentionally.

## Author

**AshwinKumar Suhas Kulkarni**

If you find this project useful, consider starring the repository on GitHub.

