#!/usr/bin/env python3
import json
import subprocess
from pathlib import Path

VOLUME_NAME = "/var/simple_django"
ENVIRONMENT_PATH = "/etc/simple_django/appconfig.env"


def get_image_id():
    result = subprocess.run(
        [
            "docker",
            "image",
            "ls",
            "--format",
            "json",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    output = result.stdout.decode("utf-8")
    data = json.loads(output)
    return data[0]["ID"] if data else None


def main():
    for path in Path("/var/docker-exports").iterdir():
        image_name, image_tag = path.stem.rstrip("__").split("__")
        load_result = subprocess.run(
            ["docker", "image", "load", "-i", str(path)],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        output = load_result.stdout.decode("utf-8")
        if load_result.returncode != 0:
            raise Exception(output)
        image_id = get_image_id()
        if image_id is None:
            raise Exception("No image ID found after loading the image.")
        subprocess.run(
            ["docker", "image", "tag", image_id, f"{image_name}:{image_tag}"]
        )
        subprocess.run(["docker", "image", "tag", image_id, f"{image_name}:latest"])

        subprocess.run(["docker", "compose", "-f", "/root/compose.yml", "down"])
        subprocess.run(["docker", "compose", "-f", "/root/compose.yml", "rm"])
        subprocess.run(["docker", "compose", "-f", "/root/compose.yml", "up", "-d"])

        path.unlink()


if __name__ == "__main__":
    main()
