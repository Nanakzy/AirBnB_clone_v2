#!/usr/bin/python3
"""
Fabric script to genereate tgz archive
execute: fab -f 1-pack_web_static.py do_pack
"""


from fabric.api import local, put, run, env
from os.path import exists, isfile
from datetime import datetime  # Importing datetime module
import os

# Initialize the Fabric environment
env.hosts = ['34.239.254.111', '35.153.66.238']
env.user = 'ubuntu'


def do_pack():
    """
    Creates a compressed archive of the web_static directory
    """
    now = datetime.now().strftime("%Y%m%d%H%M%S")
    local("mkdir -p versions")
    result = local("tar -czvf versions/web_static_{}.tgz web_static".format
                   (now))
    if result.failed:
        print("Error: Failed to create the archive.")
        return None
    elif result.return_code != 0:
        print("Error: Non-zero return code from tar command.")
        return None
    else:
        archive_path = "versions/web_static_{}.tgz".format(now)
        print("web_static packed: {} -> {} Bytes".format
              (archive_path, os.path.getsize(archive_path)))
        return archive_path


def do_deploy(archive_path):
    """
    Distributes an archive to the web servers
    """
    if not exists(archive_path) or not isfile(archive_path):
        return False

    try:
        file_name = archive_path.split("/")[-1]
        file_no_ext = file_name.split(".")[0]
        remote_path = "/data/web_static/releases/{}/".format(file_no_ext)

        put(archive_path, "/tmp/")
        run("mkdir -p {}".format(remote_path))
        run("tar -xzf /tmp/{} -C {}".format(file_name, remote_path))
        run("rm /tmp/{}".format(file_name))
        run("mv {}web_static/* {}".format(remote_path, remote_path))
        run("rm -rf {}web_static".format(remote_path))
        run("rm -rf /data/web_static/current")
        run("ln -s {} /data/web_static/current".format(remote_path))

        return True
    except Exception as e:
        print(e)
        return False
