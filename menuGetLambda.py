from __future__ import print_function
import boto3
import json
import decimal
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError

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
  dynamodb = boto3.resource("dynamodb", region_name='us-west-2')

  table = dynamodb.Table('PizzaDB')

  try:
     response = table.get_item(
        Key={
            'menu_id': event['menu_id']
        }
    )
    
  except Exception,e:
        return 400, e
  item = response['Item']
  return item
  print("GetItem succeeded:")
  print(json.dumps(item, indent=4, cls=DecimalEncoder))
