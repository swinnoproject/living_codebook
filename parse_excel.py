import pandas as pd
import os
import re


def string_cleaner(string):
    return re.sub(
        r"\s+",
        "",
        re.sub(r"[:=]", " ", re.sub(r"[^\s\w]", "", string.replace("_x000B_", ""))),
    ).strip()


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

    values["Code list"] = values["Code list"].apply(lambda x: string_cleaner(x))

    root_dir = "parsed"
    os.makedirs(root_dir, exist_ok=True)
    for var_idx, field, desc, dtype, code_list, *_ in variables.itertuples():
        if str(field) == "nan":
            continue
        code_list = string_cleaner(code_list)
        writable_field = field.replace("=", "").replace(" ", "_").replace(":", "")

        var_path = os.path.join(root_dir, writable_field)
        with open(var_path + ".qmd", "w", encoding="utf8") as f:
            f.write("---\n")
            f.write(f'title: "{writable_field}"\n')
            f.write("code-tools: true\n")
            f.write("old-name: LOOKUP\n")
            f.write("new-name: REPLACE\n")
            f.write("table-nr: LOOKUP`\n")
            f.write(f'description: "{desc.replace(":", "")}"\n')

            if str(code_list).strip() in ("nan", "-", ""):
                f.write("---")

            # if str(code_list) not in('nan', '-'):
            else:
                ## add tabulation

                f.write("listing:\n")
                f.write("  id: fields\n")
                f.write(f"  contents: {writable_field}/*qmd" + "\n")
                f.write("  type: table\n")
                f.write("  fields: [title, label, code, description]\n")
                f.write("---\n\n")
                f.write("# {{< meta title >}}\\n\n")
                f.write("## Fields\n\n")
                f.write(":::{ #fields }\n")
                f.write(":::\n")

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
                        val_f.write("---\n")
                        val_f.write(f'title: "{value.replace(":", "")}"\n')
                        val_f.write(f'label: "{value.replace(":", "")}"\n')
                        val_f.write("code-tools: true\n")
                        val_f.write(f'description: "{val_desc.replace(":", "")}"\n')
                        val_f.write("old_codes: REPLACE\n")
                        val_f.write(f"code: {code}\n")
                        val_f.write("---\n")
