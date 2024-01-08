import argparse
import logging
from datetime import datetime as dt
from pathlib import Path

logger = logging.getLogger()
logger.setLevel(logging.INFO)

DATE_FORMAT = '%Y-%m-%d'
POST_DIR = Path("_posts/")
DEFAULT_FRONT_MATTER = """---
layout: single
title: ""
excerpt: ""
type: post
header:
    overlay_color: "#333"
classes: wide
published: false
---"""


def get_post_name():
    parser = argparse.ArgumentParser()
    parser.add_argument('--name', help='post name', required=True)
    args = parser.parse_args()
    
    return args.name.lower().replace(" ","-")

def get_post_date():
    return dt.now().strftime(DATE_FORMAT)
    
def create_post_file(date, name):
    post_name = date + "-" + name + ".md"
    file_path = POST_DIR.joinpath(post_name)
    if POST_DIR.is_dir():
        if not file_path.is_file():
            with open(file_path, "w") as file:
                file.write(DEFAULT_FRONT_MATTER)
            logger.info("[create_post_file] New post created")
        else:
            logger.error("[create_post_file] File is already created")
    else: 
        logger.error("[create_post_file] Post dir does not exists")

def run():
    name = get_post_name()
    date = get_post_date()
    create_post_file(date, name)

if __name__ == "__main__":
    run()
