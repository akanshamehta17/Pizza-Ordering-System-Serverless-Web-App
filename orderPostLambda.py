from __future__ import print_function 
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

  table1 = dynamodb.Table('PizzaDB')
  table2=dynamodb.Table('PizzaOrder')
  getResponse =  table1.get_item(
        Key={
            'menu_id': event["menu_id"]
        }
    )
  
 
  try:
    resp = table2.put_item(
    Item={   
    "menu_id": event["menu_id"],
    "order_id": "uuid_generated_by_client",
    "customer_name": "John Smith",
    "customer_email": "foobar@gmail.com"
     }
  
   )
  
  
    response = "Hi"+ " " + event["customer_name"] + ", please choose one of these selection:"
    count = 1
    for value in getResponse['Item']['selection']:
      response+= str(count) + "." + value + "," + " "
      count = count + 1
  
    return { "Message": response }
    
    
    
  except Exception,e:
        return 400, e
  return 200, "OK"
  return response
  print("PutItem succeeded:")
  print(json.dumps(response, indent=4, cls=DecimalEncoder))
