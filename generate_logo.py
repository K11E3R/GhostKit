#!/usr/bin/env python3
"""
GhostKit Logo Generator
Creates a professional cybersecurity-themed logo for the GhostKit toolkit
"""

import os

from PIL import Image, ImageDraw, ImageFilter, ImageFont

# Configuration
OUTPUT_DIR = "docs/assets/images"
SIZE = (512, 512)
BG_COLOR = (20, 20, 20, 255)
PRIMARY_COLOR = (0, 255, 0, 255)  # Matrix green
ACCENT_COLOR = (128, 0, 255, 255)  # Purple accent


def create_ghost_logo():
    """Create the GhostKit logo with a ghost silhouette and circuit board elements"""
    # Create base image with transparent background
    img = Image.new("RGBA", SIZE, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Create circular background
    center = (SIZE[0] // 2, SIZE[1] // 2)
    radius = min(SIZE) // 2 - 10

    # Draw filled circle with dark background
    draw.ellipse(
        (
            center[0] - radius,
            center[1] - radius,
            center[0] + radius,
            center[1] + radius,
        ),
        fill=BG_COLOR,
    )

    # Draw ghost silhouette
    ghost_width = radius * 1.2
    ghost_height = radius * 1.5
    ghost_top = center[1] - ghost_height // 2 + 20  # Adjust position

    # Ghost head (rounded rectangle)
    head_radius = ghost_width // 4
    ghost_body_points = [
        # Top rounded part
        (center[0] - ghost_width // 2 + head_radius, ghost_top),
        (center[0] + ghost_width // 2 - head_radius, ghost_top),
        # Right side
        (center[0] + ghost_width // 2, ghost_top + head_radius),
        (center[0] + ghost_width // 2, ghost_top + ghost_height - head_radius),
        # Bottom zigzag (3 points for ghost-like bottom)
        (center[0] + ghost_width // 3, ghost_top + ghost_height),
        (center[0], ghost_top + ghost_height - head_radius),
        (center[0] - ghost_width // 3, ghost_top + ghost_height),
        # Left side
        (center[0] - ghost_width // 2, ghost_top + ghost_height - head_radius),
        (center[0] - ghost_width // 2, ghost_top + head_radius),
    ]

    # Draw ghost body
    draw.polygon(ghost_body_points, fill=PRIMARY_COLOR)

    # Add ghost eyes (two small circles)
    eye_radius = ghost_width // 12
    eye_y = ghost_top + ghost_height // 4
    eye_spacing = ghost_width // 4

    # Left eye
    draw.ellipse(
        (
            center[0] - eye_spacing - eye_radius,
            eye_y - eye_radius,
            center[0] - eye_spacing + eye_radius,
            eye_y + eye_radius,
        ),
        fill=BG_COLOR,
    )

    # Right eye
    draw.ellipse(
        (
            center[0] + eye_spacing - eye_radius,
            eye_y - eye_radius,
            center[0] + eye_spacing + eye_radius,
            eye_y + eye_radius,
        ),
        fill=BG_COLOR,
    )

    # Add circuit board traces
    for i in range(5):
        # Horizontal traces
        y = ghost_top + ghost_height + 10 + i * 15
        if y < SIZE[1] - 20:
            line_start = center[0] - radius + 30
            line_end = center[0] + radius - 30
            draw.line([(line_start, y), (line_end, y)], fill=ACCENT_COLOR, width=3)

            # Add small connecting verticals
            if i % 2 == 0 and i > 0:
                vert_x = line_start + (line_end - line_start) * (i / 5)
                draw.line([(vert_x, y), (vert_x, y - 15)], fill=ACCENT_COLOR, width=3)

    # Add outer glow effect
    glowing = img.copy()
    glowing = glowing.filter(ImageFilter.GaussianBlur(radius=5))
    glowing_draw = ImageDraw.Draw(glowing)

    # Merge the glowing layer beneath the original
    result = Image.new("RGBA", SIZE, (0, 0, 0, 0))
    result.paste(glowing, (0, 0), glowing)
    result.alpha_composite(img)

    # Add text "GHOSTKIT" at the bottom
    try:
        font = ImageFont.truetype("arial.ttf", 40)
    except IOError:
        font = ImageFont.load_default()

    # Add "GHOSTKIT" text
    text_y = center[1] + radius - 60
    draw = ImageDraw.Draw(result)

    # Draw text shadow
    draw.text(
        (center[0] + 2, text_y + 2),
        "GHOSTKIT",
        fill=(0, 0, 0, 200),
        font=font,
        anchor="ms",
    )

    # Draw main text
    draw.text(
        (center[0], text_y), "GHOSTKIT", fill=PRIMARY_COLOR, font=font, anchor="ms"
    )

    # Save as PNG with transparency
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    result.save(os.path.join(OUTPUT_DIR, "ghostkit-logo.png"))
    print(f"Logo created at {OUTPUT_DIR}/ghostkit-logo.png")


if __name__ == "__main__":
    create_ghost_logo()
