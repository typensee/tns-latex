from pathlib import Path

from .gather import copyfromto, emptydir


def build_rollout_proj_code(
    tmpdir,
    rolloutdir
):
    destdir = rolloutdir / "code"

    emptydir(destdir)

    for srcfile in tmpdir.glob("*"):
        if (
            not srcfile.is_file()
            or
            srcfile.name[0] == '.'
            or
            srcfile.suffix == ".tex"
        ):
            continue

        print(f"+ Copying {srcfile.name}.")

        copyfromto(srcfile, destdir / srcfile.name)


def build_rollout_proj_doc_main(
    patterns,
    tmpdir,
    rolloutdir,
    manual_dir
):
    emptydir(rolloutdir / "doc")

    for texfile in tmpdir.glob("*.tex"):
        if texfile.name[0] == '.':
            continue

        lang = texfile.stem.split('-')[1]

        destfile = rolloutdir / "doc" / texfile.name

        if destfile.is_file():
            destfile.unlink()

        destfile.touch()

        print(f"+ Analyzing {destfile.name}.")

        resources = {}

        with (
            destfile.open("w") as f_out,
            texfile.open("r") as f_in
        ):
            for line in f_in:
                newline = line

                for p in patterns:
                    match = p.findall(line)

                    if not match:
                        continue

                    start, comment, macroname, options, input_file, end = match[0]

                    if input_file == '#1':
                        continue

                    if comment:
                        continue

                    for old in "./":
                        input_file_cleaned = input_file.replace(old, '-')


                    newline = f"{start}{macroname}{options}{{{input_file_cleaned}}}{end}\n"

                    if not input_file in resources:
                        resources[input_file] = input_file_cleaned

                    break

                f_out.write(newline)

        headcontents = []

        if resources:
            headcontents.append(
"""
% -------------------- %
% -- RESOURCES USED -- %
% -------------------- %
"""
                )


        if lang == "fr":
            rdir = tmpdir

        else:
            rdir = manual_dir / lang


        for rfile, rname in resources.items():
            if lang == "fr":
                rfiledir = rdir

            else:
                rfiledir = rdir / Path(rfile).parent.name

            with (rfiledir / rfile).open("r") as f:
                headcontents.append(
f"""
\\begin{{filecontents*}}[overwrite]{{{rname}}}
{f.read().strip()}
\\end{{filecontents*}}
"""
                )

        headcontents = "\n".join(headcontents)

        if headcontents:
            headcontents += """

% ------------------------ %
% -- SOURCE FOR THE DOC -- %
% ------------------------ %

"""

        finaltex = headcontents + destfile.read_text()

        destfile.write_text(data = finaltex)
