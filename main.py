import argparse
from pypdf import PdfReader
from PIL import Image
import io
import os


def str2bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


def extract_images_from_pdf(pdf_path, output_folder, extension):
    try:
        reader = PdfReader(pdf_path)
    except FileNotFoundError:
        print(f"Error: The file '{pdf_path}' was not found.")
        exit(1)

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for page_num, page in enumerate(reader.pages):
        if '/XObject' in page['/Resources']:
            xObject = page['/Resources']['/XObject'].get_object()

            for obj in xObject:
                if xObject[obj]['/Subtype'] == '/Image':
                    size = (xObject[obj]['/Width'], xObject[obj]['/Height'])
                    data = xObject[obj].get_data()

                    if xObject[obj]['/ColorSpace'] == '/DeviceRGB':
                        mode = "RGB"
                    else:
                        mode = "P"

                    if '/Filter' in xObject[obj]:
                        if xObject[obj]['/Filter'] == '/FlateDecode':
                            img = Image.frombytes(mode, size, data)
                        elif xObject[obj]['/Filter'] == '/DCTDecode':
                            img = Image.open(io.BytesIO(data))
                        elif xObject[obj]['/Filter'] == '/JPXDecode':
                            img = Image.open(io.BytesIO(data))
                        else:
                            img = None
                    else:
                        img = Image.frombytes(mode, size, data)

                    if img:
                        img_path = os.path.join(
                            output_folder,
                            f"page_{page_num + 1}_{obj[1:]}{extension}")
                        img.save(img_path)
                        print(f"Saved image: {img_path}")


parser = argparse.ArgumentParser(
    description="Extract images from each page of a PDF file")
parser.add_argument('-i',
                    '--input',
                    type=str,
                    required=True,
                    help='The PDF file to process')
parser.add_argument('-o',
                    '--output',
                    type=str,
                    required=True,
                    help='The folder to save the extracted images')
parser.add_argument('-e',
                    '--extension',
                    type=str,
                    default='.png',
                    help='The image file extension (e.g., .jpeg, .png)')

args = parser.parse_args()

extract_images_from_pdf(args.input, args.output, args.extension)
print(f"Images extracted and saved to {args.output}")
