# tlescraper\htmlrender.py
import os
from jinja2 import Environment, FileSystemLoader


def search_files(rootDir="."):
    """Searches for files in a directory recursively"""
    files = []

    for dirName, subdirList, fileList in os.walk(rootDir):
        for fname in fileList:
            files.append(
                os.path.relpath(os.path.join(dirName, fname), rootDir).replace(
                    "\\", "/"
                )
            )
    return files


def render_files(template_filename, output_filename, **kwargs):
    """Renders a template file and saves it to a file"""
    template = Environment(
        loader=FileSystemLoader(os.path.dirname(template_filename))
    ).get_template(os.path.basename(template_filename))

    output = template.render(**kwargs)

    if not os.path.exists(os.path.dirname(output_filename)):
        os.makedirs(os.path.dirname(output_filename))
    with open(output_filename, "w") as f:
        f.write(output)

    return output


def generate_index_html(rootDir="."):
    """Generates an index.html file for a directory"""
    files = search_files(rootDir)
    output = render_files(
        "templates/index.html.j2",
        os.path.join(rootDir, "index.html").replace("\\", "/"),
        files=files,
    )
    return output
