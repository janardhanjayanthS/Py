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

#### Policy Types: Managed vs Inline

```mermaid
graph TD
    A[IAM Policies] --> B[Managed Policies]
    A --> C[Inline Policies]

    B --> D[AWS Managed]
    B --> E[Customer Managed]

    D --> F["Pre-built by AWS<br/>e.g., PowerUserAccess"]
    E --> G["Created by you<br/>Reusable across entities"]

    C --> H["Embedded directly<br/>into one user/role/group"]

    style D fill:#9f9,stroke:#333
    style E fill:#9cf,stroke:#333
    style C fill:#fc9,stroke:#333
```

**Managed Policies** (Recommended ✅)
- Standalone policies that can be attached to multiple users, groups, or roles
- **Reusable** and centrally managed
- Easy to update - changes apply to all attached identities

**Types of Managed Policies:**
1. **AWS Managed Policies**
   - Pre-built by AWS
   - Examples: `AdministratorAccess`, `ReadOnlyAccess`, `AmazonS3FullAccess`
   - AWS maintains and updates them
   - ✅ Great for common use cases

2. **Customer Managed Policies**
   - Created and managed by you
   - Full control over permissions
   - ✅ Best for custom requirements

**Inline Policies** (Use sparingly ⚠️)
- Embedded directly into a single user, group, or role
- **1:1 relationship** - deleted when the identity is deleted
- Harder to manage and track
- ⚠️ Use only for one-off exceptions

**When to use what:**
- ✅ **AWS Managed** - Common scenarios (S3 full access, read-only, etc.)
- ✅ **Customer Managed** - Custom permissions needed by multiple identities
- ⚠️ **Inline** - Strict 1:1 relationship where policy must not outlive the identity

---

#### Policy Types: Identity-Based vs Resource-Based

```mermaid
graph LR
    A[Policy Types by Attachment]

    A --> B[Identity-Based Policies]
    A --> C[Resource-Based Policies]

    B --> D[Attached to:<br/>Users, Groups, Roles]
    B --> E["Defines: What this<br/>identity can do"]

    C --> F[Attached to:<br/>Resources S3, SQS, SNS]
    C --> G["Defines: Who can<br/>access this resource"]

    style B fill:#9cf,stroke:#333,stroke-width:2px
    style C fill:#f9c,stroke:#333,stroke-width:2px
```

**Identity-Based Policies**
- Attached to **users, groups, or roles**
- Defines what actions that identity can perform
- Most common type of policy

**Example:** Policy attached to a user defining they can read S3 buckets
```json
{
  "Effect": "Allow",
  "Action": "s3:GetObject",
  "Resource": "arn:aws:s3:::my-bucket/*"
}
```

**Resource-Based Policies**
- Attached to **resources** (S3 buckets, SQS queues, Lambda functions)
- Defines who can access that specific resource
- Supports cross-account access

**Example:** S3 bucket policy allowing another AWS account to read objects
```json
{
  "Effect": "Allow",
  "Principal": {"AWS": "arn:aws:iam::123456789012:root"},
  "Action": "s3:GetObject",
  "Resource": "arn:aws:s3:::my-bucket/*"
}
```

**Key Difference:**
- **Identity-based:** "What can I do?" (attached to identities)
- **Resource-based:** "Who can access me?" (attached to resources)

---

## IAM Components

### Users
**Individual identities** representing people or applications that need to interact with AWS.

**Characteristics:**
- Each user has unique credentials (username/password or access keys)
- Used for **permanent, long-term access**
- Can be assigned permissions directly or through groups
- Each user gets a unique Amazon Resource Name (ARN)

**When to use:**
- Individual team members who need AWS console access
- Long-term service accounts (though roles are preferred)

**Example:** `john-smith`, `ci-cd-deployer`

---

### Groups
**Collections of users** with similar job functions or permission needs.

**Characteristics:**
- Simplifies permission management for multiple users
- Users inherit all permissions attached to their groups
- A user can belong to multiple groups (up to 10)
- **Groups cannot be nested** (no groups within groups)

**When to use:**
- Organizing users by department, project, or function
- Applying common permissions to multiple users at once

**Example Groups:**
- `Developers` - Read/write access to dev resources
- `Admins` - Full administrative access
- `DataAnalysts` - Read-only access to databases and S3

---

### Roles
**Temporary identities** that can be assumed by users, applications, or AWS services.

**Characteristics:**
- **No permanent credentials** - uses temporary security tokens
- Can be assumed by anyone/anything that is trusted
- More secure than access keys for applications
- Can be assumed across AWS accounts

**When to use:**
- Applications running on AWS (EC2, Lambda, ECS)
- Cross-account access
- Temporary elevated permissions
- Service-to-service communication

**Example:** `lambda-s3-read-role`, `ec2-instance-role`

**Key Difference from Users:**
- **Users** = Permanent credentials for specific people/apps
- **Roles** = Temporary credentials that can be assumed by anyone trusted

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

## Least Privilege Principle

The **Principle of Least Privilege** means granting only the minimum permissions needed to perform a task—nothing more.

```mermaid
graph LR
    A[Least Privilege Principle] --> B["❌ Don't Do This"]
    A --> C["✅ Do This"]

    B --> D["Give Full Admin Access<br/>to everyone"]
    B --> E["Grant 'just in case'<br/>permissions"]

    C --> F["Grant only what's needed<br/>for the job"]
    C --> G["Start with nothing,<br/>add as required"]

    style B fill:#f99,stroke:#333,stroke-width:2px
    style C fill:#9f9,stroke:#333,stroke-width:2px
```

### Why It Matters
- 🔒 **Reduces attack surface** - Compromised credentials have limited damage
- 🛡️ **Limits accidental damage** - Users can't accidentally delete critical resources
- 📊 **Improves compliance** - Meets regulatory requirements
- 🎯 **Better accountability** - Clear audit trail of who can do what

### How to Implement

**❌ Bad Example:**
```json
{
  "Effect": "Allow",
  "Action": "*",
  "Resource": "*"
}
```
This grants full access to everything—very dangerous!

**✅ Good Example:**
```json
{
  "Effect": "Allow",
  "Action": [
    "s3:GetObject",
    "s3:PutObject"
  ],
  "Resource": "arn:aws:s3:::my-app-bucket/uploads/*"
}
```
This grants only read/write access to a specific folder in one S3 bucket.

### Best Practice Workflow

```mermaid
flowchart TD
    A[Start with Zero Access] --> B[Identify Required Actions]
    B --> C[Grant Minimal Permissions]
    C --> D[Test Application]
    D --> E{Access Denied Errors?}
    E -->|Yes| F[Add Specific Permission]
    F --> D
    E -->|No| G[✅ Done - Least Privilege Achieved]

    style A fill:#f9f,stroke:#333
    style G fill:#9f9,stroke:#333,stroke-width:2px
```

**Steps:**
1. Start with no permissions
2. Add permissions only when needed
3. Monitor for access denied errors
4. Grant only the specific permission required
5. Regularly review and remove unused permissions

---

## How Services Assume Roles (Service-to-Service Communication)

AWS services often need to access other services. Instead of hardcoding credentials, services **assume roles** to get temporary permissions.

### The Role Assumption Process

```mermaid
sequenceDiagram
    participant Lambda as Lambda Function
    participant STS as AWS STS<br/>(Security Token Service)
    participant IAM as IAM Role
    participant S3 as S3 Bucket

    Note over Lambda: Lambda needs to read from S3

    Lambda->>IAM: 1. Check Execution Role
    IAM->>STS: 2. Request Temporary Credentials
    Note over IAM: Trust policy allows Lambda<br/>to assume this role

    STS->>Lambda: 3. Return Temp Credentials<br/>(Access Key + Secret + Token)
    Note over Lambda: Credentials valid for<br/>15 min - 12 hours

    Lambda->>S3: 4. Access S3 using temp credentials
    S3->>IAM: 5. Verify permissions
    IAM->>S3: 6. Allow (policy grants s3:GetObject)
    S3->>Lambda: 7. Return requested data ✓

    Note over Lambda,S3: All credentials are temporary<br/>and auto-rotated!
```

### Components Required

**1. Trust Policy (Who can assume the role)**
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
This says: "Lambda service is allowed to assume this role"

**2. Permission Policy (What the role can do)**
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:PutObject"
      ],
      "Resource": "arn:aws:s3:::my-bucket/*"
    }
  ]
}
```
This says: "This role can read and write to my-bucket"

### Common Service-to-Service Scenarios

```mermaid
graph TD
    A[Common Role Assumptions]

    A --> B[Lambda → S3]
    A --> C[EC2 → DynamoDB]
    A --> D[ECS → Secrets Manager]
    A --> E[API Gateway → Lambda]

    B --> F["Trust: lambda.amazonaws.com<br/>Permissions: s3:GetObject"]
    C --> G["Trust: ec2.amazonaws.com<br/>Permissions: dynamodb:Query"]
    D --> H["Trust: ecs-tasks.amazonaws.com<br/>Permissions: secretsmanager:GetSecretValue"]
    E --> I["Trust: apigateway.amazonaws.com<br/>Permissions: lambda:InvokeFunction"]

    style F fill:#9cf,stroke:#333
    style G fill:#9cf,stroke:#333
    style H fill:#9cf,stroke:#333
    style I fill:#9cf,stroke:#333
```

### Step-by-Step Example: Lambda Reading from S3

**Scenario:** You have a Lambda function that needs to read files from an S3 bucket.

**Step 1:** Create IAM Role for Lambda
```bash
Role Name: lambda-s3-reader-role
```

**Step 2:** Add Trust Policy (Allow Lambda to assume it)
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

**Step 3:** Add Permission Policy (Allow S3 read)
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::my-data-bucket/*"
    }
  ]
}
```

**Step 4:** Attach Role to Lambda Function
- In Lambda console, assign the `lambda-s3-reader-role` as the execution role

**Step 5:** Lambda Automatically Assumes the Role
- When Lambda runs, it automatically requests temporary credentials from AWS STS
- Uses those credentials to access S3
- No hardcoded access keys needed! 🎉

### Why This Is Better Than Access Keys

| Aspect | Role Assumption ✅ | Hardcoded Access Keys ❌ |
|--------|-------------------|------------------------|
| **Security** | Temporary credentials (auto-expire) | Permanent credentials |
| **Rotation** | Automatic | Manual |
| **Management** | Centralized in IAM | Scattered in code/configs |
| **Audit** | CloudTrail tracks all assumptions | Harder to track usage |
| **Compromise Risk** | Limited blast radius | Full access if leaked |

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
3. ✅ **Follow Least Privilege Principle** - only give permissions that are needed (see detailed section above)
4. ✅ **Prefer Managed Policies** over inline policies for easier management
5. ✅ **Use Roles for Applications** instead of hardcoded access keys (enables automatic credential rotation)
6. ✅ **Rotate Credentials** regularly for IAM users
7. ✅ **Monitor Activity** with CloudTrail to track all IAM actions
8. ✅ **Use Service Roles** for AWS services to communicate with each other
9. ❌ **Never use Root Account** for daily tasks - create IAM users instead
10. ❌ **Never share credentials** between users or hardcode them in code
11. ❌ **Don't use wildcard (*) permissions** unless absolutely necessary

---

## Quick Reference

| Component | Purpose | Example |
|-----------|---------|---------|
| **User** | Individual identity (permanent credentials) | john@company.com |
| **Group** | Collection of users | Developers, Admins |
| **Role** | Temporary identity (assumed by services/users) | Lambda execution role |
| **Policy** | Permission document (JSON) | Allow S3 read access |
| **Resource** | AWS entity | S3 bucket, EC2 instance |
| **Action** | Operation | CreateBucket, GetObject |
| **AWS Managed Policy** | Pre-built policy by AWS | AdministratorAccess |
| **Customer Managed Policy** | Custom reusable policy | MyCustomS3Policy |
| **Inline Policy** | Embedded policy (1:1 relationship) | Policy embedded in one role |
| **Identity-Based Policy** | Attached to users/groups/roles | What can I do? |
| **Resource-Based Policy** | Attached to resources | Who can access me? |
| **Trust Policy** | Defines who can assume a role | Lambda can assume this role |
| **STS** | Security Token Service | Issues temporary credentials |
| **Least Privilege** | Minimum permissions needed | Only s3:GetObject, not s3:* |

---

## Resources
- 📺 [IAM Explanation (YouTube)](https://www.youtube.com/watch?v=_ZCTvmaPgao)
- 📺 [IAM User Creation & Policy (YouTube)](https://www.youtube.com/watch?v=dMPDZHVIZBs)
- 📖 [AWS IAM Official Documentation](https://docs.aws.amazon.com/IAM/)

---

**Remember:** IAM is the foundation of AWS security. Understanding it well will help you build secure and well-architected applications! 🔒
