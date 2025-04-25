from pathlib import Path

THIS_DIR = Path(__file__).parent


for texfile in THIS_DIR.glob("*-std.tex"):
    print(f"Working on << {texfile.name} >>")

    content = []

    for oneline in texfile.read_text().splitlines():
        if (
            not oneline
            or
            oneline[0] == "%"
        ):
            continue

        content.append(oneline.strip())

    content = "".join(content)

    for new in "=;":
        for old in [
            f" {new}",
            f"{new} ",
        ]:
            while old in content:
                content = content.replace(old, new)

    name = texfile.stem[:-4]
    texfile = texfile.parent / f"{name}-monster.tex"
    texfile.write_text(content)
