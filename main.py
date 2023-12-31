import os
import secrets

os.environ["CONFIG_DIR"] = os.getenv("CONFIG_DIR", "/config")
os.environ["SETTINGS_PATH"] = os.getenv("SETTINGS_PATH", os.path.join(os.environ["CONFIG_DIR"], 'settings.yml'))
os.environ["USERS_DB_PATH"] = os.getenv("USERS_DB_PATH", os.environ["SETTINGS_PATH"])


os.environ["CACHE_TTL"] = os.getenv("CACHE_TTL", '60')
os.environ["LOG_LEVEL"] = os.getenv("LOG_LEVEL", "INFO")

os.environ["FLASK_SESSION_COOKIE_DOMAIN"] = os.getenv("FLASK_SESSION_COOKIE_DOMAIN","")
os.environ["FLASK_SECRET_KEY"] = os.getenv("FLASK_SECRET_KEY",secrets.token_hex(16))

import logging

import logging
import sys
import time
import argparse
import pidfile
import getpass

import server.users
import server.core

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(funcName)s() - %(levelname)s - %(message)s', level=os.environ["LOG_LEVEL"])

logger = logging.getLogger(__name__)

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Select mode')
    parser.add_argument('mode', type=str, help='Select modules', choices=[
                        "server", "users"])
    args = parser.parse_args(sys.argv[1:2])

    if args.mode == 'server':
        parser.add_argument("action", type=str,
                            help="Select actions", choices=["start", "kill"])
        args = parser.parse_args()

        if args.action == 'start':

            if os.path.exists('pidfile'):
                try:
                    # check if process is running
                    os.kill(int(open('pidfile').read()), 0)
                    time.sleep(1)
                    os.remove('pidfile')

                except OSError:
                    os.remove('pidfile')

            try:
                with pidfile.PIDFile("pidfile"):
                    server.core.start()
            except pidfile.AlreadyRunningError:
                logger.critical('Server already running!')

        elif args.action == 'kill':
            try:
                os.kill(int(open('pidfile').read()), 2)
                logger.info("Sent SIGKILL")
                time.sleep(3)

                os.kill(int(open('pidfile').read()), 0)
                logger.warning("Not Killed")

            except OSError:
                logger.info("Killed!")

    if args.mode == "users":
        parser.add_argument("action", type=str, help="Select actions", choices=[
                            "add", "delete", "edit"])
        parser.add_argument("username", type=str, nargs=1)

        parser.add_argument("--password", type=str, nargs=1)
        parser.add_argument(
            "--algo", type=str, help="hashing algorithm to be used", default='sha256')
        parser.add_argument("--salt_bytes", type=int,
                            help="number of salt bytes", default=16)
        parser.add_argument("--iterations", type=int, default=10000)

        args = parser.parse_args()
        if args.action == "add":
            if args.password == None:
                args.password = [getpass.getpass("Enter new password:")]

            status, msg = server.users.add_user(
                args.username[0], args.password[0], algo=args.algo, salt_bytes=args.salt_bytes, iterations=args.iterations)
            logger.info(msg)

        elif args.action == "edit":
            if args.password == None:
                args.password = [getpass.getpass("Enter new password:")]

            status, msg = server.users.edit_user(
                args.username[0], args.password[0], algo=args.algo, salt_bytes=args.salt_bytes, iterations=args.iterations)
            logger.info(msg)

        elif args.action == 'delete':
            status, msg = server.users.delete_user(
                args.username[0], verify=False)
            logger.info(msg)
