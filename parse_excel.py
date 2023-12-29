import pandas as pd
import os
import re


def string_cleaner(string):
    if type(string) != str:
        return string
    return re.sub(
        r"\s+",
        " ",
        re.sub(r"[:=]", " ", re.sub(r"[^\s\w]", " ", string.replace("_x000B_", " "))),
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
        desc = string_cleaner(desc)

        var_path = os.path.join(root_dir, writable_field)
        with open(var_path + ".qmd", "w", encoding="utf8") as f:
            f.write("---\n")
            f.write(f'title: "{writable_field}"\n')
            f.write("code-tools: true\n")
            f.write("old-name: LOOKUP\n")
            f.write("name: REPLACE\n")
            f.write("sort-order: 0\n")
            f.write(f'description: "{desc.replace(":", "")}"\n')

            if str(code_list).strip() in ("nan", "-", ""):
                f.write("---")

            # if str(code_list) not in('nan', '-'):
            else:
                ## add tabulation

                f.write("listing:\n")
                f.write("  id: Codes\n")
                f.write(f"  contents: {writable_field}.yaml" + "\n")
                f.write("  type: table\n")
                f.write("  fields: [title, label, code, description]\n")
                f.write("  sort-ui: false\n")
                f.write("  sort:\n")
                f.write("    - sort-order\n")
                f.write("    - code\n")
                f.write("    - title\n")
                f.write("---\n\n")
                f.write(":::{ #Codes }\n")
                f.write(":::\n")

                code_yaml_path = os.path.join(var_path + ".yaml")
                with open(code_yaml_path, "w", encoding="utf8") as y:
                    for val_idx, grouping, code, value, val_desc in values[
                        values["Code list"] == code_list
                    ].itertuples():
                        # print(code,'|', value,'|', val_desc)
                        code = string_cleaner(code)

                        y.write(f'\n- title: "{value.replace(":", "")}"\n')
                        y.write(f'  label: "{value.replace(":", "")}"\n')
                        y.write("  code-tools: true\n")
                        y.write("  sort-order: 0\n")
                        y.write(f'  description: "{val_desc.replace(":", "")}"\n')
                        y.write("  old_codes: [REPLACE, REPLACE]\n")
                        y.write(f"  code: {code}\n")
