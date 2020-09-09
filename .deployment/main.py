import os
import sys
import logging
import argparse
import paramiko

logger = logging.getLogger(__name__)


def get_connection(args):
    host, port = args.host, 22
    transport = paramiko.Transport((host, port))
    username, password = args.user, args.password
    transport.connect(None, username, password)

    sftp = paramiko.SFTPClient.from_transport(transport)
    return sftp, transport


def remove(sftp, path):
    # eyðum öll draslinu í möppunni ef hún er til
    files = sftp.listdir(path)
    for f in files:
        filepath = os.path.join(path, f)
        try:
            sftp.remove(filepath)
        except IOError:
            remove(sftp, filepath)
    sftp.rmdir(path)


def make_remote_path(root, remote_path):
    # hjálparfall til að búa til relative remote path, verkefni/x/y
    if f"{remote_path}/" in root:
        rel_path = os.path.join(remote_path, root.split(f"{remote_path}/")[1])
    else:
        rel_path = remote_path
    return rel_path


def main(args):
    sftp, transport = get_connection(args)

    logger.info(f"before: {sftp.listdir()}")
    # Ef --dir er notað sem arg í keyrslu
    if args.dir:
        abs_path = os.path.abspath(args.dir)
        remote_path = os.path.basename(os.path.normpath(args.dir))
        # eyðum öllu í möppunni sem beðið er um
        remove(sftp, remote_path)
        logger.info(f"creating dir: {remote_path}")
        sftp.mkdir(remote_path)
        logger.info(f"success: {remote_path}")
        for root, dirs, files in os.walk(abs_path, topdown=True):
            for dir_name in dirs:
                rel_path = make_remote_path(root, remote_path)
                remote_abs_path = os.path.join(rel_path, dir_name)
                logger.info(f"creating dir: {remote_abs_path}")
                sftp.mkdir(remote_abs_path)
                logger.info(f"success: {remote_abs_path}")
            for file_name in files:
                local_path = os.path.join(root, file_name)
                logger.info(root)
                logger.info(remote_path)
                rel_path = make_remote_path(root, remote_path)

                remote_abs_path = os.path.join(rel_path, file_name)
                logger.info(f"started copying {local_path} to {remote_abs_path}")
                _ = sftp.put(local_path, remote_abs_path)
                logger.info(f"done: {local_path} to {remote_abs_path}")
                print(sftp.lstat(remote_abs_path))
    # Ef --file er notað sem arg í keyrslu
    else:
        filepath = os.path.basename(args.file)
        _ = sftp.put(args.file, filepath)
        logger.info(f"after: {sftp.listdir()}")
    if sftp:
        sftp.close()
    if transport:
        transport.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    # færð villu ef þú reynir að nota --dir og --file saman
    group.add_argument("--file")
    group.add_argument("--dir")

    parser.add_argument("--user", required=True)
    parser.add_argument("--password", required=True)
    parser.add_argument("--host", default="katla.rhi.hi.is")
    args = parser.parse_args()

    main(args)