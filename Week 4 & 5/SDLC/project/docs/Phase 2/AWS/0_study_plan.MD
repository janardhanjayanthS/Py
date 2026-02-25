# AWS Learning Roadmap — Backend Developer
> **Level:** Upper Beginner in Cloud | **Role:** Backend Developer
> **Goal:** Learn AWS services for backend development, from fundamentals to production-ready applications.

---

## 🗺️ Overview

| Phase | Topic | Duration |
|-------|-------|----------|
| 1 | AWS Fundamentals & IAM | 1–2 weeks |
| 2 | Core Compute & Storage | 2–3 weeks |
| 3 | Serverless Core | 2–3 weeks |
| 4 | Data & Caching | 2–3 weeks |
| 5 | Security & Secrets | 1–2 weeks |
| 6 | Observability & Communication | 1–2 weeks |
| 7 | Capstone Project | Ongoing |

**Total estimated time:** 10–17 weeks at a comfortable pace.

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
**Duration:** 1–2 weeks

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
**Duration:** 2–3 weeks

### Goals
Build the foundational mental model for cloud servers and storage that everything else builds on.

---

### EC2

- [ ] Instance types and when to use them
- [ ] Security groups and inbound/outbound rules
- [ ] Key pairs and SSH access
- [ ] Elastic IPs
- [ ] Stop vs. terminate

#### 📺 Videos
- [EC2 Crash Course — freeCodeCamp](https://www.youtube.com/results?search_query=EC2+crash+course+aws+freeCodeCamp)
- [EC2 Tutorial — Stephane Maarek Udemy Course](https://www.udemy.com/course/aws-certified-developer-associate-dva-c01/) *(best structured EC2 coverage)*
- [AWS EC2 Explained — Abhishek Veeramalla Zero to Hero](https://www.youtube.com/@AbhishekVeeramalla)

#### 📖 Docs & Reading
- [EC2 Getting Started — AWS Docs](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/EC2_GetStarted.html)
- [EC2 Instance Types — AWS](https://aws.amazon.com/ec2/instance-types/)

#### Practice
Spin up an EC2 instance and run a simple Node.js or Python HTTP server on it.

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

## Phase 3 — Serverless Core
**Duration:** 2–3 weeks

### Goals
Understand the serverless execution model and build your first real API.

---

### Lambda

- [ ] Execution model — how Lambda runs your code
- [ ] Cold starts and how to minimize them
- [ ] Memory, timeout, and concurrency settings
- [ ] Environment variables
- [ ] Layers *(for shared dependencies)*
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

### Serverless Applications (AWS SAM)

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

## Phase 4 — Data & Caching
**Duration:** 2–3 weeks

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

## Phase 5 — Security & Secrets
**Duration:** 1–2 weeks

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

## Phase 6 — Observability & Communication
**Duration:** 1–2 weeks

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

## Phase 7 — Capstone Project
**Duration:** Ongoing

### Goal
Build a real project that connects every service and surfaces gaps in your knowledge.

### Project Idea: Serverless Backend API

Build a backend API for a simple app (e.g. a task manager or e-commerce backend):

```
Request
  └── API Gateway (HTTP API)
        └── Cognito Authorizer (authentication)
              └── Lambda (business logic)
                    ├── DynamoDB (primary storage)
                    ├── ElastiCache / Redis (caching layer)
                    ├── Secrets Manager (credentials)
                    ├── SES (transactional emails)
                    └── S3 (file storage)

Observability:
  ├── CloudWatch (logs & metrics)
  └── X-Ray (distributed tracing)

Infrastructure:
  └── AWS SAM (deployed as code)
```

### Capstone Checklist
- [ ] All infrastructure defined as code with SAM
- [ ] All secrets in Secrets Manager — nothing hardcoded
- [ ] All endpoints protected by Cognito
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

## ➕ Bonus Services to Add (Recommended for Backend Devs)

Very common in real backend AWS work — learn these after your capstone or alongside it.

| Service | Why You Need It | Best Starting Resource |
|---------|----------------|----------------------|
| **SQS** | Async job queues, decoupling Lambda functions | [SQS Developer Guide — AWS Docs](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/welcome.html) |
| **SNS** | Fan-out messaging, pub/sub patterns | [SNS Developer Guide — AWS Docs](https://docs.aws.amazon.com/sns/latest/dg/welcome.html) |
| **EventBridge** | Event-driven architecture between services | [EventBridge User Guide — AWS Docs](https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-what-is.html) |
| **RDS** | When your project needs a SQL database | [RDS Getting Started — AWS Docs](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_GettingStarted.html) |
| **VPC Basics** | Required for ElastiCache and RDS from Lambda | [VPC Getting Started — AWS Docs](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-getting-started.html) |
| **AWS CDK** | Write infrastructure in your own programming language | [CDK Getting Started — AWS Docs](https://docs.aws.amazon.com/cdk/v2/guide/getting_started.html) |

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
5. **Deploy with code from day one.** Get comfortable with SAM early — avoid clicking through the console for everything.
6. **Delete resources when done.** Always clean up to avoid surprise bills.
