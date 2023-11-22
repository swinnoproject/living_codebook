import os

root = os.path.join(os.path.dirname(__file__), "parsed")

qmds = set(f for f in os.listdir(root) if f.endswith(".qmd"))
dirs = set(d for d in os.listdir(root) if "." not in d and d.islower())

for table_dir in dirs:
    qmd_path = os.path.join(root, table_dir + ".qmd")

    with open(qmd_path, "w", encoding="utf-8") as f:
        f.write("---\n")
        f.write(f"title: {table_dir.title()}\n")
        f.write(f"code-tools: true\n")
        f.write(f'description: "TABLE_DESCRIPTION"\n')
        f.write(f'old-name: "FIND"\n')
        f.write(f"name: {table_dir}\n")
        f.write(f"listing: \n")
        f.write(f"  id: fields\n")
        f.write(f"  contents: {table_dir}/*qmd\n")
        f.write(f"  type: table\n")
        f.write(f"  fields: [title, label, name, description]\n\n")
        f.write(f"---\n\n")
        f.write("# {{< meta title >}}\n\n")
        f.write(f"## Fields\n")
        f.write(":::{ #fields}\n")
        f.write(f":::\n")
