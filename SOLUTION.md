| Method | Local | Same-Zone | Different Region |
|---|---|---|---|
| REST add | ~3–5 ms | ~4–9 ms | 307.92 ms |
| gRPC add | ~1 ms | ~1.07 ms | 154.08 ms |
| REST rawimg | ~40 ms | ~42 ms | 1262.54 ms |
| gRPC rawimg | ~13 ms | ~13.85 ms | 191.94 ms |
| REST dotproduct | ~4 ms | ~4.96 ms | 319.95 ms |
| gRPC dotproduct | ~1.3 ms | ~1.34 ms | 152.68 ms |
| REST jsonimg | ~42 ms | ~42 ms | 1430.32 ms |
| gRPC jsonimg | ~32 ms | ~32.61 ms | 220.41 ms |
| PING | <1 ms | ~0.65 ms | 151.07 ms |

Network latency has a major impact on the performance of both REST and gRPC when the client and server are located in different regions. The ping latency between the US and Europe virtual machines averaged about 151 ms, which closely matches the latency observed for lightweight operations such as `add` and `dotproduct`. This indicates that when computation is small, the network round-trip time dominates the total response time. Larger operations such as `rawimg` and `jsonimg` take longer because they involve transmitting larger payloads across the network. In general, gRPC consistently performed faster than REST because it uses a binary protocol and maintains a single persistent TCP connection. In contrast, REST creates a new TCP connection for each request, which adds additional overhead. As network latency increases, the efficiency advantages of gRPC become more noticeable.





dc


Summary of Findings:



The results show a consistent performance difference between REST and gRPC across the different environments. When the services were running locally or within the same zone, gRPC generally performed faster than REST. This is likely because gRPC maintains a persistent HTTP/2 connection and uses efficient binary serialization through Protocol Buffers, while REST typically creates a new TCP connection for each request and sends data using text formats like JSON. Because of this, REST introduces additional overhead for repeated requests.

As network distance increased, especially when running tests between different regions, overall latency increased substantially for both methods. The ping test between the US and Europe virtual machines averaged about ~151 ms, which closely matches the latency observed for lightweight operations such as `add` and `dotproduct`. This indicates that when the computation itself is small, the network round-trip time dominates the total response time. In other words, most of the delay is caused by the physical distance between the machines rather than the RPC framework itself.

Larger operations such as `rawimg` and `jsonimg` take longer because they involve transmitting larger payloads across the network. This increases the amount of data that must travel between regions, which adds additional latency on top of the base network delay.

Overall, these experiments demonstrate an important concept in distributed and datacenter systems: while gRPC can reduce serialization overhead and improve efficiency through persistent connections, network latency still plays a major role in overall performance. When services are geographically separated, the physical network distance and round-trip time become the primary factors affecting response time regardless of whether REST or gRPC is used.
