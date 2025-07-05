import re
from pathlib import Path
from typing import List, Tuple


def parse_table_row(line: str) -> Tuple[str, str]:
    """Parse a table row and return the anime name and full row."""
    anime_name = line.split("|")[0].strip().lower()
    return anime_name, line


def sort_table(input_path: Path, output_path: Path) -> None:
    """Sort anime tables in markdown file while preserving structure."""
    # Compile regex patterns once
    patterns = {
        "table_header": re.compile(
            r"^Nama Anime \| Native Resolution\(s\)/Kernel \| Descale\(\?\) \| Komparasi \| Catatan"
        ),
        "table_divider": re.compile(r"^-+ \| -+ \| -+ \| -+ \| -+"),
        "section_header": re.compile(r"^### .+"),
    }

    try:
        with open(input_path, "r", encoding="utf-8") as file:
            lines = file.readlines()
    except FileNotFoundError:
        print(f"Error: Input file {input_path} not found")
        return
    except Exception as e:
        print(f"Error reading file: {e}")
        return

    sorted_lines: List[str] = []
    table_rows: List[str] = []
    inside_table = False

    for line in lines:
        if patterns["section_header"].match(line):
            if inside_table:
                # Sort and append current table before new section
                table_rows.sort(key=lambda x: parse_table_row(x)[0])
                sorted_lines.extend(table_rows)
                table_rows = []
                inside_table = False
            sorted_lines.append(line)

        elif patterns["table_header"].match(line):
            inside_table = True
            sorted_lines.append(line)

        elif patterns["table_divider"].match(line):
            sorted_lines.append(line)

        elif inside_table:
            if not line.strip():
                # End of table - sort and append rows
                table_rows.sort(key=lambda x: parse_table_row(x)[0])
                sorted_lines.extend(table_rows)
                sorted_lines.append(line)
                table_rows = []
                inside_table = False
            else:
                table_rows.append(line)

        else:
            sorted_lines.append(line)

    # Handle last table if exists
    if inside_table and table_rows:
        table_rows.sort(key=lambda x: parse_table_row(x)[0])
        sorted_lines.extend(table_rows)

    try:
        with open(output_path, "w", encoding="utf-8") as file:
            file.writelines(sorted_lines)
        print(f"Successfully sorted tables and saved to {output_path}")
    except Exception as e:
        print(f"Error writing file: {e}")


def main():
    input_file = Path("./docs/encoding/Tahu-Tentang-Native-res.md")
    output_file = Path("./docs/encoding/Tahu-Tentang-Native-res.md")
    sort_table(input_file, output_file)


if __name__ == "__main__":
    main()
