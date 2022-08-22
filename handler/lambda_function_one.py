import json
import tenjin_utility as pg
import re


def lambda_handler(event, context):
    input_json = event["queryStringParameters"]

    print(input_json)
    if "x-api-key" in event["headers"]:
        api_key = event["headers"]["x-api-key"]

        id_sql = f"Select * from tenjin_common.get_tenant_info_json('{api_key}')"
        columns = ('id_json')
        print('SQL:', id_sql)

        id_json = json.loads(pg.run(id_sql, columns))

        if not (id_json):
            return {"body": "Access to API forbidden", "statusCode": 403, "headers": {
                'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET,PUT'
                }}
        else:
            schema = id_json[0]['i']['schema']
            tenant = id_json[0]['i']['tenant']
    else:
        try:
            user_name = event['requestContext']['authorizer']['claims']['cognito:username']
            tenant = 'Tenjin'
        except KeyError:
            return {"body": "Access to API forbidden. Authorization information not provided.", "statusCode": 403,
                    "headers": {
                        'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
                        'Access-Control-Allow-Origin': '*',
                        'Access-Control-Allow-Methods': 'OPTIONS,POST,GET,PUT'
                        }}

    sql_string = f"select * from tenjin_common.get_article();"
    pg.debug_print('SQL statement', sql_string)

    # Return columns
    return_columns = ('article_json')
    created_record = json.loads(pg.run(sql_string, return_columns))
    if created_record:
        article_data = created_record[0]['a']

        return {"body": {"goals": article_data}, "statusCode": 200, "headers": {
            'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET,PUT'}}
    else:
        return {"body": {"goals": json.dumps({})}, "statusCode": 200, "headers": {
            'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET,PUT'}}

