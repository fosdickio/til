# Network Engineering Notes

## General
- On the same network, everything talks via MAC address
- IP address, MAC address, default gateway, subnet mask, and DNS are required to get out to the internet

### Default Gateways
- Default gateway = router
- PC performs subnet mask (255.255.255.0) to determine if destination IP address is on the network
  - If the PC determines the IP address isn’t in the host network, it gets forwarded to the default gateway
- A default gateway’s IP address is pre-configured for computers on the network
  - A PC can only have one default gateway

### Address Resolution Protocol (ARP)
- Address Resolution Protocol (ARP) maps an IP address to a MAC address
  - Broadcasts a request to all devices on the network
  - If the PC at the IP address has that MAC address, then it responds (ARP reply)
  - PC builds an ARP table, so it doesn’t need to repeatedly ask for MAC addresses

### Routers
- Routers have two NICs
  - Can’t have the same address on two different networks
- Routers separate broadcast domains (broadcasts don’t go further than the router)
  - Broadcast - specific frame
  - Flood - flooding the broadcast frame out all of the ports (except the receiving port)

### VLANs
- Virtually separate different networks

### MAC Address Tables
- Map MAC addresses to ports
  - Unplugging a wire from a switch will wipe the corresponding entry in the MAC address table
- Spanning tress shutdown ports to prevent loops
  - Downside: shuts down ports that can be used in a network

---

## Static Routing
- Destination IP is used by routers to route traffic
- Switches forward frames (they don’t change anything)
- Source and destination MAC addresses change when sending traffic through a router
 - MAC addresses are only used on the same network
- Connected routes are learned automatically when they have the following: IP address, subnet mask, interface is enabled, plug it in
- The most specific route in a route table is always matched first
- Connected routes don’t need to be static routes because the router already knows about them
- The higher the number in the / of a route indicates a more specific route (/24 is better than /8)
- Next hop and destination are stored in the route table
- Default route is also a static route

## Dynamic Routing
- /24 at the host level is usually best
- Routing protocols choose best path, dynamically update routes, and reconfigure the network
- A router advertises it’s connected networks
