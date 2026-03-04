# API Gateway

- It is a AWS service that enables developers to create, publish, maintain, monitor, and secure REST, HTTP, and WebSocket APIs at any scale.
- Acts as a front-door for clients/users to access backend AWS resources (such as Lambda, EC2 etc...)

#### Key Functions:
- Traffic Management
- Authentication & Authorization
- Security
- Performance Optimization
- API Lifecycle Management
- Monitoring & Logging

### Types of APIs:
- REST API
- HTTP API
- WebSocket API

---
### Basic security throttling config.:
- From the APIs listed in APIGateway table
    - Choose one to edit
    - from the side bar select Throttling under protect
    - Then select edit in Default route throttling
        - the base Rate limit defines the normal requests per second(rps)
        - Burst limit defines the max rps during a spike
   
