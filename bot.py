import discord
import responses
import asyncio
import json
import boto3


dynamodb = boto3.client('dynamodb',
		     	region_name = "YOUR_DB_REGION_NAME",
                     	aws_access_key_id = "YOUR_DB_ACCESS_KEY_ID",
                     	aws_secret_access_key = "YOUR_AWS_SECRET_ACCESS_KEY")


async def check_table(): #Checks if the data table already exists and creates one for the new client if not.
    tables = dynamodb.list_tables()
    print (tables)
    try:
        dynamodb.create_table(
	        TableName = 'kc_data',
		KeySchema = [
		        {
				'AttributeName' : "user_id",
				'KeyType' : "HASH"
			}
    		],
    		AttributeDefinitions=[
        		{
            			'AttributeName': 'user_id',
            			'AttributeType': 'S'
        		}

    		],
    		ProvisionedThroughput={
        		'ReadCapacityUnits': 10,
        		'WriteCapacityUnits': 10
    		}
	)
    except dynamodb.exceptions.ResourceInUseException:
        print ("kc_data table already found, continuing without creation.")


async def set_data(user, user_message): #Sends the user's keystone set request to the database.
    dynamodb.put_item(
            TableName = 'kc_data',
            Item = {
                'user_id' : {"S": user},
                'keystone' : {"S": user_message}
            }
    )


async def get_data():   #Returns the currently set keys (the items of the kc_data table).
    data = dynamodb.scan(
            TableName = 'kc_data'
    )
    return data['Items']


async def process_message(user, message, channel): #Sends user input to be handled by the appropriate responses module functions.
    try:
        print ('In process message, message is: (' + message + ") and author is: (" + user + ")")
        if message.startswith('!kc'):
            message_arguments = message.split()
            if message_arguments[1] == 'set':
                print ("setting message")
                await set_data(user, message_arguments[2])
                response = responses.handle_set_response(message)
            elif message_arguments[1] == 'keys':
                data = get_data()
                awaited_data = await data
                response = responses.handle_keys_response(awaited_data)
            elif message_arguments[1] == 'help':
                response = responses.handle_help_response()
            else: #Invalid user command
                response = responses.handle_unknown_response()
        await channel.send(response)
    except Exception as e:
        print(e)


def run_bot():
    TOKEN = "YOUR_TOKEN_HERE"
    client = discord.Client(intents=discord.Intents.all())
    asyncio.run(check_table())

    @client.event
    async def on_ready():
        print(f'{client.user} is now running')

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return
        user = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)
        await process_message(user, user_message, message.channel)
    client.run(TOKEN)

