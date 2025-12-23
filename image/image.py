#!/usr/bin/env python3

import os
import sys
import yaml
import json
import uuid
import argparse

def image_operation(filename, mode):
    if mode == "fetch":
        return image_fetch(filename)
    else:
        return image_update(filename)

def image_fetch(filename):
    with open(filename, "r", encoding="utf-8") as handle:
        content = yaml.safe_load(handle)

    sys.stdout.write(f"content.repository: [{content['repository']}]\n")
    sys.stdout.write(f"content.version: [{content['version']}]\n")
    sys.stdout.write(f"content.release: [{content['release']}]\n")

    if os.getenv("GITHUB_OUTPUT"):
        delimiter = f"EOF-{uuid.uuid4()}"
        with open(os.getenv("GITHUB_OUTPUT"), "a", encoding="utf-8") as handle:
            handle.write(f"image<<{delimiter}\n")
            handle.write(f"{json.dumps(content)}\n")
            handle.write(f"{delimiter}\n")

    return content

def image_update(filename):
    with open(filename, "r", encoding="utf-8") as handle:
        content = yaml.safe_load(handle)

    elements = content["version"].split(".")

    if content["release"] == "major":
        elements[0] = elements[0] + 1
    if content["release"] == "minor":
        elements[1] = elements[1] + 1
    if content["release"] == "patch":
        elements[2] = elements[2] + 1

    content["version"] = ".".join(elements)

    sys.stdout.write(f"content.repository: [{content['repository']}]\n")
    sys.stdout.write(f"content.version: [{content['version']}]\n")
    sys.stdout.write(f"content.release: [{content['release']}]\n")

    with open(filename, "w") as handle:
        yaml.dump(content, handle)

    return content

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Generate image")
    parser.add_argument("--filename", dest="filename", default="image.yaml", help="image filename")
    parser.add_argument("--mode", dest="mode", default="fetch", help="operation mode")
    arguments = parser.parse_args()

    try:
        image_operation(filename=arguments.filename, mode=arguments.mode.lower())
    except Exception as err:
        sys.stderr.write(f"Unable to {arguments.mode} image: {err}\n")
        sys.exit(1)

    sys.exit(0)
