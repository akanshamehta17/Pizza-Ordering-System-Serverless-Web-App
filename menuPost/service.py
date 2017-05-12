import boto3
import json

def format(list, var):
    return [dict({var:item}) for item in list]

def handler(event, context):
    # Your code goes here!
    client = boto3.client("dynamodb")

    store_hours={}
    for item in event["store_hours"]:
        it=dict()
        it["S"] = event["store_hours"][item]
        store_hours[item] = it
    
    try:
        client.put_item(TableName="PizzaDB", Item={"menu_id":{"S":event["menu_id"]}, "store_name": {"S":event["store_name"]}, "selection":{"L": format(event["selection"],"S")}, "size":{"L":format(event["size"],"S")}, "price":{"L":format(event["price"],"N")}, "store_hours":{"M":store_hours}})
    except Exception,e:
        return 400, e
    return 200, "OK"
