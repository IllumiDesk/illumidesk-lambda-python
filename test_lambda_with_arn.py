import boto3
import json

def run_python_code(code):
    """
    Runs Python code on AWS Lambda.

    Args:
        code (str): Python code to be executed on Lambda.

    Returns:
        json: Result of the Python code execution as a json formatted string.
    """
    # Initialize the AWS Lambda client
    lambda_client = boto3.client('lambda')
    
    # Set up the payload with the python code to be executed on Lambda
    payload = {
        'code': code
    }
    
    # Invoke the Lambda function with the payload
    response = lambda_client.invoke(
        # Specify the Lambda function ARN (Amazon Resource Name)
        FunctionName='arn:aws:lambda:us-east-1:860100747351:function:app-dev-docker-lambda_handler',
        # Set the invocation type to synchronous 'RequestResponse'
        InvocationType='RequestResponse',
        # Convert the payload to a JSON-formatted string
        Payload=json.dumps(payload)
    )
    
    # Parse the Lambda response payload and read the result
    result = json.loads(response['Payload'].read())
    
    # Return the result from the Lambda function
    return result


if __name__ == '__main__':
    code = 'a = 2 + 3; b = a * 4'
    result = run_python_code(code)
    print(result)
