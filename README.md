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


## Troubleshooting

## Additional Resources
