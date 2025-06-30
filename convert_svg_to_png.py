#!/usr/bin/env python3
"""Convert SVG to PNG using the best available tool"""

import subprocess
import sys
import os

def convert_svg_to_png(svg_file='demo.svg', png_file='demo.png', width=800):
    """Convert SVG to PNG using available tools"""
    
    if not os.path.exists(svg_file):
        print(f"Error: {svg_file} not found")
        return False
    
    # Try different conversion methods in order of preference
    converters = [
        # Modern ImageMagick
        (['magick', svg_file, '-resize', f'{width}x', png_file], 'ImageMagick magick'),
        # Python cairosvg
        (None, 'cairosvg'),
        # rsvg-convert
        (['rsvg-convert', '-w', str(width), '-f', 'png', '-o', png_file, svg_file], 'rsvg-convert'),
        # Legacy ImageMagick
        (['convert', svg_file, '-resize', f'{width}x', png_file], 'ImageMagick convert (legacy)'),
    ]
    
    for cmd, name in converters:
        try:
            if name == 'cairosvg':
                # Try using cairosvg Python package
                import cairosvg
                cairosvg.svg2png(url=svg_file, write_to=png_file, output_width=width)
                print(f'PNG generated using {name}')
                return True
            else:
                # Try using command line tool
                subprocess.run(cmd, check=True, capture_output=True)
                print(f'PNG generated using {name}')
                return True
        except (subprocess.CalledProcessError, FileNotFoundError, ImportError) as e:
            continue
    
    print('No SVG to PNG converter found. Please install one of:')
    print('- pip install cairosvg')
    print('- brew install librsvg (for rsvg-convert)')
    print('- brew install imagemagick (for magick/convert)')
    return False

if __name__ == "__main__":
    success = convert_svg_to_png()
    if not success:
        sys.exit(1)
    else:
        print("Conversion completed successfully!")