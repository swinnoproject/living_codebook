import pandas as pd
import os

if __name__ == "__main__":
    variables = pd.read_excel(
        os.path.join(
            "..", "parsing_export", "data", "20230309 SWINNO 1908-1969 1970-2021.xlsx"
        ),
        sheet_name="Variables in table format",
        engine="openpyxl",
    )

    values = pd.read_excel(
        os.path.join(
            "..", "parsing_export", "data", "20230309 SWINNO 1908-1969 1970-2021.xlsx"
        ),
        sheet_name="Codes in table format",
        engine="openpyxl",
    )

    root_dir = "parsed"
    os.makedirs(root_dir, exist_ok=True)
    for var_idx, field, desc, dtype, code_list, *_ in variables.itertuples():
        if str(field) == "nan":
            continue
        writable_field = field.replace("=", "").replace(" ", "_").replace(":", "")

        var_path = os.path.join(root_dir, writable_field)
        with open(var_path + ".qmd", "w", encoding="utf8") as f:
            f.write(
                f"""---
Title: "{writable_field}"
code-tools: true
old-name: LOOKUP
new-name: REPLACE
table-nr: LOOKUP
description: "{desc.replace(':', '')}"

    """.replace(
                    "=", ""
                )
                .replace("[", "")
                .replace("]", "")
            )

            if str(code_list) in ("nan", "-"):
                f.write("---")

            # if str(code_list) not in('nan', '-'):
            else:
                ## add tabulation

                f.write(
                    f"""listing:
id: fields
contents: {writable_field}/*qmd
type: table
fields: [title, label, code, description]
---
"""
                )
                f.write(
                    """

## Fields
:::{ #fields }
:::
"""
                )

                os.makedirs(var_path, exist_ok=True)
                for val_idx, grouping, code, value, val_desc in values[
                    values["Code list"] == code_list
                ].itertuples():
                    # print(code,'|', value,'|', val_desc)
                    val_path = os.path.join(
                        var_path,
                        str(val_idx).zfill(3)
                        + "_"
                        + value.replace(" ", "_").replace("/", ".")
                        + ".qmd",
                    )
                    with open(val_path, "w", encoding="utf8") as val_f:
                        val_f.write(
                            f"""---
title: "{value.replace(':', '')}"
label: "{value.replace(':', '')}"
code-tools: true
description: "{val_desc.replace(':', '')}"
old_codes: REPLACE
code: {code}
---

    """.replace(
                                "=", ""
                            )
                            .replace("[", "")
                            .replace("]", "")
                        )
