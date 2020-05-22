REM Validate the CloudFormation templates
aws cloudformation validate-template --template-body file://SQSLambdaStack.yaml
aws cloudformation validate-template --template-body file://s3-apigateway-lambda.yaml

aws cloudformation create-stack --stack-name SQSLambdaStack --template-body file://SQSLambdaStack.yaml

REM install the dependent packages
REM pip install -r src/push_documents/requirements.txt -t src/push_documents

REM package the cloudformation template with lambda. This transforms the template and it packages the lambda in to S3 bucket created by create-stack "infrastrack"
REM aws cloudformation package --template-file s3-sqs-events.yaml --s3-bucket artifact-bucket-123456789012 --output-template-file s3-sqs-events.out.yaml

REM deploy the lambda in the newly created stack
REM aws cloudformation deploy --template-file file://s3-sqs-events.out.yaml --stack-name lambda-stack

