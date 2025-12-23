#!/usr/bin/env python3

import os
import sys
import yaml
import json
import uuid
import argparse

def generate_image(filename):
    with open(filename, "r", encoding="utf-8") as handle:
        content = yaml.safe_load(handle)

    image = {
        "version": content.get("version", "v0.0.0"),
        "repository": content.get("repository", "repository")
    }

    sys.stdout.write(f"image.version: [{image['version']}]\n")
    sys.stdout.write(f"image.repository: [{image['repository']}]\n")

    if os.getenv("GITHUB_OUTPUT"):
        delimiter = f"EOF-{uuid.uuid4()}"
        with open(os.getenv("GITHUB_OUTPUT"), "a", encoding="utf-8") as handle:
            handle.write(f"image<<{delimiter}\n")
            handle.write(f"{json.dumps(image)}\n")
            handle.write(f"{delimiter}\n")

    return image

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Generate image")
    parser.add_argument("--filename", dest="filename", default="image.yaml", help="image filename")
    arguments = parser.parse_args()

    try:
        generate_image(filename=arguments.filename)
    except Exception as err:
        sys.stderr.write(f"Unable to generate image: {err}\n")
        sys.exit(1)

    sys.exit(0)
