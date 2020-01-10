# syf-alexa / Amazon Alexa Skill 

> **Important note**: this solution was developed and provided as part of a hackathon. This
> project is currently not being used in a project and is to be understood as a demo.

Amazon Alexa Skill 'SyF' (working title) starts and queries the Sigfox backend via APIv2 for new IoT readings

User: `Alexa, open <invocation name>.`<br />
User: `Alexa, open <invocation name> with details.`<br />
User: `Alexa, open <invocation name> with Team.`<br />


## Requirements
The following conditions are required for this skill:

1. Sigfox IoT device (e.g. Pycom devices)
2. IoT device reports information to the Sigfox backend (or has already reported)
3. sigfox backend is released via API access
4. AWS access
5. Amazon Developer (Alexa) access

*Of course, other devices and a different network/backend than Sigfox can also be used. The code must be adapted accordingly.*

## Installation
###Sigfox Backend

1. Transfer of the measured values into the Sigfox backend using a suitable routine.
2. Setting up access information for API use. This information is later entered in the Alexa Skill under 'Sigfox_API_USername' and 'Sigfox_API_Password'.

*Note: In the present scenario, the data is compressed so that the desired value range can be sent as a single byte. The information in the backend has the format xxyy, where 'xx' is the protocol version (01) used by the sending device and 'yy' corresponds to the actual measured value.*

###AWS Lambda

1. Create a Amazon AWS Lambda function (at https://console.aws.amazon.com/console/home)
2. Create a new function with settings `Author from scratch`, `Python 2.7 Runtine`, `Create a custome role` with 'lambda_basic_execution
2. Select 'Alexa Skill Kit' as trigger for the own function
3. Copy code from `/aws_lambda/` into the Code9 editor
2. Define environment variables 'Card_Title_Prefix', 'Skill_Name', 'Skill_Answer_DefaultMode', 'Sigfox_Device_ID', 'Sigfox_API_USername' and 'Sigfox_API_Password' and specify them with their own values
3. Check the executability of the code again by `Test`; if necessary, create a test event (`Test Event` based on the template `Amazon Alexa Start Session`)

###Alexa skill
1. Create Amazon Alexa Skill in the Amazon Developer (https://developer.amazon.com/home.html) under `Alexa Skill Kit`
2. Select skill with `Custom` model and `Alexa-Hosted` method
2. Specify `Invocation`
3. Create intents `detail`, 'short' and `team` with desired own uterances (example see /alexa_skill/syf.json)
4. Endpoint for Amazon Alexa Skill ⇄ Set up Amazon AWS Lambda function and enter ARN of the ASW Lambda handler
5. Save skill again and have it regenerated

## Notes
Depending on the speed of the backend query, the initial start of the skill/lambda function and the query of the backend may take more than 3 seconds. In this case the Lambda function reports a timeout error. If this behavior occurs frequently, the timeout default of 3 seconds may have to be increased. However, it should be remembered that longer startup phases can affect the UX at the user's end. For this reason, the prototype query shown here is limited to one device.

#### Tags
 #sigfox #iot #aws #alexa #python #temperature
