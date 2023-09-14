import os
import subprocess
import argparse

# Settings
PROJECT = "doc"
TEX = f"{PROJECT}.tex"
PDF = f"{PROJECT}.pdf"
DOCX = f"{PROJECT}.docx"
ALLTEX = [f for f in os.listdir() if f.endswith('.tex')]
AUX = [tex.replace('.tex', '.aux') for tex in ALLTEX]
PROJ_TEMP = [f"{PROJECT}.bbl", f"{PROJECT}.blg", f"{PROJECT}-blx.bib", f"{PROJECT}.lof", f"{PROJECT}.log",
             f"{PROJECT}.out", f"{PROJECT}.run.xml", f"{PROJECT}.toc"]

BIBTOOL = "bibtex"
PDFVIEWER = "okular"


def generate_pdf():
    clean()  # Cleaning before generating the PDF
    subprocess.run(["pdflatex", PROJECT])
    subprocess.run([BIBTOOL, PROJECT])
    subprocess.run(["pdflatex", PROJECT])
    subprocess.run(["pdflatex", PROJECT])


def generate_docx():
    subprocess.run(["pandoc", "-s", TEX, "-o", DOCX])
    fix_umlaute()


def fix_umlaute():
    subprocess.run(["./helpers/fix_umlaute.sh"])


def clean():
    for file in AUX + PROJ_TEMP + [PDF, DOCX]:
        try:
            os.remove(file)
        except FileNotFoundError:
            pass


def view():
    subprocess.run([PDFVIEWER, PDF])


def create_zip():
    subprocess.run(["git", "archive", "master", "--format", "zip", "--output", "efsdoc.zip"])


def main():
    parser = argparse.ArgumentParser(description='Manage your LaTeX project.')
    parser.add_argument('-pdf', '--generate-pdf', action='store_true', help='Generate PDF from .tex files.')
    parser.add_argument('-docx', '--generate-docx', action='store_true', help='Generate DOCX from .tex files.')
    parser.add_argument('-clean', '--clean', action='store_true', help='Clean auxiliary files.')
    parser.add_argument('-view', '--view', action='store_true', help='View the PDF.')
    parser.add_argument('-zip', '--zip', action='store_true', help='Create a ZIP of the project.')

    args = parser.parse_args()

    if args.generate_pdf:
        generate_pdf()
    if args.generate_docx:
        generate_docx()
    if args.clean:
        clean()
    if args.view:
        view()
    if args.zip:
        create_zip()


if __name__ == '__main__':
    main()
