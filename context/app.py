import io
import json
import sys


class OutputCatcher(io.StringIO):
    def __init__(self):
        self.buffer = ""
        super().__init__(self.buffer)

    def write(self, msg):
        self.buffer += msg

    def flush(self):
        pass


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
    codes: list[dict] = event.get("codes")
    if codes:
        results = []
        exec_globals = {}
        exec_locals = {}

        for code_block in codes:
            output_catcher = OutputCatcher()
            sys.stdout = output_catcher

            result = {
                "id": code_block["id"],
                "outputs": [],
            }

            try:
                exec(code_block["code"], exec_globals, exec_locals)
            except Exception as ex:
                result["outputs"].append({"type": "error", "content": str(ex)})

            sys.stdout = sys.__stdout__
            output = output_catcher.buffer
            if output:
                result["outputs"].append({"type": "stdout", "content": output})

            results.append(result)

        response = {
            "statusCode": 200,
            "body": json.dumps({"results": results}),
        }
        return response
    else:
        return {"statusCode": 400, "body": json.dumps({"error": "No code provided"})}
