#!/usr/bin/env python3

import os
import sys
import yaml
import argparse

def generate_image_version(filename):
    with open(filename, "r", encoding="utf-8") as handle:
        infrastructure = yaml.safe_load(handle)

    image_version = infrastructure.get("version", "v0.0.0")

    sys.stdout.write(f"image_version: [{image_version}]\n")

    if os.getenv("GITHUB_OUTPUT"):
        with open(os.getenv("GITHUB_OUTPUT"), "a", encoding="utf-8") as handle:
            handle.write(f"image_version: '{image_version}'\n")

    return image_version

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Generate image version")
    parser.add_argument("--filename", dest="filename", default="image.yaml", help="image filename")
    arguments = parser.parse_args()

    try:
        generate_image_version(filename=arguments.filename)
    except Exception as err:
        sys.stderr.write(f"Unable to generate image version: {err}\n")
        sys.exit(1)

    sys.exit(0)
