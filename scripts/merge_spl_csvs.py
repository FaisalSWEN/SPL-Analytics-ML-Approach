import csv
import re
import sys
from pathlib import Path

# Merge all CSV files under Dataset/Saudi-Professional-League-Datasets-master into Dataset/SPL_raw.csv
# Uses only Python standard library for portability


def find_csv_files(root: Path):
    # Handle possible nested duplicated directory names
    search_root = root / "Dataset" / "Saudi-Professional-League-Datasets-master"
    if not search_root.exists():
        print(f"ERROR: Directory not found: {search_root}", file=sys.stderr)
        sys.exit(1)
    # look for csv recursively
    return sorted(search_root.rglob("*.csv"))


def parse_file_metadata(file_path: Path):
    """Parse season info from filename like 'SPL-2008-2009-FS.csv'.
    Returns dict with: season_label, season_start_year, season_end_year, stage.
    """
    filename = file_path.name
    m = re.search(r"^SPL-(\d{4})-(\d{4})-([A-Za-z]+)\.csv$", filename)
    season_start_year = season_end_year = None
    stage = None
    if m:
        season_start_year = int(m.group(1))
        season_end_year = int(m.group(2))
        stage = m.group(3).upper()
    season_label = (
        f"{season_start_year}-{season_end_year}" if season_start_year and season_end_year else None
    )
    return {
        "season_label": season_label or "",
        "season_start_year": season_start_year or "",
        "season_end_year": season_end_year or "",
        "stage": stage or "",
        "source_file": file_path.name,
    }


def gather_headers(files):
    headers = []
    seen = set()
    for f in files:
        with f.open("r", encoding="utf-8", newline="") as fh:
            reader = csv.DictReader(fh)
            if reader.fieldnames:
                for h in reader.fieldnames:
                    if h not in seen:
                        seen.add(h)
                        headers.append(h)
    # Ensure metadata headers exist and appear at the end for readability
    for meta_h in [
        "season_label",
        "season_start_year",
        "season_end_year",
        "stage",
        "source_file",
    ]:
        if meta_h not in seen:
            headers.append(meta_h)
    return headers


def get_first(row: dict, candidates):
    for key in candidates:
        if key in row and row[key] not in (None, ""):
            return row[key]
    return ""


def build_normalized_row(row: dict, meta: dict):
    # Handle BOM-prefixed variants and alternative column names.
    date = get_first(row, ["Date", "\ufeffDate", "Date.2"])
    time = get_first(row, ["Time"])  # may be empty in some files
    match_id = get_first(
        row, ["matchNo", "Match No.", "\ufeffmatchNo"])  # optional

    home_team = get_first(row, ["Team1", "Home_team"])
    away_team = get_first(row, ["Team2", "Away_team"])
    home_score = get_first(row, ["Score1", "Home_team_score"])
    away_score = get_first(row, ["Score2", "Away_team_score"])

    stadium = get_first(row, ["Stadium"])  # may not exist in early files
    city = get_first(row, ["City"])  # may not exist in early files
    round_name = get_first(row, ["Round"])  # may not exist in early files
    referee_name = get_first(row, ["Referee_name"])  # may not exist
    attendance = get_first(row, ["Attendance"])  # may not exist

    normalized = {
        "match_id": match_id,
        "date": date,
        "time": time,
        "home_team": home_team,
        "away_team": away_team,
        "home_score": home_score,
        "away_score": away_score,
        "stadium": stadium,
        "city": city,
        "round": round_name,
        "referee_name": referee_name,
        "attendance": attendance,
        "season_label": meta.get("season_label", ""),
        "season_start_year": meta.get("season_start_year", ""),
        "season_end_year": meta.get("season_end_year", ""),
        "stage": meta.get("stage", ""),
        "source_file": meta.get("source_file", ""),
    }
    return normalized


def merge(files, out_path: Path, headers, normalized_out_path: Path, normalized_headers):
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8", newline="") as out_f, \
            normalized_out_path.open("w", encoding="utf-8", newline="") as norm_f:
        writer = csv.DictWriter(out_f, fieldnames=headers)
        writer.writeheader()
        norm_writer = csv.DictWriter(norm_f, fieldnames=normalized_headers)
        norm_writer.writeheader()
        for f in files:
            with f.open("r", encoding="utf-8", newline="") as fh:
                reader = csv.DictReader(fh)
                meta = parse_file_metadata(f)
                for row in reader:
                    # Filled, verbose merged row
                    merged_row = {h: row.get(h, "") for h in headers}
                    merged_row.update(meta)
                    writer.writerow(merged_row)

                    # Normalized row
                    normalized_row = build_normalized_row(row, meta)
                    norm_writer.writerow(normalized_row)


def main():
    repo_root = Path(__file__).resolve().parents[1]
    files = find_csv_files(repo_root)
    if not files:
        print("ERROR: No CSV files found to merge.", file=sys.stderr)
        sys.exit(2)
    headers = gather_headers(files)
    if not headers:
        print("ERROR: Could not detect headers in CSV files.", file=sys.stderr)
        sys.exit(3)
    out_path = repo_root / "Dataset" / "SPL_raw.csv"
    normalized_out_path = repo_root / "Dataset" / "SPL_raw_normalized.csv"
    normalized_headers = [
        "match_id",
        "date",
        "time",
        "home_team",
        "away_team",
        "home_score",
        "away_score",
        "stadium",
        "city",
        "round",
        "referee_name",
        "attendance",
        "season_label",
        "season_start_year",
        "season_end_year",
        "stage",
        "source_file",
    ]
    merge(files, out_path, headers, normalized_out_path, normalized_headers)
    print(f"Merged {len(files)} files into {out_path}")
    print(f"Normalized dataset written to {normalized_out_path}")


if __name__ == "__main__":
    main()
