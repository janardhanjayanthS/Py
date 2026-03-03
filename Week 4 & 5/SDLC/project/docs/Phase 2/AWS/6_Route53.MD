# AWS Route 53

## What is Route 53?

Route 53 is AWS's **DNS (Domain Name System)** service — it translates human-readable domain names into IP addresses so browsers can find the right server.

**It does three things:**
1. **Domain registration** — buy/manage domains directly in AWS
2. **DNS routing** — route traffic to AWS resources or external endpoints
3. **Health checking** — monitor endpoints and reroute on failure

```mermaid
graph LR
    User["User types\nwww.mysite.com"] --> R53["Route 53\n(DNS resolver)"]
    R53 -->|"returns IP / alias"| Target["Target resource\n(CloudFront / ALB / EC2 / S3)"]
    Target --> User
```

> The name "Route 53" refers to TCP/UDP **port 53** — the standard DNS port.

---

## Hosted Zones

A **Hosted Zone** is a container for DNS records for a specific domain. Route 53 automatically creates one when you register a domain.

| Type | Used For |
|---|---|
| **Public Hosted Zone** | Routes traffic on the public internet (e.g., `www.mysite.com`) |
| **Private Hosted Zone** | Routes traffic within a VPC only (e.g., internal microservices) |

```mermaid
graph TD
    Domain["mysite.com\n(domain)"]
    Domain --> PHZ["Public Hosted Zone\n(internet-facing)"]
    Domain --> PRVHZ["Private Hosted Zone\n(VPC-internal only)"]

    PHZ --> CF["CloudFront\n(www.mysite.com)"]
    PHZ --> ALB["ALB\n(api.mysite.com)"]
    PRVHZ --> RDS["RDS\n(db.internal.mysite.com)"]
```

Each hosted zone automatically gets **NS** (Name Server) and **SOA** (Start of Authority) records on creation.

---

## Record Types

| Record | Purpose | Example |
|---|---|---|
| **A** | Maps domain → IPv4 address | `mysite.com → 54.21.3.100` |
| **AAAA** | Maps domain → IPv6 address | `mysite.com → 2001:db8::1` |
| **CNAME** | Maps domain → another domain name | `www.mysite.com → mysite.com` |
| **Alias** | AWS-specific — maps to AWS resources | `www.mysite.com → d1234.cloudfront.net` |
| **MX** | Mail server routing | `mysite.com → mail.mysite.com` |
| **TXT** | Text data (SPF, domain verification) | `"v=spf1 include:..."` |
| **NS** | Name servers for the zone | Auto-created by Route 53 |
| **SOA** | Zone metadata (TTL, admin email) | Auto-created by Route 53 |

### Alias vs CNAME — Key Difference

| | **CNAME** | **Alias** |
|---|---|---|
| Points to | Any hostname | AWS resource (CloudFront, ALB, S3, etc.) |
| On zone apex? | ❌ No (`mysite.com` not allowed) | ✅ Yes |
| DNS query charge | Yes | **Free** |
| Health checks | No | Yes (for some targets) |

> **Rule of thumb:** Use **Alias** for AWS resources, **CNAME** for non-AWS external hostnames.

---

## Routing Policies

Routing policies control **how Route 53 responds** to DNS queries.

### Simple Routing
One record, one target. No health checks.

```
www.mysite.com → 54.21.3.100
```

Use for: basic single-resource setups.

---

### Weighted Routing
Split traffic by percentage across multiple targets.

```mermaid
graph LR
    DNS["Route 53\nWeighted"] -->|"70%"| V1["EC2 v1\n(54.21.3.100)"]
    DNS -->|"30%"| V2["EC2 v2\n(54.21.3.101)"]
```

Use for: **A/B testing**, **blue-green deployments**, gradually shifting traffic.

---

### Latency-Based Routing
Routes to the region with the **lowest latency** for the user.

```mermaid
graph LR
    User_AP["User (Tokyo)"] --> DNS["Route 53\nLatency"]
    User_EU["User (Berlin)"] --> DNS
    DNS -->|"lowest latency"| AP["ap-northeast-1\n(Tokyo)"]
    DNS -->|"lowest latency"| EU["eu-west-1\n(Ireland)"]
```

Use for: globally distributed apps where response time matters.

---

### Failover Routing
Active/passive setup. If the primary fails a health check, traffic shifts to secondary.

```mermaid
flowchart LR
    DNS["Route 53\nFailover"]
    DNS -->|"primary (healthy)"| Primary["Primary\nEC2 / ALB"]
    Primary -->|"health check fails"| DNS
    DNS -->|"failover"| Secondary["Secondary\n(backup / S3 static page)"]
```

Use for: **disaster recovery**, high availability.

---

### Geolocation Routing
Routes based on the **geographic location** of the user (country/continent).

```mermaid
graph LR
    DNS["Route 53\nGeolocation"]
    DNS -->|"US users"| US["us-east-1"]
    DNS -->|"EU users"| EU["eu-west-1"]
    DNS -->|"default"| Default["us-west-2"]
```

Use for: compliance (data residency laws), localized content.

> Different from latency-based — it's about **where the user is**, not speed.

---

### Geoproximity Routing (Traffic Flow only)
Like geolocation but you can **bias** the routing radius — expand or shrink a region's reach.

Use for: shifting traffic toward a specific region even if users are slightly outside it.

---

### Multi-Value Answer Routing
Returns up to **8 healthy IP addresses** per query. Client picks one. Acts like a basic load balancer.

Use for: simple client-side load balancing with health checks (not a replacement for ALB).

---

## Health Checks

Route 53 health checks monitor endpoints and mark them healthy/unhealthy.

```mermaid
sequenceDiagram
    participant R53 as Route 53
    participant EP as Endpoint

    loop Every 10-30s
        R53->>EP: HTTP/HTTPS/TCP probe
        EP-->>R53: 2xx response = healthy
    end

    Note over R53: If unhealthy → stop returning this IP in DNS
```

| Health Check Type | What it monitors |
|---|---|
| **Endpoint** | Public IP or URL (HTTP/HTTPS/TCP) |
| **Calculated** | Combines multiple health checks (AND/OR logic) |
| **CloudWatch alarm** | Ties health to a CloudWatch metric |

> Health checks only work on **public endpoints**. For private resources, use a CloudWatch alarm health check.

---

## Integration with AWS Services

```mermaid
graph TD
    R53["Route 53"]
    R53 -->|"Alias A record"| CF["CloudFront\n(www.mysite.com)"]
    R53 -->|"Alias A record"| ALB["Application Load Balancer\n(api.mysite.com)"]
    R53 -->|"Alias A record"| S3["S3 Static Website\n(assets.mysite.com)"]
    R53 -->|"Alias A record"| APIGW["API Gateway\n(v2.mysite.com)"]
    R53 -->|"A record"| EC2["EC2 Instance\n(admin.mysite.com)"]
```

All AWS resource targets should use **Alias records** — they're free, support the zone apex, and integrate with health checks.

---

## ACM DNS Validation via Route 53

When requesting a TLS certificate from ACM, DNS validation requires adding a CNAME record to prove domain ownership. Route 53 can do this **automatically**.

```mermaid
sequenceDiagram
    participant Dev
    participant ACM
    participant R53 as Route 53

    Dev->>ACM: Request public cert for mysite.com
    ACM-->>Dev: Provide CNAME validation record
    Dev->>R53: Click "Create records in Route 53"
    R53->>R53: Add CNAME record automatically
    ACM->>R53: Verify CNAME exists
    ACM-->>Dev: Certificate issued ✓
```

> ACM re-checks this CNAME before cert renewal — **don't delete it** after validation.

---

## Practical: Full DNS Setup for a Web App

```mermaid
graph LR
    User -->|"www.mysite.com"| R53["Route 53\n(Alias A record)"]
    R53 --> CF["CloudFront\n(HTTPS + ACM cert)"]
    CF -->|"OAC"| S3["S3 Bucket\n(React build)"]

    User2 -->|"api.mysite.com"| R53
    R53 -->|"Alias A record"| ALB["ALB\n(Django backend)"]
    ALB --> EC2["EC2 / ECS"]
```

| Record | Type | Target |
|---|---|---|
| `www.mysite.com` | Alias A | CloudFront distribution |
| `mysite.com` | Alias A | CloudFront distribution (zone apex) |
| `api.mysite.com` | Alias A | Application Load Balancer |
| `_acme.mysite.com` | CNAME | ACM validation record |

---

## Key Concepts Summary

| Concept | What it does |
|---|---|
| **Hosted Zone** | Container for all DNS records for a domain |
| **A / AAAA record** | Maps domain to IPv4 / IPv6 |
| **CNAME** | Maps domain to another hostname (not on zone apex) |
| **Alias record** | AWS-specific — maps to AWS resources, free, supports apex |
| **Routing Policy** | How Route 53 picks which record to return |
| **Health Check** | Monitors endpoints; removes unhealthy targets from DNS |
| **TTL** | How long resolvers cache the DNS answer |

---

###### Resources:
- Route 53 Routing Policies — https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/routing-policy.html
- See also: [5_Cloudfront.MD](./5_Cloudfront.MD) — wiring Route 53 to a CloudFront + S3 deployment
