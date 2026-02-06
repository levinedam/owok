# This file is part of NeuraSelf-UwU.
# Copyright (c) 2025-Present Routo
#
# NeuraSelf-UwU is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# You should have received a copy of the GNU General Public License
# along with NeuraSelf-UwU. If not, see <https://www.gnu.org/licenses/>.

import glob
import os
import numpy as np
from PIL import Image
import io

async def solveHbCaptcha(captcha_url, session):
    checks = []
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    corpus_dir = os.path.join(base_dir, "corpus")

    check_images = glob.glob(os.path.join(corpus_dir, "**", "*.png"), recursive=True)
    
    if not check_images:
        print(f"Warning: No corpus images found in {corpus_dir}")
        return ""
    for check_image in sorted(check_images):
        try:
            img = Image.open(check_image)
        
            
            checks.append((img, img.size, os.path.basename(check_image).split(".")[0]))
        except Exception as e:
            print(f"Error loading corpus image {check_image}: {e}")

    try:
        async with session.get(captcha_url) as resp:
            if resp.status == 200: 
                data = await resp.read()
                large_image = Image.open(io.BytesIO(data))
                large_array = np.array(large_image)
            else:
                print(f"Failed to fetch captcha: Status {resp.status}")
                return ""

    except Exception as e:
        print(f"Error fetching/processing captcha: {e}")
        return ""

    matches = []
    for img, (small_w, small_h), letter in checks:
        try:
            small_array = np.array(img)
            if small_array.shape[2] == 4:
                mask = small_array[:, :, 3] > 0
            else:
                mask = np.ones((small_h, small_w), dtype=bool)

            for y in range(large_array.shape[0] - small_h + 1):
                for x in range(large_array.shape[1] - small_w + 1):
                    segment = large_array[y : y + small_h, x : x + small_w]
                    
                    if segment.shape != small_array.shape:
                        continue

                    if np.array_equal(segment[mask], small_array[mask]):
                        if not any(
                            (m[0] - small_w < x < m[0] + small_w)
                            and (m[1] - small_h < y < m[1] + small_h)
                            for m in matches
                        ):
                            matches.append((x, y, letter))
        except Exception as e:
            continue
            
    matches = sorted(matches, key=lambda tup: tup[0])
    return "".join([i[2] for i in matches])
