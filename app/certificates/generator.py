from datetime import datetime, timezone
from pathlib import Path
import secrets

from reportlab.lib.colors import HexColor
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas


def render_description(
    description,
    name,
    college_name,
    certificate_number,
    date
):
    replacements = {
        "{name}": name,
        "{college_name}": college_name,
        "{certificate_number}": certificate_number,
        "{date}": date
    }

    for variable, value in replacements.items():
        description = description.replace(
            variable,
            value
        )

    return description


def generate_certificate_number(certificate_id):
    year = datetime.now(timezone.utc).year
    return f"CERT-{year}-{certificate_id:06d}"


def generate_public_token():
    return secrets.token_urlsafe(32)


BACKGROUND_PATH = (
    Path(__file__).resolve().parent.parent
    / "static"
    / "img"
    / "certificate-bg.png"
)

# Background design is 566 x 360 px. The page keeps the same aspect ratio
# so the design is never stretched.
BG_PX_WIDTH = 566
BG_PX_HEIGHT = 360
PAGE_WIDTH = 842.0
PAGE_HEIGHT = PAGE_WIDTH * BG_PX_HEIGHT / BG_PX_WIDTH

NAVY = HexColor("#0B3A6E")
GOLD = HexColor("#A8812A")
TEXT = HexColor("#2B3440")


def fit_font_size(text, font_name, max_size, max_width, min_size=14):
    size = max_size

    while size > min_size and stringWidth(text, font_name, size) > max_width:
        size -= 1

    return size


def wrap_text(text, font_name, font_size, max_width):
    lines = []

    for paragraph in text.splitlines() or [""]:
        current_line = ""

        for word in paragraph.split():
            test_line = f"{current_line} {word}".strip()

            if stringWidth(test_line, font_name, font_size) <= max_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)

                current_line = word

        if current_line:
            lines.append(current_line)

    return lines


def generate_pdf(
    title,
    description,
    name,
    college_name,
    certificate_number,
    output_path
):
    output_path = Path(output_path)
    output_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    pdf = canvas.Canvas(
        str(output_path),
        pagesize=(PAGE_WIDTH, PAGE_HEIGHT)
    )

    center_x = PAGE_WIDTH / 2
    content_width = PAGE_WIDTH - 300

    issue_date = datetime.now(timezone.utc).strftime("%d %B %Y")

    pdf.drawImage(
        str(BACKGROUND_PATH),
        0,
        0,
        width=PAGE_WIDTH,
        height=PAGE_HEIGHT,
        mask="auto"
    )

    # Company name
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawCentredString(
        center_x,
        PAGE_HEIGHT - 100,
        "GAMKERS"
    )

    # Title
    title_font = "Times-Bold"
    title_size = fit_font_size(title, title_font, 36, content_width)
    pdf.setFont(title_font, title_size)
    pdf.drawCentredString(
        center_x,
        PAGE_HEIGHT - 150,
        title
    )

    # Gold divider
    pdf.setStrokeColor(GOLD)
    pdf.setLineWidth(1.5)
    pdf.line(
        center_x - 90,
        PAGE_HEIGHT - 166,
        center_x + 90,
        PAGE_HEIGHT - 166
    )

    # Presented to
    pdf.setFillColor(TEXT)
    pdf.setFont("Helvetica-Oblique", 13)
    pdf.drawCentredString(
        center_x,
        PAGE_HEIGHT - 198,
        "This certificate is proudly presented to"
    )

    # Recipient name
    name_font = "Times-BoldItalic"
    name_size = fit_font_size(name, name_font, 38, content_width)
    pdf.setFillColor(NAVY)
    pdf.setFont(name_font, name_size)
    pdf.drawCentredString(
        center_x,
        PAGE_HEIGHT - 245,
        name
    )

    name_width = min(
        stringWidth(name, name_font, name_size) + 40,
        content_width
    )
    pdf.setStrokeColor(GOLD)
    pdf.setLineWidth(1)
    pdf.line(
        center_x - name_width / 2,
        PAGE_HEIGHT - 256,
        center_x + name_width / 2,
        PAGE_HEIGHT - 256
    )

    # College
    college_size = fit_font_size(
        college_name,
        "Helvetica-Bold",
        15,
        content_width,
        min_size=9
    )
    pdf.setFillColor(TEXT)
    pdf.setFont("Helvetica-Bold", college_size)
    pdf.drawCentredString(
        center_x,
        PAGE_HEIGHT - 282,
        college_name
    )

    # Description
    rendered_description = render_description(
        description,
        name,
        college_name,
        certificate_number,
        issue_date
    )

    pdf.setFont("Helvetica", 12)
    lines = wrap_text(
        rendered_description,
        "Helvetica",
        12,
        content_width
    )

    y = PAGE_HEIGHT - 315

    for line in lines[:5]:
        pdf.drawCentredString(center_x, y, line)
        y -= 19

    # Footer
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica", 10)
    pdf.drawString(
        72,
        PAGE_HEIGHT - 430,
        f"Certificate No: {certificate_number}"
    )
    pdf.drawString(
        72,
        PAGE_HEIGHT - 446,
        f"Date of Issue: {issue_date}"
    )

    pdf.save()
