const AWS = require('aws-sdk')

const firehose = new AWS.Firehose()
const StreamName = "Sensor_Data"

exports.handler = async (event) => {
    
    console.log('Received IoT event:', JSON.stringify(event, null, 2))
    
    let payload = {
        time: new Date(event.time),
        //time: new Date(Date.now()).toString(),
        sensor_value: event.sensor_a0
    }
    
    let params = {
            DeliveryStreamName: StreamName,
            Record: { 
                Data: JSON.stringify(payload)
            }
        }
        
    return await firehose.putRecord(params).promise()

}