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
#### 99.9% Availability - Three 9s
| Duration | Acceptable Downtime |
| --- | --- |
| Downtime per year | 8h 45min 57s |
| Downtime per month | 43m 49.7s |
| Downtime per week | 10m 4.8s |
| Downtime per day | 1m 26.4s |

#### 99.99% Availability - Four 9s
| Duration | Acceptable Downtime |
| --- | --- |
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

---

## Domain Name System (DNS)
A domain name system (DNS) translates a domain name such as www.example.com to an IP address.

DNS is hierarchical, with a few authoritative servers at the top level.  Your router or ISP provides information about which DNS server(s) to contact when doing a lookup.  Lower level DNS servers cache mappings, which could become stale due to DNS propagation delays. DNS results can also be cached by your browser or OS for a certain period of time, determined by the time-to-live (TTL).

![Domain Name System (DNS)](img/dns.jpg)

- **NS record (name server)** - Specifies the DNS servers for your domain/subdomain.
- **MX record (mail exchange)** - Specifies the mail servers for accepting messages.
- **A record (address)** - Points a name to an IP address.
- **CNAME (canonical)** - Points a name to another name or CNAME (example.com to www.example.com) or to an A record.

---

## Content Delivery Networks (CDN)
A content delivery network (CDN) is a globally distributed network of proxy servers, serving content from locations closer to the user.  Generally, static files such as HTML/CSS/JS, photos, and videos are served from CDN (although some CDNs such as Amazon's CloudFront support dynamic content).  The site's DNS resolution will tell clients which server to contact.

### Push CDNs
Push CDNs receive new content whenever changes occur on your server. You take full responsibility for providing content, uploading directly to the CDN and rewriting URLs to point to the CDN.  You can configure when content expires and when it is updated.  Content is uploaded only when it is new or changed, minimizing traffic, but maximizing storage.

Sites with a small amount of traffic or sites with content that isn't often updated work well with push CDNs.  Content is placed on the CDNs once, instead of being re-pulled at regular intervals.

### Pull CDNs
Pull CDNs grab new content from your server when the first user requests the content.  You leave the content on your server and rewrite URLs to point to the CDN.  This results in a slower request until the content is cached on the CDN.

A time-to-live (TTL) determines how long content is cached. Pull CDNs minimize storage space on the CDN, but can create redundant traffic if files expire and are pulled before they have actually changed.

Sites with heavy traffic work well with pull CDNs, as traffic is spread out more evenly with only recently-requested content remaining on the CDN.

---

## Load Balancers
Load balancers distribute incoming client requests to computing resources such as application servers and databases.  In each case, the load balancer returns the response from the computing resource to the appropriate client.

Load balancers are effective at:
- Preventing requests from going to unhealthy servers
- Preventing overloading resources
- Helping to eliminate a single point of failure

### Layer 4 Load Balancing
Layer 4 load balancers look at info at the transport layer to decide how to distribute requests.  Generally, this involves the source, destination IP addresses, and ports in the header, but not the contents of the packet.  Layer 4 load balancers forward network packets to and from the upstream server, performing Network Address Translation (NAT).

### Layer 7 Load Balancing
Layer 7 load balancers look at the application layer to decide how to distribute requests.  This can involve contents of the header, message, and cookies.  Layer 7 load balancers terminate network traffic, reads the message, makes a load-balancing decision, then opens a connection to the selected server.

At the cost of flexibility, layer 4 load balancing requires less time and computing resources than layer 7, although the performance impact can be minimal on modern commodity hardware.

### Horizontal Scaling
Load balancers can also help with horizontal scaling, improving performance and availability.  Scaling out using commodity machines is more cost efficient and results in higher availability than scaling up a single server on more expensive hardware (called **vertical scaling**).

## Reverse Proxies
A reverse proxy is a web server that centralizes internal services and provides unified interfaces to the public.  Requests from clients are forwarded to a server that can fulfill it before the reverse proxy returns the server's response to the client.

---

## Databases

### Relational Database Management System (RDBMS)
A relational database like SQL is a collection of data items organized in tables.

**ACID** is a set of properties of relational database transactions.
- **Atomicity** - each transaction is all or nothing
- **Consistency** - any transaction will bring the database from one valid state to another
- **Isolation** - executing transactions concurrently has the same results as if the transactions were executed serially
- **Durability** - once a transaction has been committed, it will remain so

There are many techniques to scale a relational database: **master-slave replication**, **master-master replication**, **federation**, **sharding**, **denormalization**, and **SQL tuning**.

#### Master-Slave Replication
The master serves reads and writes, replicating writes to one or more slaves, which serve only reads.  Slaves can also replicate to additional slaves in a tree-like fashion.  If the master goes offline, the system can continue to operate in read-only mode until a slave is promoted to a master or a new master is provisioned.

#### Master-Master Replication
Both masters serve reads and writes and coordinate with each other on writes.  If either master goes down, the system can continue to operate with both reads and writes.

#### Federation
Federation (or functional partitioning) splits up databases by function.  For example, instead of a single, monolithic database, you could have three databases: forums, users, and products, resulting in less read and write traffic to each database and therefore less replication lag.  Smaller databases result in more data that can fit in memory, which in turn results in more cache hits due to improved cache locality.  With no single central master serializing writes you can write in parallel, increasing throughput.

#### Sharding
Sharding distributes data across different databases such that each database can only manage a subset of the data.  Taking a users database as an example, as the number of users increases, more shards are added to the cluster.

Similar to the advantages of federation, sharding results in less read and write traffic, less replication, and more cache hits.  Index size is also reduced, which generally improves performance with faster queries.

#### Denormalization
Denormalization attempts to improve read performance at the expense of some write performance.  Redundant copies of the data are written in multiple tables to avoid expensive joins.  Some RDBMS such as PostgreSQL and Oracle support materialized views which handle the work of storing redundant information and keeping redundant copies consistent.

### NoSQL
NoSQL is a collection of data items represented in a key-value store, document store, wide column store, or a graph database.  Data is denormalized, and joins are generally done in the application code.  Most NoSQL stores lack true ACID transactions and favor eventual consistency.

#### Document Stores
A document store is centered around documents (XML, JSON, binary, etc), where a document stores all information for a given object.  Document stores provide APIs or a query language to query based on the internal structure of the document itself.  Based on the underlying implementation, documents are organized by collections, tags, metadata, or directories.

Some document stores like MongoDB and CouchDB also provide a SQL-like language to perform complex queries.  DynamoDB supports both key-values and documents.

Document stores provide high flexibility and are often used for working with occasionally changing data.

#### Wide Column Stores
A wide column store's basic unit of data is a column (name/value pair). A column can be grouped in column families (analogous to a SQL table). Super column families further group column families. You can access each column independently with a row key, and columns with the same row key form a row. Each value contains a timestamp for versioning and for conflict resolution.

![Wide Column Store](img/wide-column-store.png)

Google introduced Bigtable as the first wide column store, which influenced the open-source HBase often-used in the Hadoop ecosystem, and Cassandra from Facebook. Stores such as BigTable, HBase, and Cassandra maintain keys in lexicographic order, allowing efficient retrieval of selective key ranges.

Wide column stores offer high availability and high scalability. They are often used for very large data sets.

#### Graph Databases
In a graph database, each node is a record and each arc is a relationship between two nodes.  Graph databases are optimized to represent complex relationships with many foreign keys or many-to-many relationships.

---

## Cache
Caching improves page load times and can reduce the load on your servers and databases.

Databases often benefit from a uniform distribution of reads and writes across its partitions.  Popular items can skew the distribution, causing bottlenecks.  Putting a cache in front of a database can help absorb uneven loads and spikes in traffic.

Types of caching:
- **Client caching** - can be located on the client side (OS or browser), server side, or in a distinct cache layer
- **CDN caching** - CDNs are considered a type of caching
- **Web server caching** - reverse proxies and caches can serve static and dynamic content directly
- **Database caching** - databases usually includes some level of caching in a default configuration, optimized for a generic use case
  - Caching at the database query level - whenever you query the database, hash the query as a key and store the result to the cache. This approach suffers from expiration issues.
  - Caching at the object level - see your data as an object, similar to what you do with your application code.
- **Application caching** - in-memory caches such as Memcached and Redis are key-value stores between your application and your data storage; since the data is held in RAM, it is much faster than typical databases where data it is stored on disk.
  - RAM is more limited than disk, so cache invalidation algorithms such as least recently used (LRU) can help invalidate 'cold' entries and keep 'hot' data in RAM.

Suggestions of what to cache:

- User sessions
- Fully rendered web pages
- Activity streams
- User graph data

### Cache Update Strategies

#### Cache-Aside
The application is responsible for reading and writing from storage.  Subsequent reads of data added to cache are fast.  Cache-aside is also referred to as lazy loading.  Only requested data is cached, which avoids filling up the cache with data that isn't requested.

- Look for entry in cache, resulting in a cache miss
- Load entry from the database
- Add entry to cache
- Return entry

#### Write-Through
The application uses the cache as the main data store, reading and writing data to it, while the cache is responsible for reading and writing to the database.  Write-through is a slow overall operation due to the write operation, but subsequent reads of just written data are fast.

- Application adds/updates entry in cache
- Cache synchronously writes entry to data store
- Return entry

#### Write-Behind
In write-behind, the application does the following:
- Add/update entry in cache
- Asynchronously write entry to the data store, improving write performance

#### Refresh-Ahead
You can configure the cache to automatically refresh any recently accessed cache entry prior to its expiration.  Refresh-ahead can result in reduced latency if the cache can accurately predict which items are likely to be needed in the future.

---

## Asynchronism

### Message Queues
Message queues receive, hold, and deliver messages.  If an operation is too slow to perform inline, you can use a message queue with the following workflow:

- An application publishes a job to the queue, then notifies the user of job status
- A worker picks up the job from the queue, processes it, then signals the job is complete

The user is not blocked and the job is processed in the background.  During this time, the client might optionally do a small amount of processing to make it seem like the task has completed.

### Task Queues
Tasks queues receive tasks and their related data, runs them, then delivers their results.  They can support scheduling and can be used to run computationally-intensive jobs in the background.

---

## Communication

### Hypertext Transfer Protocol (HTTP)
HTTP is a request/response protocol: clients issue requests and servers issue responses with relevant content and completion status info about the request.

### Transmission Control Protocol (TCP)
TCP is a connection-oriented protocol over an IP network.  Connection is established and terminated using a handshake.  All packets sent are guaranteed to reach the destination in the original order and without corruption through:

- Sequence numbers and checksum fields for each packet
- Acknowledgement packets and automatic retransmission

If the sender does not receive a correct response, it will resend the packets.  If there are multiple timeouts, the connection is dropped. 

### User Datagram Protocol (UDP)
Datagrams (analogous to packets) are guaranteed only at the datagram level.  Datagrams might reach their destination out of order or not at all.

UDP can broadcast, sending datagrams to all devices on the subnet.  This is useful with DHCP because the client has not yet received an IP address, thus preventing a way for TCP to stream without the IP address.

UDP is less reliable but works well in real time use cases such as VoIP, video chat, streaming, and real-time multiplayer games.

### Remote Procedure Call (RPC)
In an RPC, a client causes a procedure to execute on a different address space, usually a remote server.  The procedure is coded as if it were a local procedure call, abstracting away the details of how to communicate with the server from the client program.  Popular RPC frameworks include Protobuf, Thrift, and Avro.

### Representational State Transfer (REST)
REST is an architectural style enforcing a client/server model where the client acts on a set of resources managed by the server. The server provides a representation of resources and actions that can either manipulate or get a new representation of resources. All communication must be stateless and cacheable.

There are four qualities of a RESTful interface:

- **Identify resources (URI in HTTP)** - use the same URI regardless of any operation
- **Change with representations (Verbs in HTTP)** - use verbs, headers, and body
- **Self-descriptive error message (status response in HTTP)** - use status codes, don't reinvent the wheel
- **HATEOAS (HTML interface for HTTP)** - your web service should be fully accessible in a browser

---

## Security

The basics:

- Encrypt in transit and at rest.
- Sanitize all user inputs or any input parameters exposed to user to prevent XSS and SQL injection.
- Use parameterized queries to prevent SQL injection.
- Use the principle of least privilege.
