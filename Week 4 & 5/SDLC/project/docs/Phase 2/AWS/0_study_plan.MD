# AWS Learning Roadmap — Backend Developer
> **Level:** Upper Beginner in Cloud | **Role:** Backend Developer
> **Goal:** Learn AWS services for backend development, from fundamentals to production-ready applications.

---

## 🗺️ Overview

| Phase | Topic |
|-------|-------|
| 1 | AWS Fundamentals & IAM |
| 2 | Core Compute & Storage |
| 3 | Serverless Core & Dev Tooling |
| 4 | Containers |
| 5 | Data & Caching |
| 6 | Networking |
| 7 | Security & Secrets |
| 8 | Events & Orchestration |
| 9 | Observability & Communication |
| 10 | Capstone Project |

---

## 🌐 Master Resource List (Start Here)

These resources cover AWS broadly and are useful throughout every phase. Bookmark all of them.

### 📺 YouTube Channels

| Channel | Best For |
|---------|----------|
| [AWS Official Channel](https://www.youtube.com/@amazonwebservices) | Official deep dives, re:Invent talks, product news |
| [AWS Online Tech Talks](https://www.youtube.com/@AWSOnlineTechTalks) | Live demos and best-practice walkthroughs per service |
| [freeCodeCamp](https://www.youtube.com/@freecodecamp) | Full beginner courses (Cognito, Lambda, IAM, etc.) — all free |
| [Abhishek Veeramalla](https://www.youtube.com/@AbhishekVeeramalla) | "AWS Zero to Hero" playlist — practical, real-world projects |
| [A Cloud Guru](https://www.youtube.com/@ACloudGuru) | Certification prep and concept explanations |
| [TechWorld with Nana](https://www.youtube.com/@TechWorldwithNana) | DevOps + AWS fundamentals, great for beginners |

### 📚 Paid Courses (Worth It)

| Course | Platform | Notes |
|--------|----------|-------|
| [AWS Certified Developer Associate — Stephane Maarek](https://www.udemy.com/course/aws-certified-developer-associate-dva-c01/) | Udemy | Best single course for backend AWS devs. Covers almost your entire list |
| [Production-Ready Serverless — Yan Cui](https://theburningmonk.com/production-ready-serverless-workshop/) | Manning / Workshop | Best resource for serious serverless — real-world patterns, hands-on |

### 🆓 Free Platforms

| Platform | URL | Notes |
|----------|-----|-------|
| AWS Skill Builder | https://skillbuilder.aws | Official AWS learning; free courses per service |
| AWS Documentation | https://docs.aws.amazon.com | Better than expected — read Getting Started + Developer Guides |
| Serverless Land | https://serverlessland.com | Patterns, tutorials, and blog focused on serverless |
| AWS Workshops | https://workshops.aws | Free hands-on labs directly from AWS teams |
| AWS Fundamentals Blog | https://awsfundamentals.com/blog | Practical blog covering IAM, Lambda, CloudWatch in depth |

### 📰 Newsletters & Blogs (Follow These)

| Source | URL | What It Covers |
|--------|-----|----------------|
| Off-by-none (Jeremy Daly) | https://offbynone.io | Weekly curated serverless news — required reading |
| The Burning Monk (Yan Cui) | https://theburningmonk.com | Deep serverless and Lambda guides from an AWS Hero |
| Alex DeBrie | https://alexdebrie.com | DynamoDB — the best writing on this topic anywhere |
| Jeremy Daly Blog | https://www.jeremydaly.com | Architecture and serverless deep dives |
| AWS Blog — Compute | https://aws.amazon.com/blogs/compute | Official Lambda, API Gateway, and serverless updates |
| AWS Blog — Database | https://aws.amazon.com/blogs/database | DynamoDB, ElastiCache, and more |
| Ready, Set, Cloud | https://www.readysetcloud.io/blog | Great diagrams and beginner-friendly AWS tutorials |

### 🧪 Practice & Reference

| Tool | URL | Use |
|------|-----|-----|
| Tutorials Dojo | https://tutorialsdojo.com | Cheat sheets per service, practice exams |
| AWS in Plain English | https://expeditedsecurity.com/aws-in-plain-english | Quick mental model check for any service |
| AWS Workshops | https://workshops.aws | Guided, hands-on labs in your own AWS account |

---

## Phase 1 — AWS Fundamentals & IAM

### Goals
Understand how AWS works as a platform before touching any specific service.

### Topics
- [ ] How AWS accounts, regions, and availability zones work
- [ ] The AWS Console, CLI, and SDK basics *(pick one: Python/Boto3 or Node.js)*
- [ ] Billing basics and the AWS free tier
- [ ] The shared responsibility model

### IAM — Do This First, Always
IAM is the backbone of every AWS service. Nothing works securely without it.

- [ ] Users, groups, and roles
- [ ] Policies — inline vs. managed
- [ ] Least privilege principle
- [ ] Identity-based vs. resource-based policies
- [ ] How services assume roles to talk to each other

### 📺 Videos
- [AWS IAM Tutorial for Beginners — freeCodeCamp YouTube](https://www.youtube.com/results?search_query=AWS+IAM+tutorial+freeCodeCamp) — free, complete beginner walkthrough
- [AWS IAM Deep Dive — Abhishek Veeramalla (Day 2, Zero to Hero)](https://www.youtube.com/@AbhishekVeeramalla) — practical with real demos
- [AWS re:Invent — IAM Best Practices](https://www.youtube.com/results?search_query=AWS+reinvent+IAM+best+practices) — watch at least one re:Invent IAM talk

### 📖 Docs & Reading
- [IAM Getting Started — AWS Docs](https://docs.aws.amazon.com/IAM/latest/UserGuide/getting-started.html)
- [IAM Best Practices — AWS Docs](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html)
- [IAM Policies Deep Dive — AWS Fundamentals Blog](https://awsfundamentals.com/blog) *(search "IAM policies")*

### Practice
- Create an AWS free-tier account
- Set up the AWS CLI with a non-root IAM user
- Write a policy that grants S3 read-only access and attach it to a test user

### Key Question From This Point Forward
> *"How does IAM control access to this service?"* — ask this for every new service.

---

## Phase 2 — Core Compute & Storage

### Goals
Build the foundational mental model for cloud servers, storage, and delivery that everything else builds on.

---

### EC2

- [ ] Instance types and when to use them
- [ ] Security groups and inbound/outbound rules
- [ ] Key pairs and SSH access
- [ ] Elastic IPs
- [ ] Stop vs. terminate
- [ ] Nginx as a reverse proxy — routing public traffic to your app's local port
- [ ] Running the app as a persistent systemd service

#### 📺 Videos
- [EC2 Crash Course — freeCodeCamp](https://www.youtube.com/results?search_query=EC2+crash+course+aws+freeCodeCamp)
- [EC2 Tutorial — Stephane Maarek Udemy Course](https://www.udemy.com/course/aws-certified-developer-associate-dva-c01/) *(best structured EC2 coverage)*
- [AWS EC2 Explained — Abhishek Veeramalla Zero to Hero](https://www.youtube.com/@AbhishekVeeramalla)
- [Hosting FastAPI application in EC2](https://www.youtube.com/watch?v=SgSnz7kW-Ko) — covers Nginx + systemd deployment end to end

#### 📖 Docs & Reading
- [EC2 Getting Started — AWS Docs](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/EC2_GetStarted.html)
- [EC2 Instance Types — AWS](https://aws.amazon.com/ec2/instance-types/)
- [Nginx Beginner's Guide](https://nginx.org/en/docs/beginners_guide.html) — reverse proxy configuration

#### Practice
Deploy a FastAPI application on EC2: configure Nginx as a reverse proxy on port 80, run the app with uvicorn on port 8000, and keep it alive across reboots using a systemd service.

---

### S3

- [ ] Buckets, objects, and key structure
- [ ] Bucket policies vs. ACLs
- [ ] Presigned URLs *(very common in backend work)*
- [ ] Versioning and lifecycle rules
- [ ] S3 event notifications *(previews Lambda triggers)*

#### 📺 Videos
- [S3 Tutorial for Beginners — AWS Online Tech Talks](https://www.youtube.com/results?search_query=amazon+s3+tutorial+beginners+AWS+Tech+Talks)
- [S3 Deep Dive — Abhishek Veeramalla Zero to Hero](https://www.youtube.com/@AbhishekVeeramalla)
- [S3 Crash Course — freeCodeCamp](https://www.youtube.com/results?search_query=amazon+s3+crash+course+freeCodeCamp)

#### 📖 Docs & Reading
- [S3 Developer Guide — AWS Docs](https://docs.aws.amazon.com/AmazonS3/latest/userguide/Welcome.html)
- [S3 Presigned URLs — AWS Docs](https://docs.aws.amazon.com/AmazonS3/latest/userguide/PresignedUrlUploadObject.html)

#### Practice
Upload and retrieve files programmatically using the AWS SDK.

---

### CloudFront

- [ ] What CloudFront is — CDN and global edge delivery
- [ ] Distributions and origins (S3, EC2, ALB, API Gateway)
- [ ] Cache behaviours and TTL
- [ ] HTTPS with ACM certificates
- [ ] Invalidations — clearing cached content
- [ ] Restricting S3 bucket access to CloudFront only (OAC)

#### 📺 Videos
- [Amazon CloudFront Tutorial — AWS Online Tech Talks](https://www.youtube.com/results?search_query=amazon+cloudfront+tutorial+aws+tech+talks)
- [CloudFront with S3 Static Website — Tutorial](https://www.youtube.com/results?search_query=cloudfront+s3+static+website+aws+tutorial)

#### 📖 Docs & Reading
- [CloudFront Developer Guide — AWS Docs](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/Introduction.html)
- [CloudFront with S3 — AWS Docs](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/GettingStartedCreateDistribution.html)

#### Practice
Serve your S3-hosted static files through a CloudFront distribution with HTTPS enabled.

---

### CloudWatch

- [ ] Log groups and log streams
- [ ] Metrics and dashboards
- [ ] Alarms and notifications
- [ ] CloudWatch Logs Insights query language

#### 📺 Videos
- [Amazon CloudWatch Tutorial — AWS Online Tech Talks](https://www.youtube.com/results?search_query=amazon+cloudwatch+tutorial+tech+talks)
- [CloudWatch for Developers — freeCodeCamp](https://www.youtube.com/results?search_query=cloudwatch+aws+tutorial+freeCodeCamp)
- [CloudWatch Logs Insights Demo — AWS Official](https://www.youtube.com/results?search_query=cloudwatch+logs+insights+demo+aws+official)

#### 📖 Docs & Reading
- [CloudWatch Getting Started — AWS Docs](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/GettingStarted.html)
- [CloudWatch Logs Insights Syntax — AWS Docs](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/CWL_QuerySyntax.html)
- [Complete CloudWatch Guide — AWS Fundamentals Blog](https://awsfundamentals.com/blog) *(search "CloudWatch complete guide")*
- [CloudWatch Alarms Best Practices — AWS Fundamentals Blog](https://awsfundamentals.com/blog) *(search "CloudWatch alarms")*

#### Practice
Set up a CloudWatch alarm that fires when EC2 CPU usage exceeds 80%.

---

## Phase 3 — Serverless Core & Dev Tooling

### Goals
Understand the serverless execution model, build your first real API, and deploy infrastructure as code.

---

### Lambda

- [ ] Execution model — how Lambda runs your code
- [ ] Cold starts and how to minimize them
- [ ] Memory, timeout, and concurrency settings
- [ ] Deployment: Console → CLI → SAM *(in that order)*

#### 📺 Videos
- [AWS Lambda Tutorial for Beginners — freeCodeCamp](https://www.youtube.com/results?search_query=AWS+Lambda+tutorial+beginners+freeCodeCamp)
- [Lambda Cold Starts Explained — Yan Cui / Burning Monk](https://www.youtube.com/results?search_query=lambda+cold+starts+yan+cui)
- [How Lambda Works Internally — AWS re:Invent](https://www.youtube.com/results?search_query=how+AWS+lambda+works+internally+reinvent)
- [Stephane Maarek — Lambda section](https://www.udemy.com/course/aws-certified-developer-associate-dva-c01/)

#### 📖 Docs & Reading
- [Lambda Developer Guide — AWS Docs](https://docs.aws.amazon.com/lambda/latest/dg/welcome.html)
- [Lambda Best Practices — AWS Docs](https://docs.aws.amazon.com/lambda/latest/dg/best-practices.html)
- [Lambda Timeout Reasons & Fixes — AWS Fundamentals Blog](https://awsfundamentals.com/blog) *(search "Lambda timeout")*
- [Lambda Power Tuning Tool — GitHub](https://github.com/alexcasalboni/aws-lambda-power-tuning) *(optimize memory vs. cost)*
- [Lambda Best Practices — The Burning Monk](https://theburningmonk.com) *(search "Lambda best practices")*

#### Practice
Write a Lambda that reads a file from S3 and logs its content to CloudWatch.

---

### API Gateway

- [ ] REST APIs vs. HTTP APIs *(prefer HTTP APIs — simpler and cheaper)*
- [ ] Routes and methods
- [ ] Lambda proxy integration
- [ ] Stages and deployments
- [ ] CORS configuration

#### 📺 Videos
- [API Gateway Full Tutorial — freeCodeCamp](https://www.youtube.com/results?search_query=API+gateway+lambda+tutorial+freeCodeCamp)
- [REST vs HTTP API Explained — AWS Online Tech Talks](https://www.youtube.com/results?search_query=API+gateway+REST+vs+HTTP+API+AWS)
- [Stephane Maarek — API Gateway section](https://www.udemy.com/course/aws-certified-developer-associate-dva-c01/)

#### 📖 Docs & Reading
- [API Gateway Developer Guide — AWS Docs](https://docs.aws.amazon.com/apigateway/latest/developerguide/welcome.html)
- [Build a CRUD HTTP API — AWS Official Tutorial](https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-dynamo-db.html) *(API Gateway + Lambda + DynamoDB — excellent hands-on)*
- [Lambda + API Gateway Tutorial — AWS Docs](https://docs.aws.amazon.com/lambda/latest/dg/services-apigateway-tutorial.html)
- [API Gateway + Lambda + DynamoDB — Medium / Netlify Guide](https://www.netlify.com/guides/creating-an-api-with-aws-lambda-dynamodb-and-api-gateway/)

#### Practice
Build a simple CRUD API with API Gateway + Lambda *(mock data, no database yet)*.

---

### AWS SAM (Serverless Application Model)

- [ ] What Infrastructure as Code (IaC) is and why it matters
- [ ] SAM template structure (`template.yaml`)
- [ ] Defining Lambdas, APIs, and permissions in SAM
- [ ] `sam build`, `sam deploy`, `sam local invoke`

#### 📺 Videos
- [AWS SAM Full Tutorial — AWS Official Channel](https://www.youtube.com/results?search_query=AWS+SAM+serverless+application+model+tutorial+official)
- [Build Serverless Apps with SAM — AWS Online Tech Talks](https://www.youtube.com/results?search_query=build+serverless+app+SAM+AWS+tech+talks)
- [SAM Local Development — AWS Demo](https://www.youtube.com/results?search_query=AWS+SAM+local+invoke+demo)

#### 📖 Docs & Reading
- [AWS SAM Developer Guide — AWS Docs](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/what-is-sam.html)
- [AWS SAM CLI Reference](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-command-reference.html)
- [Serverless Land — SAM Patterns and Examples](https://serverlessland.com/patterns) *(real-world SAM templates)*
- [Node REST API with SAM — Serverless.com Blog](https://www.serverless.com/blog/node-rest-api-with-serverless-lambda-and-dynamodb)
- [AWS Serverless Ramp-Up Guide — AWS PDF](https://d1.awsstatic.com/training-and-certification/ramp-up_guides/Ramp-Up_Guide_Serverless.pdf) *(official AWS learning path)*

#### Practice
Rebuild your API Gateway + Lambda project using SAM instead of the console.

---

### CloudFormation

SAM is built on top of CloudFormation. Learning CloudFormation gives you full control over any AWS resource — not just serverless.

- [ ] How CloudFormation relates to SAM — SAM transforms into CloudFormation
- [ ] Template anatomy — `Resources`, `Parameters`, `Outputs`, `Mappings`
- [ ] Stacks — create, update, delete
- [ ] Change sets — preview changes before applying them
- [ ] Drift detection
- [ ] Nested stacks for large projects

#### 📺 Videos
- [AWS CloudFormation Tutorial — AWS Online Tech Talks](https://www.youtube.com/results?search_query=AWS+cloudformation+tutorial+tech+talks)
- [CloudFormation for Beginners — freeCodeCamp](https://www.youtube.com/results?search_query=cloudformation+beginners+freeCodeCamp)

#### 📖 Docs & Reading
- [CloudFormation User Guide — AWS Docs](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/Welcome.html)
- [CloudFormation Template Reference — AWS Docs](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/template-reference.html)

#### Practice
Deploy an S3 bucket and IAM role using a raw CloudFormation template (without SAM).

---

### AWS CDK (Cloud Development Kit)

Write your infrastructure in Python, TypeScript, or Java instead of YAML.

- [ ] What CDK is and how it differs from CloudFormation/SAM
- [ ] Constructs — L1, L2, L3 levels
- [ ] `cdk init`, `cdk synth`, `cdk deploy`
- [ ] Stacks and apps
- [ ] CDK vs. SAM — when to choose which

#### 📺 Videos
- [AWS CDK Full Tutorial — AWS Official Channel](https://www.youtube.com/results?search_query=AWS+CDK+tutorial+official+2024)
- [CDK Python Tutorial — Abhishek Veeramalla](https://www.youtube.com/@AbhishekVeeramalla)

#### 📖 Docs & Reading
- [CDK Getting Started — AWS Docs](https://docs.aws.amazon.com/cdk/v2/guide/getting_started.html)
- [CDK API Reference](https://docs.aws.amazon.com/cdk/api/v2/)

#### Practice
Rewrite one of your SAM stacks using CDK in Python.

---

### AWS Toolkit (IDE Extension)

AWS Toolkit is a free extension for VS Code and JetBrains IDEs that brings Lambda, SAM, and CloudFormation development directly into your editor.

- [ ] Install the AWS Toolkit extension
- [ ] Browse deployed Lambda functions from the IDE
- [ ] Invoke Lambda functions locally without leaving the editor
- [ ] Edit and visualise SAM/CloudFormation templates

#### 📖 Docs & Reading
- [AWS Toolkit for VS Code — AWS Docs](https://docs.aws.amazon.com/toolkit-for-vscode/latest/userguide/welcome.html)

---

## Phase 4 — Containers

### Goals
Run containerised workloads on AWS — from fully managed serverless containers (Fargate) to Kubernetes (EKS).

---

### ECS (Elastic Container Service)

- [ ] Clusters, services, and tasks
- [ ] EC2 launch type vs. Fargate *(prefer Fargate — no server management)*
- [ ] Task definitions and container definitions
- [ ] IAM roles for tasks
- [ ] Load balancing with an Application Load Balancer (ALB)
- [ ] Service auto-scaling
- [ ] ECR (Elastic Container Registry) — storing your Docker images on AWS

#### 📺 Videos
- [AWS ECS Tutorial for Beginners — TechWorld with Nana](https://www.youtube.com/results?search_query=AWS+ECS+tutorial+beginners+TechWorld+with+Nana)
- [ECS Fargate Deep Dive — AWS Online Tech Talks](https://www.youtube.com/results?search_query=ECS+fargate+deep+dive+AWS+tech+talks)
- [ECS vs Lambda — When to Use What](https://www.youtube.com/results?search_query=ECS+vs+Lambda+AWS+when+to+use)
- [Deploy FastAPI to ECS — Tutorial](https://www.youtube.com/results?search_query=deploy+fastapi+docker+ECS+fargate+tutorial)

#### 📖 Docs & Reading
- [ECS Developer Guide — AWS Docs](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/Welcome.html)
- [ECS Fargate Getting Started — AWS Docs](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/getting-started-fargate.html)
- [ECR User Guide — AWS Docs](https://docs.aws.amazon.com/AmazonECR/latest/userguide/what-is-ecr.html)

#### Practice
Containerise your FastAPI app with Docker, push the image to ECR, and deploy it to ECS Fargate behind an ALB.

---

### EKS (Elastic Kubernetes Service)

> Learn ECS first. EKS is for teams already running Kubernetes — if k8s is new to you, treat this as a later-stage topic.

- [ ] Kubernetes fundamentals — pods, deployments, services, namespaces
- [ ] EKS cluster creation with `eksctl`
- [ ] Managed node groups vs. Fargate profiles
- [ ] `kubectl` with EKS
- [ ] IAM Roles for Service Accounts (IRSA) — the EKS equivalent of ECS task roles
- [ ] Helm chart deployments

#### 📺 Videos
- [Kubernetes Crash Course — TechWorld with Nana](https://www.youtube.com/results?search_query=kubernetes+crash+course+TechWorld+with+Nana)
- [AWS EKS Tutorial — Abhishek Veeramalla Zero to Hero](https://www.youtube.com/@AbhishekVeeramalla)
- [EKS Getting Started — AWS Official](https://www.youtube.com/results?search_query=AWS+EKS+getting+started+tutorial+official)

#### 📖 Docs & Reading
- [EKS User Guide — AWS Docs](https://docs.aws.amazon.com/eks/latest/userguide/what-is-eks.html)
- [eksctl Documentation](https://eksctl.io) — simplest way to provision EKS clusters

#### Practice
Deploy a containerised service to EKS using `eksctl` and expose it via a Kubernetes LoadBalancer service.

---

## Phase 5 — Data & Caching

### Goals
Add persistent storage and caching to your backend.

---

### DynamoDB

- [ ] Core concepts: tables, items, attributes
- [ ] Partition keys and sort keys
- [ ] On-demand vs. provisioned capacity
- [ ] Single-table design thinking *(major mental shift from SQL — take your time here)*
- [ ] Global Secondary Indexes (GSIs)
- [ ] DynamoDB Streams
- [ ] DynamoDB Document Client (SDK)

#### 📺 Videos
- [DynamoDB Full Course for Beginners — freeCodeCamp](https://www.youtube.com/results?search_query=DynamoDB+full+course+beginners+freeCodeCamp)
- [Data Modeling with DynamoDB — AWS re:Invent 2021 (Alex DeBrie)](https://www.youtube.com/results?search_query=data+modeling+dynamodb+reinvent+2021+alex+debrie) ⭐ *Essential watch*
- [DynamoDB Under the Hood — AWS re:Invent 2018](https://www.youtube.com/results?search_query=dynamodb+under+the+hood+reinvent+2018) ⭐ *Excellent mental model builder*
- [Single-Table Design — Rick Houlihan re:Invent](https://www.youtube.com/results?search_query=rick+houlihan+dynamodb+reinvent+single+table) ⭐ *Mind-bending but worth it*
- [Stephane Maarek — DynamoDB section](https://www.udemy.com/course/aws-certified-developer-associate-dva-c01/)

#### 📖 Docs & Reading
- [DynamoDB Developer Guide — AWS Docs](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Introduction.html)
- [DynamoDB Guide — dynamodbguide.com](https://www.dynamodbguide.com) ⭐ *Free, comprehensive, best written guide — by Alex DeBrie*
- [The What, Why, and When of Single-Table Design — Alex DeBrie](https://www.alexdebrie.com/posts/dynamodb-single-table/) ⭐ *Required reading*
- [Single-table vs Multi-table — AWS Database Blog](https://aws.amazon.com/blogs/database/single-table-vs-multi-table-design-in-amazon-dynamodb/)
- [Awesome DynamoDB — GitHub curated list](https://github.com/alexdebrie/awesome-dynamodb) ⭐ *All DynamoDB resources in one place*
- [From Relational DB to Single DynamoDB Table — Trek10 Blog](https://www.trek10.com/blog/dynamodb-single-table-relational-modeling) *(great for SQL developers)*
- [NoSQL Workbench for DynamoDB — AWS Tool](https://aws.amazon.com/dynamodb/nosql-workbench/) *(visual table designer — use this while learning)*

#### 📗 Book
- [The DynamoDB Book — Alex DeBrie](https://dynamodbbook.com) — 450+ pages, five full walkthrough examples. The single best resource on DynamoDB data modeling that exists. Worth every cent.

#### Practice
Model a real-world entity (e.g. users + their orders) in a single DynamoDB table and query it from Lambda.

---

### DocumentDB

Amazon DocumentDB is AWS's managed MongoDB-compatible document database. Use it when your data is naturally document-shaped or when migrating an existing MongoDB workload.

- [ ] When to choose DocumentDB vs. DynamoDB (document/JSON workloads, MongoDB migrations)
- [ ] Clusters and replica instances
- [ ] Connecting with MongoDB-compatible drivers (`pymongo`)
- [ ] Collections, documents, and indexes
- [ ] VPC-only access — no public endpoint, must be in the same VPC

#### 📺 Videos
- [Amazon DocumentDB Tutorial — AWS Online Tech Talks](https://www.youtube.com/results?search_query=amazon+documentdb+tutorial+aws+tech+talks)

#### 📖 Docs & Reading
- [DocumentDB Developer Guide — AWS Docs](https://docs.aws.amazon.com/documentdb/latest/developerguide/what-is.html)
- [DocumentDB vs DynamoDB — AWS Blog](https://aws.amazon.com/blogs/database/how-to-determine-if-amazon-dynamodb-is-appropriate-for-your-needs-and-then-plan-your-migration/)

#### Practice
Create a DocumentDB cluster and perform CRUD operations using `pymongo` from a Lambda inside the same VPC.

---

### OpenSearch

Amazon OpenSearch Service (formerly Elasticsearch Service) is AWS's managed search and analytics engine. Best for full-text search, log analytics, and Kibana-style dashboards.

- [ ] When to use OpenSearch — full-text search, log analysis, dashboards
- [ ] Domains, nodes, and shards
- [ ] Indexing and querying documents via the REST API
- [ ] OpenSearch Dashboards (replaces Kibana)
- [ ] Ingesting CloudWatch Logs into OpenSearch via subscription filters

#### 📺 Videos
- [Amazon OpenSearch Service Tutorial — AWS Online Tech Talks](https://www.youtube.com/results?search_query=amazon+opensearch+service+tutorial+aws+tech+talks)

#### 📖 Docs & Reading
- [OpenSearch Service Developer Guide — AWS Docs](https://docs.aws.amazon.com/opensearch-service/latest/developerguide/what-is.html)

#### Practice
Index your application logs in an OpenSearch domain and build a search dashboard.

---

### ElastiCache & Redis

- [ ] Why caching exists (reduce DB load, speed up reads)
- [ ] ElastiCache as managed Redis on AWS
- [ ] Cache-aside pattern *(check cache → miss → fetch DB → populate cache)*
- [ ] TTL (time-to-live) and cache invalidation
- [ ] Connecting Lambda to ElastiCache *(VPC considerations)*
- [ ] When not to cache

#### 📺 Videos
- [AWS ElastiCache Tutorial — AWS Online Tech Talks](https://www.youtube.com/results?search_query=AWS+ElastiCache+tutorial+redis+tech+talks)
- [Redis Caching Explained — Fireship](https://www.youtube.com/results?search_query=redis+caching+explained+fireship) *(great quick intro to Redis concepts)*
- [Lambda + ElastiCache + VPC — AWS re:Invent](https://www.youtube.com/results?search_query=lambda+elasticache+redis+vpc+reinvent)

#### 📖 Docs & Reading
- [ElastiCache for Redis Developer Guide — AWS Docs](https://docs.aws.amazon.com/AmazonElastiCache/latest/red-ug/WhatIs.html)
- [Caching Strategies Guide — AWS Docs](https://docs.aws.amazon.com/AmazonElastiCache/latest/red-ug/Strategies.html) *(covers cache-aside, write-through, and lazy loading)*
- [Lambda + ElastiCache for DynamoDB — AWS Blog](https://aws.amazon.com/blogs/compute/using-amazon-elasticache-for-redis-as-a-cache-for-amazon-dynamodb/)

#### Practice
Add a Redis caching layer in front of a DynamoDB query in your Lambda function.

---

## Phase 6 — Networking

### Goals
Understand how AWS networks your infrastructure — isolate resources with VPC, route traffic with Route 53, and secure it with free TLS certificates from ACM.

---

### VPC (Virtual Private Cloud)

- [ ] What a VPC is — a logically isolated network inside AWS
- [ ] Subnets — public vs. private
- [ ] Route tables and internet gateways
- [ ] NAT Gateway — private subnets calling out to the internet
- [ ] Security Groups vs. Network ACLs
- [ ] VPC Endpoints — access AWS services without leaving AWS network
- [ ] VPC Peering
- [ ] Connecting Lambda and ElastiCache/RDS via VPC

#### 📺 Videos
- [AWS VPC Tutorial for Beginners — freeCodeCamp](https://www.youtube.com/results?search_query=AWS+VPC+tutorial+beginners+freeCodeCamp)
- [VPC Deep Dive — Abhishek Veeramalla Zero to Hero](https://www.youtube.com/@AbhishekVeeramalla)
- [AWS Networking Fundamentals — AWS Online Tech Talks](https://www.youtube.com/results?search_query=AWS+networking+fundamentals+VPC+tech+talks)

#### 📖 Docs & Reading
- [VPC Getting Started — AWS Docs](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-getting-started.html)
- [VPC User Guide — AWS Docs](https://docs.aws.amazon.com/vpc/latest/userguide/what-is-amazon-vpc.html)

#### Practice
Build a VPC with a public subnet (for EC2/load balancer) and a private subnet (for RDS/ElastiCache). Verify the private subnet cannot be reached directly from the internet.

---

### Route 53

- [ ] What Route 53 is — DNS + health checking + traffic routing
- [ ] Hosted zones and record types (A, CNAME, ALIAS)
- [ ] Routing policies — simple, weighted, latency-based, failover
- [ ] Domain registration or transfer
- [ ] Pointing a domain to EC2, CloudFront, ALB, or API Gateway

#### 📺 Videos
- [AWS Route 53 Tutorial — AWS Online Tech Talks](https://www.youtube.com/results?search_query=AWS+Route+53+tutorial+tech+talks)
- [Route 53 with Custom Domain and EC2 — Tutorial](https://www.youtube.com/results?search_query=AWS+Route+53+custom+domain+EC2+tutorial)

#### 📖 Docs & Reading
- [Route 53 Developer Guide — AWS Docs](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/Welcome.html)

#### Practice
Point a custom domain in Route 53 to your EC2 instance or CloudFront distribution.

---

### AWS Certificate Manager (ACM)

- [ ] What ACM is — free, managed TLS/SSL certificates for AWS services
- [ ] Issuing public certificates (DNS validation or email validation)
- [ ] Attaching certificates to CloudFront, ALB, and API Gateway
- [ ] Automatic certificate renewal

#### 📖 Docs & Reading
- [ACM User Guide — AWS Docs](https://docs.aws.amazon.com/acm/latest/userguide/acm-overview.html)

#### Practice
Issue a free ACM certificate for your domain and attach it to your CloudFront distribution to serve your app over HTTPS.

---

## Phase 7 — Security & Secrets

### Goals
Handle credentials and user authentication the right way.

---

### Secrets Manager

- [ ] Storing secrets: DB credentials, API keys, tokens
- [ ] Fetching secrets from Lambda at runtime
- [ ] Automatic secret rotation
- [ ] Secrets Manager vs. SSM Parameter Store *(know the difference)*

#### 📺 Videos
- [AWS Secrets Manager Tutorial — AWS Online Tech Talks](https://www.youtube.com/results?search_query=AWS+secrets+manager+tutorial+tech+talks)
- [Secrets Manager vs Parameter Store — Be a Better Dev](https://www.youtube.com/results?search_query=secrets+manager+vs+parameter+store+aws+be+a+better+dev)

#### 📖 Docs & Reading
- [Secrets Manager User Guide — AWS Docs](https://docs.aws.amazon.com/secretsmanager/latest/userguide/intro.html)
- [Use Secrets Manager in Lambda — AWS Docs](https://docs.aws.amazon.com/secretsmanager/latest/userguide/retrieving-secrets_lambda.html)
- [Secrets Manager vs Parameter Store — AWS Blog](https://aws.amazon.com/blogs/mt/the-right-way-to-store-secrets-using-parameter-store/)

#### Practice
Move all hardcoded credentials in your Lambda functions into Secrets Manager and retrieve them at runtime.

---

### AWS Cognito

- [ ] **User Pools** — authentication (sign up, sign in, JWTs)
- [ ] **Identity Pools** — authorization (granting AWS resource access)
- [ ] JWT tokens — ID token vs. Access token vs. Refresh token
- [ ] Cognito Authorizer in API Gateway
- [ ] Lambda triggers *(pre sign-up, post-confirmation, etc.)*
- [ ] Hosted UI vs. custom auth flows

#### 📺 Videos
- [AWS Cognito Full Course — freeCodeCamp](https://www.freecodecamp.org/news/learn-aws-incognito-for-authentication) ⭐ *Free, beginner to expert. Covers User Pools, Identity Pools, OAuth 2.0, JWTs, React/Node.js integration — the best free Cognito course*
- [Cognito + API Gateway Authorizer — Tutorial](https://www.youtube.com/results?search_query=aws+cognito+api+gateway+authorizer+tutorial)
- [Stephane Maarek — Cognito section](https://www.udemy.com/course/aws-certified-developer-associate-dva-c01/)

#### 📖 Docs & Reading
- [Cognito Developer Guide — AWS Docs](https://docs.aws.amazon.com/cognito/latest/developerguide/what-is-amazon-cognito.html)
- [Using Cognito with API Gateway — AWS Docs](https://docs.aws.amazon.com/apigateway/latest/developerguide/apigateway-integrate-with-cognito.html)
- [Cognito JWT Token Validation — AWS Docs](https://docs.aws.amazon.com/cognito/latest/developerguide/amazon-cognito-user-pools-using-tokens-verifying-a-jwt.html)
- [Secure API with Cognito + Lambda — freeCodeCamp Article](https://www.freecodecamp.org/news/how-to-securely-deploy-apis-to-amazon-lambda-a-practical-guide/)

#### Practice
Protect your API Gateway endpoints with a Cognito User Pool Authorizer. Only authenticated users should be able to call your API.

---

## Phase 8 — Events & Orchestration

### Goals
Decouple services with async messaging and coordinate multi-step workflows.

---

### SQS (Simple Queue Service)

- [ ] Queues — Standard vs. FIFO
- [ ] Producers, consumers, and visibility timeout
- [ ] Dead-letter queues (DLQ)
- [ ] Lambda as an SQS consumer
- [ ] Long polling vs. short polling

#### 📺 Videos
- [AWS SQS Tutorial — AWS Online Tech Talks](https://www.youtube.com/results?search_query=AWS+SQS+tutorial+tech+talks)
- [SQS + Lambda Trigger — Tutorial](https://www.youtube.com/results?search_query=SQS+lambda+trigger+AWS+tutorial)

#### 📖 Docs & Reading
- [SQS Developer Guide — AWS Docs](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/welcome.html)

#### Practice
Create an SQS queue and trigger a Lambda function to process each message.

---

### SNS (Simple Notification Service)

- [ ] Topics and subscriptions
- [ ] Fan-out pattern — one SNS topic, multiple SQS queues
- [ ] Email, SMS, HTTP/S, and Lambda subscribers
- [ ] Message filtering with subscription filter policies

#### 📺 Videos
- [AWS SNS Tutorial — AWS Online Tech Talks](https://www.youtube.com/results?search_query=AWS+SNS+tutorial+tech+talks)

#### 📖 Docs & Reading
- [SNS Developer Guide — AWS Docs](https://docs.aws.amazon.com/sns/latest/dg/welcome.html)

#### Practice
Set up an SNS topic that fans out to both an SQS queue and an email subscription simultaneously.

---

### EventBridge

- [ ] Events, buses, and rules
- [ ] AWS-native events vs. custom application events
- [ ] Event patterns and filtering
- [ ] Targets — Lambda, SQS, Step Functions, and more
- [ ] Scheduled events (replaces cron on CloudWatch Events)

#### 📺 Videos
- [AWS EventBridge Tutorial — AWS Online Tech Talks](https://www.youtube.com/results?search_query=AWS+EventBridge+tutorial+tech+talks)

#### 📖 Docs & Reading
- [EventBridge User Guide — AWS Docs](https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-what-is.html)

#### Practice
Emit a custom event when a new item is created in DynamoDB and route it to a Lambda handler via EventBridge.

---

### Step Functions

- [ ] What Step Functions is — orchestrate Lambda chains into reliable workflows
- [ ] State machines — states, transitions, inputs/outputs
- [ ] State types: Task, Choice, Wait, Parallel, Map
- [ ] Standard vs. Express workflows
- [ ] Error handling and automatic retries
- [ ] Integrating with Lambda, DynamoDB, SQS, and SNS

#### 📺 Videos
- [AWS Step Functions Tutorial — AWS Online Tech Talks](https://www.youtube.com/results?search_query=AWS+Step+Functions+tutorial+tech+talks)
- [Step Functions + Lambda Workflow — AWS Demo](https://www.youtube.com/results?search_query=AWS+Step+Functions+lambda+workflow+demo)

#### 📖 Docs & Reading
- [Step Functions Developer Guide — AWS Docs](https://docs.aws.amazon.com/step-functions/latest/dg/welcome.html)

#### Practice
Build a multi-step order processing workflow: validate → process payment → send confirmation email, using Step Functions + Lambda + SES.

---

### Kinesis *(awareness only)*

> Kinesis is AWS's real-time data streaming platform. Not essential for most backend apps, but worth knowing it exists for high-throughput streaming use cases.

- [ ] Kinesis Data Streams — real-time event streaming at scale
- [ ] Kinesis Data Firehose — load streams directly into S3, OpenSearch, or Redshift
- [ ] When to choose Kinesis vs. SQS

#### 📖 Docs & Reading
- [Kinesis Data Streams Overview — AWS Docs](https://docs.aws.amazon.com/streams/latest/dev/introduction.html)

---

## Phase 9 — Observability & Communication

### Goals
Trace requests across services and send transactional emails.

---

### AWS X-Ray

- [ ] What distributed tracing is and why it matters
- [ ] Instrumenting Lambda with the X-Ray SDK
- [ ] Reading the X-Ray service map
- [ ] Identifying latency bottlenecks
- [ ] Segments and subsegments

#### 📺 Videos
- [AWS X-Ray Introduction — AWS Online Tech Talks](https://www.youtube.com/results?search_query=AWS+X-Ray+tutorial+introduction+tech+talks)
- [X-Ray with Lambda — AWS re:Invent](https://www.youtube.com/results?search_query=AWS+x-ray+lambda+distributed+tracing+reinvent)
- [Debugging Serverless with X-Ray — Yan Cui](https://www.youtube.com/results?search_query=debugging+serverless+x-ray+yan+cui)

#### 📖 Docs & Reading
- [X-Ray Developer Guide — AWS Docs](https://docs.aws.amazon.com/xray/latest/devguide/aws-xray.html)
- [X-Ray with Lambda — AWS Docs](https://docs.aws.amazon.com/lambda/latest/dg/services-xray.html)
- [X-Ray Cheat Sheet — Tutorials Dojo](https://tutorialsdojo.com/aws-x-ray/)
- [Troubleshooting Serverless — Yan Cui / Burning Monk](https://theburningmonk.com) *(search "X-Ray" or "distributed tracing")*

#### Practice
Enable X-Ray on your full API (API Gateway → Lambda → DynamoDB) and trace a slow query end to end.

---

### SES (Simple Email Service)

- [ ] Verifying identities and domains
- [ ] Sending transactional emails from Lambda
- [ ] Handling bounces and complaints *(critical in production)*
- [ ] Moving out of the SES sandbox
- [ ] Email templates

#### 📺 Videos
- [AWS SES Tutorial — AWS Online Tech Talks](https://www.youtube.com/results?search_query=AWS+SES+tutorial+simple+email+service)
- [Send Emails from Lambda with SES — Tutorial](https://www.youtube.com/results?search_query=send+email+AWS+lambda+SES+tutorial)

#### 📖 Docs & Reading
- [SES Developer Guide — AWS Docs](https://docs.aws.amazon.com/ses/latest/dg/Welcome.html)
- [Sending Email with SES — AWS Docs](https://docs.aws.amazon.com/ses/latest/dg/sending-email.html)
- [SES Bounces and Complaints Handling — AWS Docs](https://docs.aws.amazon.com/ses/latest/dg/monitor-using-event-publishing.html)

#### Practice
Trigger a welcome email via a Cognito post-confirmation Lambda trigger using SES.

---

## Phase 10 — Capstone Project

### Goal
Build a real project that connects every service and surfaces gaps in your knowledge.

### Project Idea: Serverless Backend API

Build a backend API for a simple app (e.g. a task manager or e-commerce backend):

```
Request
  └── Route 53 (custom domain)
        └── CloudFront (CDN + HTTPS via ACM)
              └── API Gateway (HTTP API)
                    └── Cognito Authorizer (authentication)
                          └── Lambda (business logic)
                                ├── DynamoDB (primary storage)
                                ├── ElastiCache / Redis (caching layer)
                                ├── Secrets Manager (credentials)
                                ├── SES (transactional emails)
                                ├── S3 (file storage)
                                └── SQS / EventBridge (async events)

Orchestration:
  └── Step Functions (multi-step workflows)

Observability:
  ├── CloudWatch (logs & metrics)
  └── X-Ray (distributed tracing)

Infrastructure:
  └── SAM or CDK (deployed as code)

Containers (optional variation):
  └── ECS Fargate (deploy as a container instead of Lambda)
```

### Capstone Checklist
- [ ] All infrastructure defined as code with SAM or CDK
- [ ] All secrets in Secrets Manager — nothing hardcoded
- [ ] All endpoints protected by Cognito
- [ ] Custom domain via Route 53 + HTTPS via ACM + CloudFront
- [ ] CloudWatch alarms set for errors and high latency
- [ ] X-Ray tracing enabled across all services
- [ ] At least one async flow (e.g. welcome email on sign-up via SES)
- [ ] Redis caching on at least one high-read endpoint
- [ ] Clean up all resources after testing *(avoid surprise bills)*

### 📖 Capstone Resources
- [AWS Workshops — Serverless Workshop](https://workshops.aws) — search "serverless" for guided full-stack serverless labs
- [Serverless Land Patterns](https://serverlessland.com/patterns) — real-world architecture patterns for reference
- [AWS Well-Architected Serverless Lens](https://docs.aws.amazon.com/wellarchitected/latest/serverless-applications-lens/welcome.html) — production quality checklist from AWS

---

## ➕ Awareness — Services to Know Exist

These are useful to know about but not essential to go deep on for standard backend development.

| Service | Category | Notes |
|---------|----------|-------|
| **RDS** | Database | Managed SQL (PostgreSQL, MySQL, Aurora). Use when your project genuinely needs a relational DB. [RDS Getting Started — AWS Docs](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_GettingStarted.html) |
| **Elastic Beanstalk** | Compute | PaaS — deploys apps automatically. Not really needed; EC2 + ECS give you more control and are more widely used. |
| **App Runner** | Compute | Simplified container deployment from source code or an image. Not really needed; ECS Fargate is more flexible and better understood by teams. |

---

## 📗 Recommended Books

| Book | Author | Why |
|------|--------|-----|
| [The DynamoDB Book](https://dynamodbbook.com) | Alex DeBrie | The definitive guide to DynamoDB data modeling. Essential for anyone using DynamoDB seriously. |
| [Production-Ready Serverless](https://www.manning.com/livevideo/production-ready-serverless) | Yan Cui | Operational best practices for Lambda and serverless in production — covers the things courses skip. |

---

## 🧠 Core Mindset Rules

1. **Always ask:** *"How does IAM control access to this?"* — for every new service.
2. **Always ask:** *"How do I see what went wrong?"* — CloudWatch logs and X-Ray traces.
3. **Build things, break them, read the logs.** That is the fastest way through this list.
4. **Use the free tier aggressively.** Almost everything here has a free tier allowance.
5. **Deploy with code from day one.** Get comfortable with SAM or CDK early — avoid clicking through the console for everything.
6. **Delete resources when done.** Always clean up to avoid surprise bills.
