# Home tools


## Automatic mail

The first version of the automatic mail should comply to the following requirements:

	- Be able to send an email from a common mail service (such as Gmail or other (tbd)).
	- Read credentials from a configuration file.
	- Log all the accesses in a log file given as a flag.
	- Notify both through terminal log and in the given logfile the accomplishment or failure to send the email
	- Send email to personal accounts (for testing).
	- Logger with custom colors in Linux terminal.

The script that results on sending a particular message to a person or set of persons should contain the following:
	-  Capability to send messages to both 1 recipient or various
	-  Receive the directories to the files that contain the following:
      	-  Message info:
         	-  Sender
         	-  Recipient/s
         	-  Subject
         	-  Body
		- Credentials for the API
    		- Token (token.json)
    		- Credentials (credentials.json)

To have all the previously mentioned functionalities some way to implement it is using an Argument Parser that receives the following flags:
	- **Message info**: Path to the file that contains the message info
	- **Credentials info**: Directory with the credentials files
	- **Debug level**: differentiate messages between its level of importance