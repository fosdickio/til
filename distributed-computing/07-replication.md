# Replication

## Goal of Replication

- State available at more than one node
- Service can be provided from more than one node
- **Benefits of replication:** fault-tolerance, availability, scalability

## Replication Models

![Replication Models](img/replication-models.png)

## Replication Techniques

![Replication Techniques #1](img/replication-techniques-1.png)
![Replication Techniques #2](img/replication-techniques-2.png)

## Replication and Consensus

![Correctness of Replication](img/correctness-of-replication.png)

## Chain Replication

![Replication Overhead](img/replication-overhead.png)

![Chain Replication](img/chain-replication.png)

- Read from tail needed for correctness

![Chain Replication Benefits](img/chain-replication-benefits.png)

## CRAQ

- **CR:** reads limited to tail replica only
- **CRAQ: Chain Replication with Apportioned Queries**
  - Apportioned == divided among the chain replicas
  - Queries == read operations
  - Writes continue to be handled by head replica

![CRAQ](img/craq.png)

- Maintain old and new versions of data at each replica
- When both values present, check with tail

## CRAQ vs. CR Scalability

- CRAQ (-3 or -7) can scale to higher read throughput vs. CR, even as the write load increases
- CRAQ throughput scales with the increase of the number of replicas in the chain (CRAQ-7 vs. CRAQ-3)

![CR vs. CRAQ](img/cr-vs-craq.png)

## Summary

- The right choice depends on:
  - **Workload:** reads, writes
  - **System configuration:** number of nodes, distribution, network properties
  - **Consistency requirements**, failures and fault-tolerance methods
