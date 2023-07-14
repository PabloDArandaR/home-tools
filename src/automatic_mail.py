import os
import sys
import logging
import argparse
import json
import typing
import gmail as gm
import constants

CONFIG_ARG = "config-dir" # To, From, Subject, Message json file location
CRED_ARG = "cred-dir"
TOKEN_ARG = "token-dir"
DEBUG_LEVEL = "--debug-level"

def ParseArgs() -> dict:
    parser = argparse.ArgumentParser()
    parser.add_argument(CONFIG_ARG, help="Location of the message data file")
    parser.add_argument(CRED_ARG, help="Location of the credentials file")
    parser.add_argument(TOKEN_ARG, help="Location of the token file")
    parser.add_argument("-d", DEBUG_LEVEL, help="Level of the debug", action="store_true")
    return vars(parser.parse_args())


def ReadMessageInfo(filename: str)-> typing.Tuple[str, list[str], str, str]:
    try:
        with open(filename, "r") as f:
            data = json.load(f)
            return (
                data[constants.SENDER_KWD],
                data[constants.RECIPIENT_KWD] if type(data[constants.RECIPIENT_KWD]) == list else [data[constants.RECIPIENT_KWD]],
                data[constants.SUBJECT_KWD],
                data[constants.BODY_KWD]
            )
    except FileNotFoundError:
        logging.error("File for message info in path {} was not found.".format(filename))
        sys.exit()


def main():

    arguments = ParseArgs()
    if "d" in arguments.keys():
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    cred = gm.HandleCredentials(
        dir_cred=arguments[CRED_ARG],
        dir_token=arguments[TOKEN_ARG]
        )
    logging.debug("Credentials have been setup")

    sender, recipient, subject, body = ReadMessageInfo(arguments[CONFIG_ARG])
    logging.debug("Message info has been read correctly")

    if len(recipient) == 1:
        message = gm.GenerateGmailMessage(
            recipient=recipient,
            sender=sender,
            content=body,
            subject=subject
        )
    else:
        message = gm.GenerateGmailMessageGroup(
            recipients=recipient,
            sender=sender,
            content=body,
            subject=subject
        )
    logging.debug("Message has been generated")

    service = gm.GenerateGmailService(credentials=cred)

    gm.SendGmailMessage(service=service, message=message)
    logging.info("Message with message_info_filename {} has been sent.".format(arguments[CONFIG_ARG]))


if __name__ == "__main__":
    main()
