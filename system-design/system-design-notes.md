# System Design Notes

## Performance vs. Scalability
- A service is scalable if it results in increased performance in a manner proportional to resources added.
- If you have a performance problem, your system is slow for a single user.  If you have a scalability problem, your system is fast for a single user, but slow under heavy load.

## Latency vs. Throughput
- Latency is the time to perform some action or to produce some result.
- Throughput is the number of such actions or results per unit of time.
- Generally, you should aim for maximal throughput with acceptable latency.

## Availability vs. Consistency
- In a distributed computer system, you can only support two of the following guarantees:
  - **Consistency** - every read receives the most recent write or an error
  - **Availability** - every request receives a response without any guarantee that it contains the most recent version of the information
  - **Partition Tolerance** - the system continues to operate despite arbitrary partitioning due to network failures
- Networks aren't reliable, so you'll need to support partition tolerance.  You'll need to make a software tradeoff between consistency and availability.

## Availability Patterns
There are two complementary patterns to support high availability: **fail-over** and **replication**.

### Fail-Over
#### Active-Passive
- Heartbeats are sent between the active and the passive server on standby.  If the heartbeat is interrupted, the passive server takes over the active's IP address and resumes service.
- The length of downtime is determined by whether the passive server is already running in "hot" standby or whether it needs to start up from "cold" standby.  Only the active server handles traffic.
- Active-passive failover can also be referred to as master-slave failover.

#### Active-Active
- In active-active, both servers are managing traffic, spreading the load between them.
- If the servers are public-facing, the DNS would need to know about the public IPs of both servers.  If the servers are internal-facing, application logic would need to know about both servers.
- Active-active failover can also be referred to as master-master failover.

### Availability Numbers
#### 99.9% availability - three 9s
| Duration | Acceptable downtime |
--- | --- | ---
| Downtime per year | 8h 45min 57s |
| Downtime per month | 43m 49.7s |
| Downtime per week | 10m 4.8s |
| Downtime per day | 1m 26.4s |

#### 99.99% availability - four 9s
| Duration | Acceptable downtime |
--- | --- | ---
| Downtime per year | 52min 35.7s |
| Downtime per month | 4m 23s |
| Downtime per week | 1m 5s |
| Downtime per day | 8.6s |

#### Availability: In Parallel vs. In Sequence
If a service consists of multiple components prone to failure, the service's overall availability depends on whether the components are in sequence or in parallel.

##### In Sequence
Overall availability decreases when two components with availability < 100% are in sequence:
```
Availability (Total) = Availability (Foo) * Availability (Bar)
```
If both `Foo` and `Bar` each had 99.9% availability, their total availability in sequence would be 99.8%.

##### In Parallel
Overall availability increases when two components with availability < 100% are in parallel:
```
Availability (Total) = 1 - (1 - Availability (Foo)) * (1 - Availability (Bar))
```
If both `Foo` and `Bar` each had 99.9% availability, their total availability in parallel would be 99.9999%.
