*** SAM IaC Execution process

**** Step 1:    
        After creating the template.yaml file run, 
        ALSO whenever there is a change in code, or template.yaml file

bash```
sam build
```

**** Step 2: 
        Above cmd creates .aws-sam dir, then run:


bash```
sam local start-api --env-vars locals.json --add-host host.docker.internal:host-gateway
```

Explanation:
- --env-vars: says where we are storing the environment variables, in this case inside locals.json
- --add-host: bridges docker tonconnect with postgresql 
