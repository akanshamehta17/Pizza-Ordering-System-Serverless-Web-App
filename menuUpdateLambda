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
  dynamodb = boto3.resource('dynamodb', region_name='us-west-2')

  table = dynamodb.Table('PizzaDB')


  try:
    response = table.update_item(
      Key={
        'menu_id': event["menu_id"]
     },
    UpdateExpression="set selection = :s",
    ExpressionAttributeValues={
        ':s': event["selection"]
    },
    ReturnValues="UPDATED_NEW"
)
  except Exception,e:
    return 400, e
  return 200, "OK"    

  print("UpdateItem succeeded:")
  print(json.dumps(response, indent=4, cls=DecimalEncoder))
