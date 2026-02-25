CMD:

- After creating a template.yaml file
- run: sam build -> to prepare code for cloud
- run: sam deploy --guided -> To deploy code to cloud (only if you have credentials for AWS services)
- or to run code locally 
- run: sam local invoke <function name> --event <json or path to json file>
    - <function name>: from the template.yaml file, here GreetFunction
    - <json or path to json file>: json prams to lambda_handler:event -> dict or json file, here events/event.json

