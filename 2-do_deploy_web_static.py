#!/usr/bin/python3
"""
Fabric script based on the file 1-pack_web_static.py that distributes an
archive to the web servers
"""

from fabric.api import put, run, env
from os.path import exists
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

env.hosts = ['34.239.254.111', '35.153.66.238']


def do_deploy(archive_path):
    """Distribute an archive to the web servers."""
    if not exists(archive_path):
        logger.error(f"Archive '{archive_path}' does not exist.")
        return False

    try:
        file_name = archive_path.split("/")[-1]
        no_ext = file_name.split(".")[0]
        path = "/data/web_static/releases/"
        put(archive_path, '/tmp/')
        run(f'mkdir -p {path}{no_ext}/')
        run(f'tar -xzf /tmp/{file_name} -C {path}{no_ext}/')
        run(f'rm /tmp/{file_name}')
        run(f'mv {path}{no_ext}/web_static/* {path}{no_ext}/')
        run(f'rm -rf {path}{no_ext}/web_static')
        run(f'rm -rf /data/web_static/current')
        run(f'ln -s {path}{no_ext}/ /data/web_static/current')
        logger.info("New version deployed!")
        return True
    except Exception as e:
        logger.exception("Error occurred during deployment:")
        return False


# Example usage
archive_path = 'versions/web_static_20170315003959.tgz'
do_deploy(archive_path)
