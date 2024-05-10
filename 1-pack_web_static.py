#!/usr/bin/python3
"""
Fabric script that generates a .tgz archive from the contents of the web_static
folder of your AirBnB Clone repo
"""

from fabric.api import local
from datetime import datetime


def do_pack():
    """
    Generate a .tgz archive from the contents of the web_static folder

    Returns:
        str: Path to the archive if archive is generated, otherwise None
    """
    # Create the 'versions' folder if it doesn't exist
    local("mkdir -p versions")

    # Generate the name for the archive using current date and time
    now = datetime.now()
    archive_name = "versions/web_static_{}{}{}{}{}{}.tgz".format(
        now.year,
        str(now.month).zfill(2),
        str(now.day).zfill(2),
        str(now.hour).zfill(2),
        str(now.minute).zfill(2),
        str(now.second).zfill(2)
    )

    # Create the .tgz archive
    result = local("tar -cvzf {} web_static".format(archive_name))

    # Check if archive creation was successful
    if result.failed:
        return None
    else:
        return archive_name


if __name__ == "__main__":
    do_pack()
