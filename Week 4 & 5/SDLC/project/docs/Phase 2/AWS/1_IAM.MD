# AWS IAM (Identity and Access Management)

## Overview
IAM is AWS's security service that controls **who** can access **what** in your AWS account. Think of it as a security guard system that checks IDs and permissions before allowing anyone to use your AWS resources.

```mermaid
graph LR
    A[User/Application] -->|Requests Access| B[IAM]
    B -->|Checks Identity| C{Authentication}
    C -->|Valid?| D{Authorization}
    D -->|Check Policies| E[AWS Resources]
    E -->|S3, Lambda, EC2, etc.| F[Action Performed]
    C -->|Invalid| G[Access Denied]
    D -->|No Permission| G
```

---

## Core Concepts

### 1. **Resources**
Resources are specific entities in AWS that you work with.
- **Examples:** S3 buckets, Lambda functions, EC2 instances, DynamoDB tables, objects in buckets

### 2. **Actions**
Actions are tasks you can perform on resources.
- **Examples:**
  - `S3:CreateBucket` - Create a new S3 bucket
  - `S3:GetObject` - Read a file from S3
  - `Lambda:InvokeFunction` - Run a Lambda function
  - `EC2:StartInstances` - Start an EC2 server

### 3. **Policies**
Policies are JSON documents that define **what actions** are allowed or denied on **which resources**.

**Example Policy:**
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::my-bucket/*"
    }
  ]
}
```
This policy allows reading objects from `my-bucket` in S3.

---

## IAM Components

### Users
Individual people or applications that need to interact with AWS.
- Each user has unique credentials (username/password or access keys)
- Used for permanent, long-term access

### Groups
Collections of users with similar permissions.
- Makes it easy to manage permissions for multiple users
- Example: "Developers" group, "Admins" group

### Roles
Temporary identities that can be assumed by users, applications, or AWS services.
- Used for temporary access or cross-service permissions
- Example: Lambda function needs to read from S3

```mermaid
graph TD
    A[IAM Components]
    A --> B[Users]
    A --> C[Groups]
    A --> D[Roles]
    A --> E[Policies]

    B --> F[Alice]
    B --> G[Bob]

    C --> H[Developers Group]
    C --> I[Admins Group]

    F -.->|Member of| H
    G -.->|Member of| I

    H -->|Attached| E
    I -->|Attached| E
    F -->|Direct Policy| E

    D --> J[Lambda Execution Role]
    J -->|Attached| E

    style E fill:#f9f,stroke:#333,stroke-width:2px
```

---

## How IAM Works

### Authentication vs Authorization

```mermaid
sequenceDiagram
    participant User
    participant IAM
    participant Policy
    participant AWS Resource

    User->>IAM: 1. Login (username + password)
    IAM->>IAM: 2. Verify Identity ✓
    Note over IAM: Authentication Complete

    User->>AWS Resource: 3. Request Action (e.g., read S3 file)
    AWS Resource->>IAM: 4. Check Permissions
    IAM->>Policy: 5. Evaluate Policies
    Policy->>IAM: 6. Allow/Deny

    alt Permission Granted
        IAM->>AWS Resource: 7. Authorized ✓
        AWS Resource->>User: 8. Action Performed
    else Permission Denied
        IAM->>User: 7. Access Denied ✗
    end

    Note over IAM,Policy: Authorization Process
```

**Authentication:** Proving who you are (login with credentials)
**Authorization:** Determining what you're allowed to do (policy evaluation)

---

## Policy Evaluation Flow

When you make a request to AWS, IAM evaluates policies in this order:

```mermaid
flowchart TD
    A[AWS Request] --> B{Explicit DENY?}
    B -->|Yes| C[❌ DENY ACCESS]
    B -->|No| D{Explicit ALLOW?}
    D -->|Yes| E[✅ ALLOW ACCESS]
    D -->|No| F[❌ DENY by Default]

    style C fill:#f88,stroke:#333,stroke-width:2px
    style E fill:#8f8,stroke:#333,stroke-width:2px
    style F fill:#f88,stroke:#333,stroke-width:2px
```

**Important:** Deny always wins! If any policy explicitly denies an action, access is denied even if another policy allows it.

---

## Access Methods

### 1. **Console Access (AWS Web Interface)**
- Username + Password
- Optional: Multi-Factor Authentication (MFA)

### 2. **Programmatic Access (CLI, SDK, APIs)**
- Access Key ID + Secret Access Key
- Used by applications and command-line tools

```mermaid
graph LR
    A[Access AWS] --> B[Console Access]
    A --> C[Programmatic Access]

    B --> D[Username]
    B --> E[Password]
    B --> F[MFA Optional]

    C --> G[Access Key ID]
    C --> H[Secret Access Key]

    style G fill:#ff9,stroke:#333
    style H fill:#f99,stroke:#333
```

---

## Secrets & Credentials

**Secrets** are sensitive strings/codes used to authenticate with AWS:
- **Access Key ID:** Public identifier (e.g., `AKIAIOSFODNN7EXAMPLE`)
- **Secret Access Key:** Private key (e.g., `wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY`)
- **Session Tokens:** Temporary credentials for roles

⚠️ **Security Best Practices:**
- Never commit secrets to Git
- Rotate access keys regularly
- Use environment variables or AWS Secrets Manager
- Enable MFA for sensitive operations

---

## Trust Relationships

Trust relationships define **who can assume a role**. This is crucial for:
- Cross-account access (Account A accessing Account B's resources)
- Service-to-service access (Lambda accessing S3)

**Example Trust Policy:**
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
```
This allows Lambda service to assume this role.

```mermaid
graph LR
    A[Lambda Function] -->|Assumes| B[IAM Role]
    B -->|Has Policy| C[S3 Read Permission]
    C -->|Grants Access| D[S3 Bucket]

    style B fill:#9cf,stroke:#333,stroke-width:2px
```

---

## Common Use Cases

### 1. **User Management**
Create individual users for team members with specific permissions.

### 2. **Application Access**
Create roles for applications (like Lambda) to access other AWS services.

### 3. **Cross-Account Access**
Allow users from one AWS account to access resources in another account.

### 4. **Temporary Access**
Use roles to provide time-limited access without creating permanent credentials.

---

## IAM Best Practices

1. ✅ **Enable MFA** for all users, especially root account
2. ✅ **Use Groups** to assign permissions, not individual users
3. ✅ **Grant Least Privilege** - only give permissions that are needed
4. ✅ **Rotate Credentials** regularly
5. ✅ **Use Roles** for applications instead of hardcoded access keys
6. ✅ **Monitor Activity** with CloudTrail
7. ❌ **Never use Root Account** for daily tasks
8. ❌ **Never share credentials** between users

---

## Quick Reference

| Component | Purpose | Example |
|-----------|---------|---------|
| **User** | Individual identity | john@company.com |
| **Group** | Collection of users | Developers, Admins |
| **Role** | Temporary identity | Lambda execution role |
| **Policy** | Permission document | Allow S3 read access |
| **Resource** | AWS entity | S3 bucket, EC2 instance |
| **Action** | Operation | CreateBucket, GetObject |

---

## Resources
- 📺 [IAM Explanation (YouTube)](https://www.youtube.com/watch?v=_ZCTvmaPgao)
- 📺 [IAM User Creation & Policy (YouTube)](https://www.youtube.com/watch?v=dMPDZHVIZBs)
- 📖 [AWS IAM Official Documentation](https://docs.aws.amazon.com/IAM/)

---

**Remember:** IAM is the foundation of AWS security. Understanding it well will help you build secure and well-architected applications! 🔒
