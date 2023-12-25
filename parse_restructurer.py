"""
While manually restructurng the codebook files I noticed that
some fields, such as the ones relating to patents, are not
included in the excel export ...

This script is an approach towards remedying this issue by
parsing the hard-coded relationships from the export-script

The idea is to simply paste the lines, and create new .qmd files
in the appropriate directory.
"""

import os
import re

target = re.compile(r'"[^"]+"')


innovaton = """
content_row["pat_applied"] = row["a_patent_application_exists"]
content_row["pat_firm_applying"] = row["firm_applying_for_patent"]
content_row["pat_pers_applying"] = row["person_applying_for_patent"]
content_row["pat_assig_pers"] = row["patent_assigned_to_person"]
content_row["pat_granted"] = row["patent_granted"]
content_row["pat_swe"] = row["patent_granted_in_sweden"]
content_row["pat_epo"] = row["patent_granted_by_EPO"]
content_row["pat_uspto"] = row["patent_granted_by_USPTO"]
content_row["pat_jpo"] = row["patent_granted_by_JPO"]
content_row["pat_other"] = row["patent_granted_by_other_office"]

content_row["yr_export"] = row["start_year_of_export"]
content_row["export"] = row["export_has_started"]

"""


def generate_file_content(line, idx=0):
    new, old = target.findall(line)

    return (
        old.replace('"', ""),
        f"""---
title: {old}
code-tools: true
old-name: {old}
name {new}
sort-order: {idx}
description: REPLACE
---
""",
    )


def process_table(code_str, table_name, start_position):
    table_dir = os.path.join("from_code", table_name)
    os.makedirs(table_dir)
    for idx, line in enumerate(code_str.split("\n")):
        if len(line.strip()) == 0:
            continue
        name, content = generate_file_content(line, start_position + idx)

        qmd_path = os.path.join(table_dir, name + ".qmd")

        with open(qmd_path, "x", encoding="utf8") as f:
            f.write(content)


process_table(innovaton, "innovation", 20)
