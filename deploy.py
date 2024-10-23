#!/usr/bin/env python
import re
import subprocess
from argparse import ArgumentParser
from datetime import datetime
from pathlib import Path
from tempfile import TemporaryDirectory

import tomllib
from zoneinfo import ZoneInfo


def build_image(tag):
    result = subprocess.run(
        [
            "docker",
            "image",
            "build",
            "--tag",
            f"simple_django:{tag}",
            "--tag",
            "simple_django:latest",
            Path.cwd(),
        ],
        capture_output=True,
    )
    output = result.stderr.decode("utf-8")
    if result.returncode != 0:
        raise Exception(output)
    return output


def get_image_id(build_result):
    pattern = re.compile(r".+writing image.+")
    found = pattern.findall(build_result)[0]
    return found.split("sha256:")[1].split(" ")[0]


def main(upload=False):
    now = datetime.now(tz=ZoneInfo("UTC"))
    image_tag = now.strftime("%Y%m%dT%H%M")
    result = build_image(image_tag)
    if upload:
        image_id = get_image_id(result)
        with TemporaryDirectory() as tmp_dir:
            archive_name = f"simple_django__{image_tag}.tar"
            archive_path = Path(tmp_dir) / archive_name
            save_result = subprocess.run(
                [
                    "docker",
                    "image",
                    "save",
                    "-o",
                    str(archive_path),
                    image_id,
                ],
                capture_output=True,
            )
            if save_result.returncode != 0:
                raise Exception(save_result.stderr.decode("utf-8"))
            with open("image_builder.toml", "rb") as fp:
                config = tomllib.load(fp)
                remote_user = config["remote_user"]
                remote_path = Path(config["remote_directory"]) / archive_name
                for server in config["servers"]:
                    subprocess.run(
                        [
                            "rsync",
                            "-Pasvz",
                            str(archive_path),
                            f"{remote_user}@{server}:{str(remote_path)}",
                        ]
                    )


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-u", "--upload", action="store_true", default=False)
    args = parser.parse_args()
    main(args.upload)
