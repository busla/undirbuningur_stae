import os
import sys
import logging
import argparse
import paramiko

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_connection(args):
    logger.info(f"connecting to {args.host} ...")
    host, port = args.host, 22
    transport = paramiko.Transport((host, port))
    username, password = args.user, args.password
    transport.connect(None, username, password)

    sftp = paramiko.SFTPClient.from_transport(transport)
    logger.info(f"successfully connected to {args.host} ...")
    return sftp, transport


def remove(sftp, destination):
    # eyðum öll draslinu í möppunni ef hún er til
    try:
        files = sftp.listdir(destination)
    except FileNotFoundError:
        logger.info(f"{destination} was not found on remote, skipping..")
    else:
        logger.info(f"files to be deleted: {files}")
        for f in files:
            filepath = os.path.join(destination, f)
            try:
                logger.info(f"deleting remote file {filepath}")
                sftp.remove(filepath)
                logger.info(f"successfully deleted remote file {filepath}")
            except IOError:
                remove(sftp, filepath)
        logger.info(f"deleting remote {destination} dir...")
        sftp.rmdir(destination)
        logger.info(f"successfully deleted remote {destination} dir")


def make_remote_path(destination, dir_name, rel_path):
    # hjálparfall til að búa til relative remote path, verkefni/x/y
    remote_abs_path = (
        os.path.join(args.destination, dir_name)
        if not rel_path
        else os.path.join(args.destination, rel_path, dir_name)
    )
    return remote_abs_path


def main(args):
    sftp, transport = get_connection(args)

    # Ef --dir er notað sem arg í keyrslu
    if args.dir:
        logger.info(f"Files in root on {args.host}: {sftp.listdir()}")
        abs_path = os.path.abspath(args.dir)
        logger.info(f"Abs path to local dir: {abs_path}")

        # eyðum öllu í möppunni sem beðið er um
        remove(sftp, args.destination)
        logger.info(f"creating remote dir {args.destination}")
        sftp.mkdir(args.destination)
        logger.info(f"successfully created remote dir {args.destination}")
        base_path = os.path.basename(os.path.normpath(args.dir))
        logger.info(f"base path {base_path}")
        for root, dirs, files in os.walk(abs_path, topdown=True):
            rel_path = root.split(base_path)[1].strip(os.sep)
            logger.info(f"{rel_path}")
            for dir_name in dirs:
                remote_abs_path = make_remote_path(args.destination, dir_name, rel_path)
                # logger.info(f"remote_abs_path {remote_abs_path}")
                logger.info(f"creating remote dir {remote_abs_path}")
                sftp.mkdir(remote_abs_path)
                logger.info(f"successfully created remote dir {remote_abs_path}")
            for file_name in files:
                local_path = os.path.join(root, file_name)
                # logger.info(f"root: {root}")
                remote_abs_path = os.path.join(args.destination, rel_path, file_name)
                logger.info(f"starting transferring {local_path} to {remote_abs_path}")
                _ = sftp.put(local_path, remote_abs_path)
                logger.info(f"done transferring {local_path} to {remote_abs_path}")
                # print(sftp.lstat(remote_abs_path))
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
    parser.add_argument("--destination")
    args = parser.parse_args()

    main(args)