import json
import boto3
import logging
import json

sns=boto3.client('sns')

def lambda_handler(event, context):
    # TODO implement
    time = event.get("time")
    data = event.get("sensor_a0")
    
    
    if data <= 100.0 and data >= 70.0:
        message_ = "Its hot! Wear shorts and a t-shirt"
    elif data < 70 and data >= 60:
        message_ = "It is a little cool. Wear some jeans."
    elif data < 60 and data >= 40:
        message_ = "It is cold outside. Wear some sweatpants or jeans and a sweatshirt"
    elif data < 40 and data >= 30:
        message_ = "It is really cold outside. Wear a thick jacket"
    elif data < 30 and data >= 20:
        message_ = "It is below freezing. Recommend a thick jacket with some overalls"
    elif data < 20 and data >= 0:
        message_ ="It is too cold outside. Recommend coveralls with a theraml headwrap"
    else:
        message_ ="Warning, temperature reading is outside expected parameters. Please check the sensor."
   
    response = sns.publish(
        TopicArn='arn:aws:sns:us-east-1:190997780738:Clothing_Recommendations',
        Message = message_,
        )
        
    print(response)
    """
    response = sns.publish(
        PhoneNumber='+18047611650',
        Message = message_,
        )
    
    print(response)
    """
    return 'OK'
    
