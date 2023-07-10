import sys
import logging
import argparse
import json
import typing
import mailtrap as mt

CONFIG_ARG = "config-file"
RECIPIENT_ARG = "recipients"
BODY_ARG = "mail-body-file"

def ParseArgs() -> dict:
    parser = argparse.ArgumentParser()
    parser.add_argument(CONFIG_ARG)
    parser.add_argument(RECIPIENT_ARG)
    parser.add_argument(BODY_ARG)
    #, desc="Location of the configuration file"
    #, desc="Recipients of the email"
    #, desc="Content of the mail"
    return vars(parser.parse_args())

def ObtainCredentials(config_file: str) -> typing.Tuple[str, str]:
    with open(config_file, "r") as f:
        file_content = f.read()
        credentials = json.loads(file_content)
        return credentials['usr'], credentials['psw']

def ReadMail(mail_body_filename: str) -> typing.Tuple[str, str]:
    with open(mail_body_filename, "r") as f:
        file_content = f.read()
        content = json.loads(file_content)
        return content["subject"], content["body"]

def ParseRecipients(recipients: str) -> typing.List[str]:
    return recipients.split(":")

def sendMail(usr: str, name: str, pswd: str, subject: str, body: str, recipient_list: typing.List[str]) -> bool:
    mail = mt.Mail(
        sender=mt.Address(email=usr, name=name),
        to=recipient_list,
        subject=subject,
        text=body
    )
    pass

def main():
    logging.basicConfig(level=logging.INFO)

    arguments = ParseArgs()

    usr, pswd = ObtainCredentials(arguments[CONFIG_ARG])
    recipients = ParseRecipients(arguments[RECIPIENT_ARG])
    subject, body = ReadMail(arguments[BODY_ARG])

    logging.info('USERNAME: {}; PASSWORD: {}'.format(usr, pswd))
    logging.info('Content is: \n\t Subject: {} \n\t Body: {}'.format(subject, body))
    logging.info('Recipients are: {}'.format(recipients))

    sendMail(
        usr=usr,
        pswd=pswd,
        subject=subject,
        body=body,
        recipients=recipients
    )

if __name__ == "__main__":
    main()
