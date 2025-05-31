#!/usr/bin/env python3
"""
GhostKit Banner Generator
Generates cybersecurity-themed banner images for documentation
"""

import os
import random
import sys

from PIL import Image, ImageDraw, ImageFilter, ImageFont

# Configuration
OUTPUT_DIR = "docs/assets/images"
WIDTH = 1200
HEIGHT = 200
BG_COLOR = (10, 10, 10)
TEXT_COLOR = (0, 255, 0)
ACCENT_COLOR = (120, 0, 255)
SECONDARY_COLOR = (0, 180, 255)

# Banner definitions - file_name -> title
BANNERS = {
    "architecture-banner.png": "ARCHITECTURE",
    "quickstart-banner.png": "QUICKSTART",
    "web-scanner-banner.png": "WEB SCANNER",
    "opsec-banner.png": "OPERATIONAL SECURITY",
    "mitre-banner.png": "MITRE ATT&CK MAPPING",
    "threat-intel-banner.png": "THREAT INTELLIGENCE",
    "api-banner.png": "API REFERENCE",
    "exploitation-banner.png": "EXPLOITATION TECHNIQUES",
    "legal-banner.png": "SECURITY ADVISORIES",
    "contribution-banner.png": "CONTRIBUTION GUIDE",
    "plugin-banner.png": "PLUGIN DEVELOPMENT",
    "overview-banner.png": "GHOSTKIT OVERVIEW",
    "ghostkit-banner.png": "GHOSTKIT FRAMEWORK",
}


def create_matrix_effect(draw, width, height):
    """Create a Matrix-style digital rain effect"""
    chars = "01GHO5TK1+*><)(?/\\"
    font = ImageFont.truetype("arial.ttf", 14)

    for i in range(0, width, 15):
        char_count = random.randint(5, 30)
        y_start = random.randint(-100, 100)

        for j in range(char_count):
            y_pos = y_start + j * 15
            if 0 <= y_pos < height:
                char = random.choice(chars)
                opacity = int(255 * (1 - j / char_count) * 0.7)
                color = (0, min(255, random.randint(180, 255)), 0, opacity)
                draw.text((i, y_pos), char, fill=color, font=font)


def draw_circuit_lines(draw, width, height):
    """Draw circuit-board style lines"""
    for _ in range(20):
        x1 = random.randint(0, width)
        y1 = random.randint(0, height)
        length = random.randint(50, 150)
        direction = random.choice([(1, 0), (0, 1), (1, 1), (-1, 1)])

        x2 = x1 + direction[0] * length
        y2 = y1 + direction[1] * length

        # Random color from our palette
        color = random.choice(
            [
                (ACCENT_COLOR[0], ACCENT_COLOR[1], ACCENT_COLOR[2], 150),
                (SECONDARY_COLOR[0], SECONDARY_COLOR[1], SECONDARY_COLOR[2], 150),
                (TEXT_COLOR[0], TEXT_COLOR[1], TEXT_COLOR[2], 100),
            ]
        )

        width = random.randint(1, 3)
        draw.line([(x1, y1), (x2, y2)], fill=color, width=width)


def create_banner(filename, title):
    """Create a cybersecurity-themed banner with title"""
    img = Image.new("RGBA", (WIDTH, HEIGHT), BG_COLOR + (255,))
    draw = ImageDraw.Draw(img)

    # Add matrix digital rain effect
    create_matrix_effect(draw, WIDTH, HEIGHT)

    # Add circuit lines
    draw_circuit_lines(draw, WIDTH, HEIGHT)

    # Apply slight blur
    img = img.filter(ImageFilter.GaussianBlur(radius=1))
    draw = ImageDraw.Draw(img)

    # Add title text
    try:
        title_font = ImageFont.truetype("arial.ttf", 48)
    except IOError:
        title_font = ImageFont.load_default()

    # Text shadow
    shadow_offset = 2
    draw.text(
        (WIDTH // 2 - shadow_offset, HEIGHT // 2 - shadow_offset),
        title,
        fill=(0, 0, 0, 180),
        font=title_font,
        anchor="mm",
    )

    # Main text
    draw.text(
        (WIDTH // 2, HEIGHT // 2),
        title,
        fill=(220, 220, 220, 255),
        font=title_font,
        anchor="mm",
    )

    # Add "GhostKit" watermark
    try:
        small_font = ImageFont.truetype("arial.ttf", 14)
    except IOError:
        small_font = ImageFont.load_default()

    draw.text(
        (WIDTH - 10, HEIGHT - 10),
        "GhostKit",
        fill=(200, 200, 200, 128),
        font=small_font,
        anchor="rb",
    )

    # Save the image
    output_path = os.path.join(OUTPUT_DIR, filename)
    img.save(output_path)
    print(f"Created banner: {output_path}")


def main():
    """Main function to generate all banners"""
    print(f"Generating {len(BANNERS)} banner images...")

    # Create output directory if it doesn't exist
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Generate each banner
    for filename, title in BANNERS.items():
        create_banner(filename, title)

    print("Banner generation complete!")


if __name__ == "__main__":
    main()
