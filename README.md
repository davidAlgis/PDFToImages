# PDF Image Extractor

This Python script allows you to extract images from each page of a PDF file and save them in a specified folder with a given extension.

## Installation

Before running the script, you need to install the required Python libraries. You can install them using the provided `requirements.txt` file.

```bash
pip install -r requirements.txt
```

## Usage

To use this script, run it from the command line and specify the input PDF file, the output folder, and the desired image extension. For example, this command extracts images from `input.pdf` and saves them as JPEG files in the `output_folder`:

```bash
python main.py -i input.pdf -o output_folder -e .jpeg
```

## Options

- `-h`, `--help`: Display help information showing all command-line options.
- `-i`, `--input` <file>: Specify the PDF file to process. (__required__)
- `-o`, `--output` <folder>: Specify the folder where the extracted images will be saved. (__required__)
- `-e`, `--extension` <extension>: Specify the image file extension (e.g., `.jpeg`, `.png`). (default: `.png`)
