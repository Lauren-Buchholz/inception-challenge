# Inception Health Technical Challenge

##
Challege was done using AWS CDK v2 for python
Note, I had never used this before, but I remember some odd troubles trying to define and deploy lambdas via terraform and needing a CI/CD pipeline in the past,though not lambda via docker images, so I figured I would check out CDK

To deploy this, you need to have a recent version of python3 installed, then do a 
```
$ pip install -r requirements.txt
```

At this point you can now synthesize the CloudFormation template for this code.

```
$ cdk synth
```

and if all looks good, 

```
$ cdk deploy
```


So for the challenge, the single command needed would be cdk deploy from the project directory.  CDK best practices want the IaC and application logic together like this, and both are versioned controlled together.

The CDK project is current hard wired to the account you have me, but there are options to have this deploy to multiple environments if needed.  I did not implement that for this demo.

Everything works from the assignment except the route53 zone.  I don't see that hosted zone in the account and even doing a 'aws route53 list' retuned [].  So if this is from a different account and there is some corss account access policy, I was not sure how to get that working with what I did, do the API is just using the standard dynamic URL.  If you look in the app.py code, you can see how I would get a zone to attach to the gw though

I also deployed this all as a single stack.  This was trivial enough it made sense, but for a larger project you could absolutely break this into more manageble chunks.

I also included the deploy output, see ./cdk_deploy.log for that.

Lastly, I did develop this on a macbook, so the docker images are ARM64 based and the corresponding lambdas are running on graviton, not x86 backing compute.

High level, I think that is about it and I think this should meet all our reqs except for the dns zone.  It did take me more than three hours, but I figured why not learn CDK in the process.  :)
