from __future__ import print_function 
import boto3
from botocore.exceptions import ClientError
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
  dynamodb = boto3.resource('dynamodb', region_name='us-west-2')

  table = dynamodb.Table('PizzaDB')




  try:
    response = table.delete_item(
        Key={
            'menu_id': event["menu_id"]
        },
        
    )
  except Exception,e:
    return 400, e
  return 200, "OK"
  
  print("DeleteItem succeeded:")
  print(json.dumps(response, indent=4, cls=DecimalEncoder))
