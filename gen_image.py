import os
import sys
import textwrap

from PIL import Image, ImageDraw, ImageFont
from pypdftk import stamp
from wand.image import Image as wand_image


def generate_watermark(doc_size, text):
    img = Image.new("RGBA", doc_size, color=(255, 255, 255, 0))
    draw = ImageDraw.Draw(img)

    line_break = 15
    multiline_text = textwrap.wrap(text, width=15)
    fill_color = (255, 255, 255)
    shadow_color = (0, 0, 0)

    fontsize = 12
    font = ImageFont.truetype("arial.ttf", fontsize)

    # Initial position of text
    x = doc_size[0] - (line_break) * fontsize * 0.6
    y = doc_size[1] - (fontsize + 2) * len(multiline_text)

    line_position = 0
    for line in multiline_text:
        # thin border
        draw.text((x - 1, y + line_position), line, font=font, fill=shadow_color)
        draw.text((x + 1, y + line_position), line, font=font, fill=shadow_color)
        draw.text((x, y - 1 + line_position), line, font=font, fill=shadow_color)
        draw.text((x, y + 1 + line_position), line, font=font, fill=shadow_color)

        # thicker border
        draw.text((x - 1, y - 1 + line_position), line, font=font, fill=shadow_color)
        draw.text((x + 1, y - 1 + line_position), line, font=font, fill=shadow_color)
        draw.text((x - 1, y + 1 + line_position), line, font=font, fill=shadow_color)
        draw.text((x + 1, y + 1 + line_position), line, font=font, fill=shadow_color)

        # now draw the text over it
        draw.text((x, y + line_position), line, font=font, fill=fill_color)

        line_position += fontsize + 2

    img.save("watermark.png")

    with wand_image(filename="watermark.png") as watermark_img:
        watermark_img.format = "pdf"
        watermark_img.save(filename="watermark.pdf")
    os.remove("watermark.png")


def generate_watermarked_pdf(input_pdf_path, watermark_name):
    text = "PDF Generated for {}".format(watermark_name)
    output_pdf = "{}.pdf".format(watermark_name)

    with wand_image(filename=input_pdf_path) as input_pdf:
        generate_watermark(input_pdf.size, text)

    stamp(
        pdf_path=input_pdf_path,
        stamp_pdf_path="watermark.pdf",
        output_pdf_path=output_pdf,
    )
    os.remove("watermark.pdf")
    print("Generated {}".format(output_pdf))

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print ("You should give 2 args to this script. The name of the input pdf then the name to put in the watermark")
        sys.exit(1)
    generate_watermarked_pdf(sys.argv[1], sys.argv[2])
