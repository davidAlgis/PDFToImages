import argparse
import os

import fitz  # PyMuPDF


def render_pdf_to_images(pdf_path, output_folder, extension):
    try:
        doc = fitz.open(pdf_path)
    except FileNotFoundError:
        print(f"Error: The file '{pdf_path}' was not found.")
        exit(1)
    except Exception as e:
        print(f"Error opening PDF: {e}")
        exit(1)

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Clean the extension string just in case
    if not extension.startswith("."):
        extension = "." + extension

    for page_num in range(len(doc)):
        page = doc[page_num]

        # Matrix sets the resolution. 4.0x zoom gives a beautiful, crisp 288 DPI output
        # perfect for capturing fine details like font edges and the silver strokes.
        zoom = 4.0
        mat = fitz.Matrix(zoom, zoom)
        pix = page.get_pixmap(matrix=mat)

        # Build output filename
        img_name = f"page_{page_num + 1}{extension}"
        img_path = os.path.join(output_folder, img_name)

        # Save the rendered image
        pix.save(img_path)
        print(f"Saved rendered page: {img_path}")


parser = argparse.ArgumentParser(
    description="Render pages of a PDF file into images"
)
parser.add_argument(
    "-i", "--input", type=str, required=True, help="The PDF file to process"
)
parser.add_argument(
    "-o",
    "--output",
    type=str,
    required=False,
    default=None,
    help="The folder to save the images (defaults to the input PDF folder)",
)
parser.add_argument(
    "-e",
    "--extension",
    type=str,
    default=".jpeg",
    help="The image file extension (default: .jpeg)",
)

args = parser.parse_args()

# If no output folder is supplied, default to the folder of the input PDF
if args.output is None:
    args.output = os.path.dirname(os.path.abspath(args.input))

render_pdf_to_images(args.input, args.output, args.extension)
print(f"Processing complete. Images saved to {args.output}")
