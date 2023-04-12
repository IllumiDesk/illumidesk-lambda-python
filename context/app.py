import json


def lambda_handler(event, context):
    """
    AWS Lambda function to handle incoming events and execute logic in
    response.

    :param event: Dictionary containing data about the incoming event.
    Specific content varies depending on the event source.
    :type event: dict.
    :param context: An object providing SDK methods, function metadata
    and invocation context.
    :type context: aws_lambda.Context.
    :returns: Any type of data. In case of integration with Amazon API Gateway,
    the response must comply with its format.
    """
    code = event.get('code')
    if code:
        try:
            output = {}
            exec(code, {}, output)
            return {
                'statusCode': 200,
                'body': json.dumps({
                    'result': output
                })
            }
        except Exception as ex:
            return {
                'statusCode': 400,
                'body': json.dumps({
                    'error': str(ex)
                })
            }
    else:
        return {
            'statusCode': 400,
            'body': json.dumps({
                'error': 'No code provided'
            })
        }
