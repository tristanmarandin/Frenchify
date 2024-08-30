# -*- coding: utf-8 -*-
import json
import boto3
import traceback

def lambda_handler(event, context):
    
    bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')
    
    # Extract the text input from the API Gateway event
    if isinstance(event["body"], str):
        body = json.loads(event["body"])
    else:
        body = event["body"]
    
    input_text = body["request"]

    print(input_text)

    # Call the Bedrock API
    try:
        body = json.dumps(
            {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 2000,
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": input_text
                            }
                        ]
                    }
                ]
            },
            ensure_ascii=False
        ).encode('utf-8')
        
        print(body)
        
        modelId = 'anthropic.claude-3-5-sonnet-20240620-v1:0'
        accept = 'application/json'
        contentType = 'application/json'

        # Parse the response from Bedrock
        bedrock_response = bedrock.invoke_model(modelId=modelId, contentType=contentType, accept=accept, body=body)
        response_body = json.loads(bedrock_response.get('body').read().decode('utf-8'))
        result = response_body["content"][0]["text"]

        # Prepare the response for API Gateway
        return {
            'statusCode': 200,
            'body': json.dumps({
                'model_response': result
            }, ensure_ascii=False),
            'headers': {
                'Content-Type': 'application/json; charset=utf-8',
                'Access-Control-Allow-Origin': '*'
            }
        }
        
    except Exception as e:
        print(f"Error: {str(e)}")
        print(traceback.format_exc())    
        # Handle exceptions and return an error response
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': str(e)
            }, ensure_ascii=False),
            'headers': {
                'Content-Type': 'application/json; charset=utf-8',
                'Access-Control-Allow-Origin': '*'
            }
        }