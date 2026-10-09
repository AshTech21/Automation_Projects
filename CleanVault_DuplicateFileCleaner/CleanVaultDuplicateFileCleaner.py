###########################################################################################################
# Automation Script Name : Clean Vault
# Use                    : It finds all the duplicate files and delete them to maintain the storage.
# Author name            : AshwinKumar Suhas Kulkarni
###########################################################################################################
import os
import hashlib
from datetime import datetime


def CalculateChecksum(FileName):
    # Calculate the checksum of a file
    hobj = hashlib.md5()

    with open(FileName, "rb") as fobj:
        Buffer = fobj.read(1024)  # Read 1 KB at a time

        while Buffer:
            hobj.update(Buffer)
            Buffer = fobj.read(1024)

    return hobj.hexdigest()


def FindDupllicate(DirectoryName):
    # Validate the directory
    if not os.path.exists(DirectoryName):
        print("\n[ERROR] Path does not exist:", DirectoryName)
        return None

    if not os.path.isdir(DirectoryName):
        print("\n[ERROR] The given path is not a directory:", DirectoryName)
        return None

    Duplicate = {}

    print("\nScanning directory:", os.path.abspath(DirectoryName))
    print("-" * 70)

    for FolderName, Subfolder, Filename in os.walk(DirectoryName):

        for fname in Filename:
            FilePath = os.path.join(FolderName, fname)

            try:
                CheckSum = CalculateChecksum(FilePath)

                if CheckSum in Duplicate:
                    Duplicate[CheckSum].append(FilePath)
                else:
                    Duplicate[CheckSum] = [FilePath]

            except (OSError, PermissionError) as e:
                print("\n[ERROR] Unable to read file:", FilePath)
                print("Reason:", e)

            except Exception as e:
                print("\n[ERROR] Unexpected error while reading:", FilePath)
                print("Reason:", e)

    return Duplicate


def DeleteDuplicate(DirectoryName):
    MyDict = FindDupllicate(DirectoryName)

    # Stop if the directory is invalid
    if MyDict is None:
        return

    # Keep only groups containing duplicate files
    Result = [
        files for files in MyDict.values()
        if len(files) > 1
    ]

    TotalGroups = len(Result)

    TotalDuplicatesFound = sum(
        len(files) - 1 for files in Result
    )

    TotalDeleted = 0
    TotalFailed = 0

    print("\n" + "=" * 70)
    print("           DUPLICATE FILE DELETION REPORT")
    print("=" * 70)

    print("Duplicate groups found :", TotalGroups)
    print("Duplicate files found  :", TotalDuplicatesFound)

    if TotalDuplicatesFound == 0:
        print("\nNo duplicate files found.")
        print("No files were deleted.")
        print("=" * 70)
        return

    print("\nStarting deletion process...\n")

    # Process each group of duplicate files
    for group_number, files in enumerate(Result, start=1):

        # Preserve the first file in each group
        OriginalFile = files[0]

        print("-" * 70)
        print("Duplicate Group:", group_number)
        print("Original file kept:", OriginalFile)
        print("-" * 70)

        # Delete the remaining copies
        for DuplicateFile in files[1:]:

            try:
                os.remove(DuplicateFile)

                # Record the time after successful deletion
                DeletedAt = datetime.now().astimezone().strftime(
                    "%Y-%m-%d %H:%M:%S %Z"
                )

                TotalDeleted += 1

                print("\n[DELETED SUCCESSFULLY]")
                print("File name :", os.path.basename(DuplicateFile))
                print("Full path :", os.path.abspath(DuplicateFile))
                print("Deleted at:", DeletedAt)

            except OSError as e:
                TotalFailed += 1

                print("\n[DELETION FAILED]")
                print("File name :", os.path.basename(DuplicateFile))
                print("Full path :", os.path.abspath(DuplicateFile))
                print("Attempted at:", datetime.now().astimezone().strftime(
                    "%Y-%m-%d %H:%M:%S %Z"
                ))
                print("Reason:", e)

    # Final summary
    print("\n" + "=" * 70)
    print("                  FINAL SUMMARY")
    print("=" * 70)

    print("Duplicate groups found       :", TotalGroups)
    print("Duplicate files found        :", TotalDuplicatesFound)
    print("Files deleted successfully   :", TotalDeleted)
    print("Files that failed to delete  :", TotalFailed)

    print("Process completed at         :", datetime.now().astimezone().strftime(
        "%Y-%m-%d %H:%M:%S %Z"
    ))

    print("=" * 70)


def main():
    DirectoryName = "Test"
    DeleteDuplicate(DirectoryName)


if __name__ == "__main__":
    main()
