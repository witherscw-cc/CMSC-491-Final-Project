# CMSC-491-Final-Project
Final Project for CMSC 491
Steps to install this project:
1. Install the following libaries on Arduino IDE:
WiFiNINA
ArduinoBearSSL
ArduinoECCX08
ArduinoMqttClient
Arduino Cloud Provider Examples
ArduinoJson

2. Connect MKR 1000 Board and open sketch using :
File -> Examples -> ArduinoECCX08 -> Tools -> ECCX08CSR
This allows the arduino to generate a certficate for AWS

3. Open Terminal and press enter until you get to Common Name. Name this Arduino.
Select slot 0 after you press enter. Press Y to generate private key.

4.Save certifcate to text file

5.Next go to AWS and click manage -> things - > register a thing -> create a single thing.
Give thie thing a name the same as you named common name. Next, create with CSR and upload the text file with the certifcate.

6.Next, click register thing.

7.Next, click secure then policies. click create policy. Name policy and then for action write iot:* then * for resource ARN.

8.Now click certificates page under "secure". check certificate and download it.

9.Check it again and hit actions then attach policy and attach the policy we created earlier.

10. Go to settings and retrieve MQTT endpoint.

11. Go back to the arduino and open the following sketch:
Final.ino
Fill in the SSID and passwork for your home network in the ArduinoSecrets.h.
Fill in the endpoint for Secret Broker
Copy and past the certificate we downloaded earlier into secret_certficate.

A brief Description of final.ino/arduinosecrets.h:
The basic function of this code is to set up the temperature sensor, read temperature, connect to IoT Core, and publish data to the IoT Core. Starting from the top down, we begin with defining constants such as SSID, Password, certificates, endpoints, and other constants dealing with the temperature sensor such as the B value of the sensor and which pins to activate. In the setup function, it setups things such as the serial monitor, certificates slots, and validates the server’s certificates.
In the loop function, it connects to the WiFi and IoT endpoint using the credentials listed in the ArduinoSecrets.h header file. Next, it constantly polls for MQTT messages to keep the connection alive. Finally, it then publishes a message in the form of sensor data.
Going a little more in depth into the publishMessage function, it begins each message with “Arduino/outgoing”. It then creates a Json message with ‘time’ and ‘sensor_a0’ data fields. It then sends this message with “serializeJson()” and then ends the message. In the readTemp function, it reads the analog voltage value from A0. It is then converted into an R value and then converted to a temperature given by the manufacture’s equation. Then there is a delay of how ever many seconds you want between each data read and the temperature is returned.
This code can be used with a MKR WiFi 1010 or a MKR 1000. To deploy, simply connect the temperature sensor to the Arduino and upload the code. To do this, connect the red and black wires to 5V and ground respectively. Then, connect the yellow wire to A0(or whatever pin you use). Compile the function in the Arduino IDE and then upload to the board.

12. Open the serial monitor, It should start saying publishing message with the temperature following it.

13. To test to see if it is interacting with IoT Core, go to test in AWS IoT. In the subscribe topic, input arduino/outgoing and click subscribe. you should see the temperature data along with time.

14. Move to publish and change topic to arduino/incoming and click publish. Check the serial monitor from arduino and you should see a message from IoT Core.

15.Now that the arduino and IoT core are connected. Create a Kinesis Firehose Delivery Stream. In the KDF console, create a new delivery stream called sensor data stream. leave source as Direct PUT and choose next. Leave all the same and hit next again. Select S3 as a destination and create a new bucket if you don't have one already. Click next. Create new IAM Role and hit allow and finally hit create delivery stream.

16.Create two lambda functions:
For the first one we are going to call ArduinoConsumeMessage. Choose create function.For Runtime, choose Aruthor from Scratch, Node.js 10.x. For execution role create new role with basic lambda permissions. Choose Create. In the function's console go to excution role. click on ArduinoConsumeMessage-role-.... Now click attach policies and serach for AmazonKinesisFirehoseFullAccess and then attach policy. In the text editor, copy and paste ArduinoConsumeMessage.js and hit deploy.

Quick Description of ArduinoConsumeMessage.js:
In this function, it passes data from IoT Core into the Kinesis Firehose “Sensor_Data”. Starting at the top, a firehose object is defined. Next, the payload is defined. The payload in this case the time and sensor data. Next, params selects the Firehose named “Sensor_data” and sends the data defined under payload and then the data passing is complete. This can be deployed the same way as SNSFunction is but under Javascript.

16.1 Before we create the second lambda function. We need to create a topic called clothing recommendations. Open SNS console, go to topics. Choose Standard. Enter clothing recommendations for Name. You can also optionally enter this for Display name. Create Topic. Copy ARN number. Next go to subscriptions and hit create subscription. Enter Copied ARN number. Choose desired protocol. Enter enpoint for protocol (Ex. email, phone number, etc). Click Create Subscription. Repeat for any number of subscriptions.

16.2 Now that the topic is created create another amazon lambda function called SNSFunction. Repeat the steps you did to create ArduinoConsumeMessage execept for runtime choose Python 3.8 and create function. Next go to permissions and execution role and click on role name. Search for SNS FUll access and attach policy.Copy and Paste the SNSFunction into the text editor and hit deploy.

Quick Descripton of SNSFunction.py:
This function takes data from IoT Core and determines what message to send to a user based on the temperature data. Starting from the top, we create a boto3 client object called ‘sns’. This will be used to publish to the clothing topic later on. The lambda function is event driven and only is executed when IoT Core sends data to it. Next, time and data are retrieved from the Json message. Next, an if statement is used to determine which temperature range the data is in. A corresponding message is then assigned to ‘message_’. Finally, the message is then published to the topic “Clothing Recommendations” using the ARN and the message determined in the if statement above. Simply, putting this code into the text editor in the lambda screen and clicking deploy will activate this code.

17. Next go back to AWS IoT Core. click Act then create. For Rule query statement, write "SELECT * fROM 'arduino/outgoing. Choose action, send message to a lambda function, configure. First choose ArduinoConsumeMessage and Choose create rule. Repeat this step for SNSFunction.

Go back to the lambda function ->SNSfunction ->add trigger. Choose add trigger, custom IoT rule and choose rule created for SNSFunction. Now Choose add destination, choose SNS topic and then Clothing Recommendations for destination

Now Move on to quicksight. Choose new analysis and then new dataset. Choose your s3 bucket. Copy the following code into a file named manifest.json.
{
   "fileLocations":[
      {
         "URIPrefixes":[
            "s3://YOUR-BUCKET-NAME/"
         ]
      }
   ],
   "globalUploadSettings":{
      "format":"JSON"
   }
}

Upload the json file and connect then visualize.

18. You should now be able to see any data points and recieve messages based on temperature. Have Fun!
