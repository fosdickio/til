# Layered Network Model

## Layers

### 1 - Physical
- Ethernet (physical wire)
- Bits on the wire

### 2 - Data Link
- Frames
- Switches
- MAC addresses
- Ethernet (CAT5)

### 3 - Network
- Routers
- IP addresses
- Packets

### 4 - Transport
- Maps application layer to transport layer via ports
- TCP/UDP
- Firewall
- Segments

### 5 - Session
### 6 - Presentation
### 7 - Application

---

## Hardware Security (Layer 2)
- Switches use MAC addresses (not IP addresses)
  - Only care about layer 2

## Hardware Security (Layer 3)
- Access Control Lists —> does it match or not match traffic?
  - Deny (don’t match)
  - Permit (match)
  - host == 0.0.0.0
- NAT —> translates one IP to a different IP
- PAT —> translates a port to a different port
- Router + ACL = firewall
- Port forwarding == destination NAT
