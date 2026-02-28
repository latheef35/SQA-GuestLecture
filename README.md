# SQA-GuestLecture
This repo details the non-functional testing related to security and performance testing

## Table of Contents
- [Overview](#overview)
- [Learning Objectives](#learning-objectives)
- [Performance Testing Fundamentals](#performance-testing-fundamentals)
- [Prerequisites](#prerequisites)
- [Lab Exercises](#lab-exercises)
- [Troubleshooting](#troubleshooting)
- [Additional Resources](#additional-resources)



## Overview
This course provides a complete lab environment for learning and practicing:
- **Performance Testing Fundamentals** - Load, stress, spike, soak testing
- **Artillery Testing Tool** - Modern, developer-friendly load testing
- **Real Metrics Analysis** - Response times, throughput, error rates
- **Production Readiness** - Capacity planning and Go/No-Go decisions

All tools run in isolated Docker containers - no complex installations required!

## Learning Objectives
By completing this lab, you will:

**Core Concepts:**
- Understand different types of performance tests (smoke, load, stress, spike, soak)
- Learn key performance metrics (p50, p95, p99, throughput, error rate)
- Identify performance bottlenecks and system breaking points
- Make data-driven capacity planning decisions

**Artillery Skills:**
- Write and execute Artillery test scripts
- Configure realistic test scenarios with user workflows
- Interpret Artillery reports and metrics
- Set performance thresholds and expectations

**Professional Skills:**
- Conduct production readiness assessments
- Create performance test reports
- Recommend system improvements based on test results
- Communicate performance findings to stakeholders

### Why Performance Testing Matters

**Business Impact:**
- 1 second delay = 7% reduction in conversions (Amazon)
- 100ms delay = 1% drop in sales (Amazon: $1.6B/year)
- 40% of users abandon sites that take >3 seconds to load
- 79% of dissatisfied users won't return

**Cost of Poor Performance:**
- Knight Capital: $440 million lost in 45 minutes (bad deployment)
- Amazon Prime Day 2018: 63 minutes downtime = $99 million lost
- Target Canada: Site crashes during Black Friday sales
  
## Performance Testing Fundamentals

### What is Performance Testing?

Performance testing evaluates how a system performs under various conditions. Key aspects:

- **Speed**: How fast does the system respond?
- **Scalability**: How does it handle increasing load?
- **Stability**: Does it remain stable under sustained load?
- **Reliability**: What's the error rate under stress?

### Types of Performance Tests

#### 1. **Smoke Test** (Sanity Check)
```
Load: ▁▁▁▁▁▁▁▁▁▁ (minimal)
Time: ─────────→
```
- **Purpose**: Verify the system works under minimal load
- **Load**: 1-5 users
- **Duration**: 1-2 minutes
- **When**: Before any serious testing
**Real Example:** "Before AWS launches a new service, they run smoke tests to ensure the API responds correctly with minimal load."

#### 2. **Load Test**
```
Load:     ┌────────┐
       ┌──┘        └──┐
     ──┘              └──
Time: ─────────────────→
     Warmup  Sustained  Cooldown
```
- **Purpose**: Verify system behavior under expected load
- **Load**: Expected average and peak concurrent users
- **Duration**: 5-30 minutes
- **When**: Regular testing, before releases

**Real Example:** "Netflix load tests before major releases (Stranger Things, etc.) to ensure millions can stream simultaneously."


#### 3. **Stress Test**
```
Load:            /\
             /\/  \
         /\/        \
     /\/              \__
Time: ─────────────────→
     Push beyond capacity until failure
```
- **Purpose**: Find the breaking point
- **Load**: Beyond normal capacity
- **Duration**: Until system fails or degrades significantly
- **When**: Capacity planning
**Real Example:** "Twitter stress tests before Super Bowl, World Cup, major events to know when to scale up servers."

#### 4. **Spike Test**
```
Load:      ││
           ││
    ───────││────────
Time: ─────────────→
     Normal SPIKE Normal
```
- **Purpose**: Test sudden traffic surges
- **Load**: Sudden jump to high load
- **Duration**: Short bursts
- **When**: Testing flash sales, viral content scenarios

**Real Examples:**
- Flash sales (Nike sneaker drops)
- Breaking news (CNN when major event happens)
- Viral social media posts
- Black Friday 12:00 AM
  
#### 5. **Soak Test (Endurance)**
```
Load: ────────────────
Time: ─────────────────────────────→
      Hours or Days
```
- **Purpose**: Find memory leaks, resource exhaustion
- **Load**: Normal load
- **Duration**: Several hours to days
- **When**: Before major releases
**Real Example:** "NASA runs soak tests on ISS systems for weeks to ensure they'll work for months in space."


#### 6. **Scalability Test**
- **Purpose**: Determine if adding resources improves performance
- **Load**: Increasing load with increasing resources
- **Duration**: Multiple test runs
- **When**: Infrastructure planning

---

## Key Performance Metrics

### Response Time Metrics

**Response Time**: Time from request sent to response received

- **Average (Mean)**: Sum of all response times / number of requests
  - Can be misleading due to outliers
  
- **Median (p50)**: 50% of requests are faster than this
  - Better representation of "typical" experience
  
- **p95 (95th Percentile)**: 95% of requests are faster than this
  - Used for SLA definitions
  - Example: "95% of requests complete in < 500ms"
  
- **p99 (99th Percentile)**: 99% of requests are faster than this
  - Shows worst-case scenarios most users experience
  
- **Max**: Slowest request
  - Useful for finding outliers

**Example:**
```
100 requests with response times:
- Average: 250ms
- p50: 200ms (median - half are faster)
- p95: 450ms (95 out of 100 are faster)
- p99: 890ms (99 out of 100 are faster)
- Max: 1200ms
```

**Rule of Thumb:**
- **p50**: What most users experience
- **p95**: What we promise in SLAs
- **p99**: What keeps us up at night

### Throughput Metrics

- **Requests per Second (RPS)**: How many requests the system handles
- **Transactions per Second (TPS)**: Complete user workflows per second

### Error Metrics

- **Error Rate**: Percentage of failed requests
- **Error Types**: 4xx (client errors), 5xx (server errors), timeouts

### Resource Metrics

- **CPU Usage**: Percentage of CPU utilized
- **Memory Usage**: RAM consumption
- **Disk I/O**: Read/write operations
- **Network**: Bandwidth usage

## Introduction to Artillery 

### Why Artillery?

**Comparison:**

```
Traditional Tools (JMeter, LoadRunner):
- Heavy GUI applications
- Complex setup
- Expensive licenses (LoadRunner)
- Hard to version control

Artillery (Modern Approach):
- Simple YAML configuration
- Code-based (version control friendly)
- Free and open source
- Developer-friendly
- CI/CD integration
- Detailed HTML reports
```


### Artillery Core Concepts



#### 1. Config Section
- **target**: Where to send requests
- **phases**: How load changes over time
- **duration**: How long each phase runs
- **arrivalRate**: New users per second

**Analogy:** "Think of a concert venue. arrivalRate is how fast people arrive at the entrance, not total capacity."

```yaml
config:
  target: "http://localhost:3000"
  phases:
    - duration: 60        # Run for 60 seconds
      arrivalRate: 10     # 10 users per second
      name: "Warm up"

scenarios:
  - name: "Basic user flow"
    flow:
      - get:
          url: "/api/products"
      - think: 2          # Wait 2 seconds (user reading)
      - get:
          url: "/api/cart"
```
---

#### 2. Scenarios Section
- **Scenarios**: User workflows
- **Weight**: Percentage distribution
- **Flow**: Sequence of actions

**Example:**
```yaml
scenarios:
  - name: "Purchaser"
    weight: 30           # 30% of users
    flow:
      - get: /products
      - post: /cart
      - post: /checkout

  - name: "Browser"
    weight: 70           # 70% of users
    flow:
      - get: /products
      # No purchase
```

---

#### 3. Think Time
"Real users don't instantly click. They read, consider, get distracted. Think time simulates reality!"


**Explanation:** 
```yaml
- get: /products
- think: 3              # User spends 3 seconds reading
- get: /product/123
```



## Prerequisites
### Required Software

**Docker Desktop**
- Windows: [Download](https://www.docker.com/products/docker-desktop)
- Mac: [Download](https://www.docker.com/products/docker-desktop)
- Linux: [Installation Guide](https://docs.docker.com/engine/install/)


**System Requirements:**
- 4GB RAM (8GB recommended)
- 5GB free disk space
- Internet connection for initial setup

**Artillery Cloud Account**
- Artillery Cloud [Artillery Cloud Account](https://www.artillery.io/docs/get-started/get-artillery#set-up-cloud-reporting)

Grab the API key for reports


## Lab exercises

### What You'll Do Today

**Show the progression:**

```
Lab 1: Smoke Test (10 min)
├─→ Learn: Basic validation
└─→ Goal: Verify system works

Lab 2: Load Test - Steady (20 min)
├─→ Learn: Normal operations
└─→ Goal: Can it handle expected traffic?

Lab 3: Load Test - Ramp Up (25 min)
├─→ Learn: Find degradation point
└─→ Goal: When does it slow down?

Lab 4: Stress Test (25 min)
├─→ Learn: Find breaking point
└─→ Goal: When does it break?

Lab 5: Spike Test (20 min)
├─→ Learn: Handle traffic surges
└─→ Goal: Can it handle flash sales?

Lab 6: Soak Test (30 min)
├─→ Learn: Long-term stability
└─→ Goal: Any memory leaks?

```
### Lab 1: Smoke Test (15 min total)


First lab is a smoke test. We're verifying basic functionality. 

```bash
# Execute Lab1
docker-compose run --rm artillery run 01-smoke-test.yml --output /reports/01-smoke-test.json --record --key {{Key_from-Prerequisite}}

```

### Lab 2: Load Test - Steady (25 min total)

Now we test with realistic load. This simulates your normal business day. We're looking for: Can the system handle expected traffic sustainably?


```yaml
phases:
  - warmup    # Give system time to initialize
  - sustained # The actual test
  - cooldown  # See if it recovers
```

```bash
# Execute Lab2
docker-compose run --rm artillery run 02-load-test-steady.yml --output /reports/02-load-test-steady.json --record --key {{Key_from-Prerequisite}}

```
### Lab 3: Load Test - Ramp Up (30 min total)


"This is where it gets interesting. We're gradually increasing load to find the degradation point. 

```
Stage 1: 5 req/sec   → Baseline
Stage 2: 10 req/sec  → Still comfortable
Stage 3: 20 req/sec  → Starting to feel it?
Stage 4: 40 req/sec  → Getting stressed
Stage 5: 80 req/sec  → Probably degrading
Stage 6: 100 req/sec → May be failing
```

This test gives the data for capacity planning. If  need to support 200 req/sec but system breaks at 80, we know we need to scale up or optimize.

```bash
# Execute Lab3
docker-compose run --rm artillery run 03-load-test-ramp.yml --output /reports/03-load-test-ramp.json --record --key {{Key_from-Prerequisite}}

```

### Lab 4: Stress Test (30 min total)


"Now we intentionally break the system. We need to know HOW it fails. Does it crash? Slow down? Throw errors? Can it recover?"

The breaking point tells you your absolute ceiling. Your safe operating limit is usually 60-70% of breaking point."

```bash
# Execute Lab4
docker-compose run --rm artillery run 04-stress-test.yml --output /reports/04-stress-test.json --record --key {{Key_from-Prerequisite}}

```

### Lab 5: Spike Test (25 min total)


Flash sales, viral content, breaking news - traffic can spike instantly. This tests if your system can handle it or if you need a waiting room/queue system.

```bash
# Execute Lab5
docker-compose run --rm artillery run 05-spike-test.yml --output /reports/05-spike-test.json --record --key {{Key_from-Prerequisite}}

```

### Lab 6: Soak Test (30 min total)

Long running test.

```bash
# Execute Lab6
docker-compose run --rm artillery run 06-soak-test.yml --output /reports/06-soak-test.json --record --key {{Key_from-Prerequisite}}

```



## Troubleshooting
### Problem: Services won't start

**Error:** Port already in use

**Solution:**
```bash
# Check what's using port 3000
# Mac/Linux:
lsof -i :3000

# Windows:
netstat -ano | findstr :3000

# Either kill that process or change the port in docker-compose.yml
```

---

### Problem: Sample app not responding

**Solution:**
```bash
# Check logs
docker-compose logs sample-app

# Look for "Sample app running on http://0.0.0.0:3000"

# Restart if needed
docker-compose restart sample-app
```

---

### Problem: Artillery tests fail

**Error:** `ECONNREFUSED` or `lookup sample-app failed`

**Solution:**
```bash
# Ensure both containers are running
docker-compose ps

# Restart everything
docker-compose restart


```

---

### Problem: Can't access sample-app from browser

**Solution:**
```bash
# Make sure you're using localhost, not sample-app
# Browser: http://localhost:3000
# Inside Docker: http://sample-app:3000

# Check Docker port mapping
docker-compose ps
# Should show 0.0.0.0:3000->3000/tcp
```

---

### Complete Reset

```bash
# Stop and remove everything
docker-compose down -v

# Remove all images (optional)
docker system prune -a

# Start fresh
docker-compose up -d

## Additional Resources

### Artillery Documentation
- [Official Docs](https://www.artillery.io/docs)
- [Core Concepts](https://www.artillery.io/docs/guides/overview/welcome)
- [Script Reference](https://www.artillery.io/docs/reference/test-script)

### Performance Testing
- [Google SRE Book - Performance](https://sre.google/sre-book/testing-reliability/)


### Metrics & Monitoring
- [Understanding Percentiles](https://www.dynatrace.com/news/blog/why-averages-suck-and-percentiles-are-great/)
- [SLA vs SLO vs SLI](https://cloud.google.com/blog/products/devops-sre/sre-fundamentals-slis-slas-and-slos)
