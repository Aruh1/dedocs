import re

def sort_table(file_path, output_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # Regex untuk mendeteksi header tabel
    table_header_pattern = re.compile(r"^Nama Anime \| Native Resolution\(s\)/Kernel \| Descale\(\?\) \| Komparasi \| Catatan")
    table_divider_pattern = re.compile(r"^-+ \| -+ \| -+ \| -+ \| -+")
    section_header_pattern = re.compile(r"^### .+")  # Untuk mendeteksi header seperti "### Summer 2024"

    sorted_lines = []
    inside_table = False
    table_rows = []
    section_header = None

    for line in lines:
        if section_header_pattern.match(line):
            # Simpan header section (misalnya "### Summer 2024")
            if inside_table:
                # Sort and append the current table before moving to the next section
                table_rows.sort(key=lambda x: x.split('|')[0].strip().lower())
                sorted_lines.extend(table_rows)
                table_rows = []
                inside_table = False
            section_header = line
            sorted_lines.append(line)
        elif table_header_pattern.match(line):
            inside_table = True
            sorted_lines.append(line)
        elif table_divider_pattern.match(line):
            sorted_lines.append(line)
        elif inside_table:
            if line.strip() == "":
                # Sort the table rows alphabetically by the first column (Nama Anime)
                table_rows.sort(key=lambda x: x.split('|')[0].strip().lower())
                sorted_lines.extend(table_rows)
                sorted_lines.append(line)
                table_rows = []
                inside_table = False
            else:
                table_rows.append(line)
        else:
            sorted_lines.append(line)

    # Pastikan tabel terakhir juga diurutkan
    if inside_table and table_rows:
        table_rows.sort(key=lambda x: x.split('|')[0].strip().lower())
        sorted_lines.extend(table_rows)

    # Write the sorted content to the output file
    with open(output_path, 'w', encoding='utf-8') as output_file:
        output_file.writelines(sorted_lines)

# Filepath input dan output
input_file = './docs/encoding/Tahu-Tentang-Native-res.md'
output_file = './docs/encoding/Tahu-Tentang-Native-res.md'

# Jalankan fungsi
sort_table(input_file, output_file)

print(f"Tabel berhasil diurutkan dan disimpan ke {output_file}")