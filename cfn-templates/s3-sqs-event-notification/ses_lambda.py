import json
import logging
import os

import boto3

client = boto3.client('sesv2')
s3_resource = boto3.resource('s3')


# Configure Logging

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)

# Extracting recipient email
RECIPIENT_EMAIL = os.getenv('RECIPIENT_EMAIL', 'Provide the email id')

# Extracting senders email
SENDER_EMAIL = os.getenv('SENDER_EMAIL')

'''
Function to send an email
'''

def send_email(bucketname, filename):
    client.send_email(
        FromEmailAddress=SENDER_EMAIL,
        Destination={
            'ToAddresses': [
                RECIPIENT_EMAIL
            ]
        },
        ReplyToAddresses=[
            SENDER_EMAIL
        ],

        Content={
            'Simple': {
                'Subject': {
                    'Data': 'File Processing Failed',
                    'Charset': 'UTF-8'
                },
                'Body': {
                    'Text': {
                        'Data': "Check the unprocessed file {} located at {}".format(filename, bucketname),
                        'Charset': 'UTF-8'
                    }
                }
            }
        }
    )


'''
Lambda Handler
'''


def handler(event, context):
    LOGGER.info(event)
    data = {}
    try:
        records_ = event['Records']
        for sqs_record in records_:
            # The body of the SQS message is a text, hence converting it into a python dictionary
            s3_event_string = sqs_record['body']
            s3_event = json.loads(s3_event_string)

            for s3_record in s3_event['Records']:
                data['bucketName'] = s3_record['s3']['bucket']['name']
                data['key'] = s3_record['s3']['object']['key']

                # copy object from INCOMING/ALL_EMAILS to FAILURE/ALL_EMAILS
                s3_resource.Object(data['bucketName'], "FAILURE/" + data['key']).copy_from(CopySource=data['bucketName']+data['key'])

                # delete the former object from INCOMING/ALL_EMAILS
                s3_resource.Object(data['bucketName'], data['key']).delete()

                # Send an email
                send_email(data['bucketName'], "FAILURE/" + data['key'])

    except BaseException as ex:
        raise ex
    finally:
        LOGGER.debug(json.dumps(data, indent=4, default=str))