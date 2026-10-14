# Farm CLI (mini)

A small command-line tool that organizes farm documents into `immovable`, `movable`, `animals`, and `other` folders using keywords in file names.

## The problem it solves

Farm documents often end up in one download folder. Sorting them manually takes time.

This tool organizes them automatically. By default, it shows a preview without moving files. Existing destination files are never overwritten.

## Files

| Path | Purpose |
|---|---|
| `cli.py` | Main program: file organization, record creation, and reporting |
| `README.md` | Project description and usage instructions |
| `.gitignore` | Keeps the generated `farm/` folder out of the repository |
| `contributions/` | One contribution file per team member |

## Requirements

Python 3. No additional packages are required.

## Usage

Run the commands from the folder containing `cli.py`.

### Preview file organization

```bash
python cli.py organize --source test_inbox
```

This shows where files would go without moving them.

Example output:

```text
Would move: land_record.pdf -> immovable/
Would move: tractor_invoice.pdf -> movable/
Would move: vet_visit.txt -> animals/
Would move: weekly_notes.txt -> other/
Preview only. Add --apply to move the files.
```

### Move files

```bash
python cli.py organize --source test_inbox --apply
```

Files are moved into their category folders inside `farm/`.

### Add a record

```bash
python cli.py add --category movable --name "John Deere Tractor" --details "2019 model"
```

This creates `farm/movable/john_deere_tractor.txt` with the name, category, and details.

Records can be added to `immovable`, `movable`, or `animals`.

### Show a report

```bash
python cli.py report
```

This displays the number of files in each category and the total. Sub-folders are not counted.

### Use a different destination folder

The `--path` option changes the destination folder. The default is `farm`.

```bash
python cli.py organize --source test_inbox --path my_farm --apply
python cli.py report --path my_farm
```

## How files are categorized

The program removes the file extension, converts the name to lowercase, and splits it into words using underscores, hyphens, and spaces.

The first word matching the `RULES` dictionary determines the category. Only English keywords are included.

| Category | Keywords |
|---|---|
| `immovable` | `deed`, `land`, `field`, `house` |
| `movable` | `tractor`, `plow`, `invoice` |
| `animals` | `vaccine`, `vet`, `cattle` |
| `other` | Used when no keyword matches |

Whole words are matched. For example, `warehouse` does not match `house`, and `tractor2026` does not match `tractor`.

## Safety

- File organization is a preview unless `--apply` is provided.
- Existing destination files are skipped.
- Moving a file removes it from the source folder.
- Hidden files, folders, `cli.py`, and `README.md` are skipped during organization.
- Record names cannot be empty or contain `..`, `/`, or `\`.
- Errors during file moving and record writing are caught and displayed.

## Manual tests

The following cases were tested:

### Test 1: Missing source folder validation

```bash
python3 cli.py organize --source "exixsted folder"
```

Output:
```text
[ERROR] Source folder not found: 'exixsted folder'
```
### Test 2: Preview file organization (Dry-run)
```bash
python3 cli.py organize --source test_inbox
```

Output:
```text
Would move: land_record.pdf -> immovable/
Would move: tractor_invoice.pdf -> movable/
Would move: vet_visit.txt -> animals/
Would move: weekly_notes.txt -> other/
Preview only. Add --apply to move the files.
```
### Test 3: Move files to category folders

```bash
python3 cli.py organize --source test_inbox --apply
```

Output:
```text
Moved: land_record.pdf -> immovable/
Moved: tractor_invoice.pdf -> movable/
Moved: vet_visit.txt -> animals/
Moved: weekly_notes.txt -> other/
```
### Test 4: Create a new animal record

```bash
python3 cli.py add --category animals --name "Test Cow" --details "Born in 2023, healthy"
```

Output:
```text
[SUCCESS] Record created: farm/animals/Test_cow.txt
```
### Test 5: Prevent overwriting existing records

```bash
python3 cli.py add --category animals --name "Test Cow" --details "Updated details"
```

Output:
```text
[ERROR] Record already exists: farm/animals/Test_cow.txt
```
### Test 6: Reject invalid path characters (Security)

```bash
python3 cli.py add --category animals --name "test/name"
```

Output:
```text
[ERROR] Invalid name (empty, or contains '..', '/' or '\').
```
### Test 7: Generate inventory and summary report

```bash
python3 cli.py report
```

Output:
```text
immovable: 1 files
movable: 1 files
animals: 2 files
other: 1 files
Total: 5 files
```

## Limitations

- Classification uses file names, not file contents.
- Only the listed English keywords are recognized.
- Source sub-folders are not scanned.
- If a name matches multiple categories, the first matching word determines the category.
- The report counts only files directly inside each category folder.
- An empty source folder produces no output when `--apply` is used.