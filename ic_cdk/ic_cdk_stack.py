from aws_cdk import (
    aws_lambda as _lambda,
    aws_dynamodb as _ddb,
    aws_apigateway as api_gateway,
    aws_events as events,
    aws_events_targets as event_targets,
    aws_route53 as route53,
    aws_route53_targets as route53_targets,
    aws_certificatemanager as certificatemanager,
    CfnOutput,
    App,
    Duration,
    Stack
)
from constructs import Construct
import aws_cdk as cdk

# depployment defaults
dynamo_table_name = "inception_dynamo_table"
API_SUBDOMAIN = "jake-sandbox.ihengine.com"

class ICCDKStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

#Docker Section

        inception_dynamo_table = _ddb.Table(
            self, dynamo_table_name,
            table_name=dynamo_table_name,
            partition_key=_ddb.Attribute(
                name="id",
                type=_ddb.AttributeType.STRING
            ),
            # dynamo and s3 are not removed by default, so we need to set removal policy.  
            # most likely not production friendly, but makes sense here
            removal_policy=cdk.RemovalPolicy.DESTROY
        )

#Lambda Rest API Section
        # this is how to deploy a lambda from a docker image
        LambdaExpress = _lambda.DockerImageFunction(self, "LambdaExpress",
                                                    function_name="LambdaExpress",
                                                    architecture=_lambda.Architecture.ARM_64,
                                                    code=_lambda.DockerImageCode.from_image_asset(directory="ic_cdk/app_express")
            )
        # this sets the an env variable for the lambda to know the dynamo table name
        LambdaExpress.add_environment("DYNAMO_TABLE_NAME", dynamo_table_name)
        
    
        ### TODO there are no hosted zones my account sees or can access, so this is just returning []
        # this is just using the dynamically created ip for now, but the below is how you can get a hosted
        # zone and then attact it to the api_gateway
        # hosted_zone = route53.HostedZone.from_lookup(self, 'myHostedZone', domain_name=API_SUBDOMAIN)

        # this creates the api gateway and attaches the lambda to the api. 
        gw = api_gateway.LambdaRestApi(
            self,
            'LambdaExpress-api-gateway',
            handler=LambdaExpress,
        )

        # this output the dynamic url back to the user during a deploy
        CfnOutput(self, "LambdaExpress-api-gateway-output", value=gw.url)
        #this grants the lambda the ability to read from the dynamo table
        inception_dynamo_table.grant_read_data(LambdaExpress)

#Lambda checkin Section
        LambdaCheckin = _lambda.DockerImageFunction(self, "LambdaCheckin",
                                                    function_name="LambdaCheckin",
                                                    architecture=_lambda.Architecture.ARM_64,
                                                    code=_lambda.DockerImageCode.from_image_asset(directory="ic_cdk/app_checkin")
            )

        LambdaCheckin.add_environment("DYNAMO_TABLE_NAME", dynamo_table_name)

        # this attached a cron like trigger to the Checkin lambda
        # Run every day on the hour
        rule = events.Rule(
            self, "Rule",
            schedule=events.Schedule.cron(
                minute='0',
                hour='*',
                month='*',
                week_day='*',
                year='*'),
        )
        rule.add_target(event_targets.LambdaFunction(LambdaCheckin))
        # this grants the lambda the ability to write from the dynamo table
        inception_dynamo_table.grant_write_data(LambdaCheckin)



