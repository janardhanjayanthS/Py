# Cloudwatch
- Service to monitor all other AWS services
- Create dashboards for monitoring

#### Concepts:
- **Metric:** A variable that is being monitored, such as latency, requests, etc..
- **Dimenstions:** It is a name/value pair that uniquely identifies a metric, it is a category to filter a metric (Eg. CPUUtilization for EC2 insatace ID: 100032, here EC2 instance ID is a dimention and we can add multiple dimenstions(filters))
- **Statistics:** Aggregation of metric values over time to reveal truth!. in AWS cloudwatch -> the results of mathematical operations performed on your raw metric data over a specific window of time.
- **Alarm:** Is a trigger that performs a specified action when a metric reaches/crosses a particular threshold. It observes a particular metrich overtime
- **Logs:** Is a way to view logs created by our services/apps running in AWS - such as EC2 instance's logs, DynamoDB;s logs, etc... (they are by default sent to cloudwatch we can view it there)
    - Purpose:
        - View Setup
        - Monitoring (errors, debugging, metrics)
    - Different ways to see logs:
        - Log Stream: Logs that are generated from a service (an EC2 instance, Lambda ect...)
        - Log Group: Multiple Log Streams combined together in a single log stream (used for a full app that uses EC2, DynamoDB, etc... together)

#### Working:
1. Collect ...
2. Monitor ...
3. Act ...
4. Analyse ...


---
##### Resources:
- cloudwatch overview - https://www.youtube.com/watch?v=k7wuIrHU4UY
- tutorial - https://youtu.be/__knpcBRLHg?si=lV9TXxBrgWTP2yT8
- cloudwatch logs: https://www.youtube.com/watch?v=HRJnhzSSFtk
- using cloudwatch with fastapi -https://maazbinmustaqeem.medium.com/how-to-upload-fastapi-logs-to-aws-cloudwatch-a-beginners-guide-66b9957078b9
