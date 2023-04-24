import json
import os

import boto3


def run_python_code(codes: list[dict]) -> str:
    """
    Runs Python code on AWS Lambda.

    Args:
        code (str): Python code to be executed on Lambda.

    Returns:
        json: Result of the Python code execution as a json formatted string.
    """
    # Initialize the AWS Lambda client
    lambda_client = boto3.client("lambda")

    # Set up the payload with the python code to be executed on Lambda
    payload = {"codes": codes}

    # Invoke the Lambda function with the payload
    response = lambda_client.invoke(
        # Specify the Lambda function ARN (Amazon Resource Name)
        FunctionName=os.getenv("LAMBDA_FUNCTION_ARN"),
        # Set the invocation type to synchronous 'RequestResponse'
        InvocationType="RequestResponse",
        # Convert the payload to a JSON-formatted string
        Payload=json.dumps(payload),
    )

    # Parse the Lambda response payload and read the result
    result = json.loads(response["Payload"].read())

    # Return the result from the Lambda function
    return result


if __name__ == "__main__":
    TEST_CODE = "a = 2 + 3; b = a * 4"
    codes = [{"id": 1, "code": TEST_CODE}]
    test_result = run_python_code(codes)
    print(test_result)
