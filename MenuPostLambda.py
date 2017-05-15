from __future__ import print_function # Python 2/3 compatibility
import boto3
import json
import decimal

# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)


def lambda_handler(event, context):
    
 try:    
    dynamodb = boto3.resource('dynamodb', region_name='us-west-2')

    table = dynamodb.Table('PizzaDB')

    response = table.put_item(
        Item=event

        )
 except Exception,e:
        return 400, e
 return 200, "OK"

 print("PutItem succeeded:")
 print(json.dumps(response, indent=4, cls=DecimalEncoder))
