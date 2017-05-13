from __future__ import print_function # Python 2/3 compatibility
import boto3
from botocore.exceptions import ClientError
import json
import decimal
from time import gmtime, strftime

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

  table1 = dynamodb.Table('PizzaDB')
  table2 = dynamodb.Table('PizzaOrder')
 
  try:
    Order = table2.get_item(
     Key={
            "order_id": event["order_id"]
        }
     )
  
    Menu = table1.get_item(
     Key={
            "menu_id": Order['Item']['menu_id']
        }
     )
  
    if Order['Item'].get('order') is None:
        table2.update_item(
        Key={
            "order_id": event['order_id']
        },
    
        UpdateExpression="set #o = :v",
        ExpressionAttributeNames = {
                    "#o":"order"
                
                },
        ExpressionAttributeValues={
            
            ':v': {
                        "selection": Menu['Item']['selection'][int(event['input'])-1]
                        }
         },
      )
        response = "Which size do you want?" 
        count = 1
        for s in Menu['Item']['size']:
                response += str(count) + ". " + str(s)+" "
                count += 1
        return {
                'Message': response
                }
                
    else:
        
        table2.update_item(
            
            Key={
            "order_id": event['order_id']
        },
        
        UpdateExpression="set #o.size = :v1,#o.costs = :v2,#o.order_time=:v3,order_status=:v4",
                ExpressionAttributeNames = {
                    "#o":"order"
                
                },
        ExpressionAttributeValues={
            ':v1': Menu["Item"]["size"][int(event['input'])-1],
            ':v2': "15.00",
            ':v3': strftime("%m-%d-%Y@%H:%M:%S", gmtime()),
            ':v4': "processing"
         },
        
            )
        
        response = "Your order costs $15.00. We will email you when the order is ready. Thank you!"
        return {
                'Message': response
                }
  except Exception,e:
        return 400, e
  return 200, "OK"
  print("UpdateItem succeeded:")
  print(json.dumps(response, indent=4, cls=DecimalEncoder))
