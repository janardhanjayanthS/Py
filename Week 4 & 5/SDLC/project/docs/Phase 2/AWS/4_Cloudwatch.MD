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

#### Prerequisites:
- An container - EC2, Lambda or any Cloud Compute instance running an app
- Cloud watch agent - a service in that instance that sends logs from the cloud computer to cloud watch


#### Example with fastapi app running in EC2 instance:

**Step 1: Write logs to a file**
    - Run The application as you would in EC2, make sure that it writes logs to a file - Eg: vars/logs/sampleapp/app.log
    (check log.py from https://github.com/janardhanjayanthS/fastapi_book_app/blob/main/log.py repo)

**Step 2: Install Cloudwatch agent and verify its installation**

    ```bash
    wget https://s3.amazonaws.com/amazoncloudwatch-agent/ubuntu/amd64/latest/amazon-cloudwatch-agent.deb # download aws cloudwatch agent

    sudo dpkg -i amazon-cloudwatch-agent.deb

    sudo systemctl status amazon-cloudwatch-agent
    ```

**Step 3: Configure AWS Cloudwatch Agent**

```bash
sudo vim /opt/aws/amazon-cloudwatch-agent/etc/amazon-cloudwatch-agent.json # to open configuration file
```

- Paste the following code in that file

```bash
{
  "logs": {
    "logs_collected": {
      "files": {
        "collect_list": [
          {
            "file_path": "/var/log/myapp/app.log",
            "log_group_name": "/ec2/myapp",
            "log_stream_name": "{instance_id}",
            "timestamp_format": "%Y-%m-%d %H:%M:%S",
            "retention_in_days": 30
          }
        ]
      }
    }
  }
}
```

- file_path — the log file on your EC2 disk to watch
- log_group_name — the "folder" in CloudWatch where logs will appear. Name it however you like, /ec2/myapp is a common convention
- log_stream_name — within a log group, each EC2 instance gets its own stream. {instance_id} is a variable that auto-fills your instance ID (useful if you have multiple EC2 instances running the same app)
- retention_in_days — automatically delete old logs after 30 days (saves money)

**Step 4: Start Cloudwatch agent**

```bash
sudo /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-ctl \
  -a fetch-config \
  -m ec2 \
  -s \
  -c file:/opt/aws/amazon-cloudwatch-agent/etc/amazon-cloudwatch-agent.json

#then check
sudo systemctl status amazon-cloudwatch-agent
```

**Step 5: Vola!**

- The Logs will be seen in Log management tab in AWS Cloudwatch console



---
##### Resources:
- cloudwatch overview - https://www.youtube.com/watch?v=k7wuIrHU4UY
- tutorial - https://youtu.be/__knpcBRLHg?si=lV9TXxBrgWTP2yT8
- cloudwatch logs: https://www.youtube.com/watch?v=HRJnhzSSFtk
- using cloudwatch with fastapi -https://maazbinmustaqeem.medium.com/how-to-upload-fastapi-logs-to-aws-cloudwatch-a-beginners-guide-66b9957078b9
