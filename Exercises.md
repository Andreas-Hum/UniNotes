

How might the clocks in two computers that are linked by a local network be  
synchronized without reference to an external time source? What factors limit the  
accuracy of the procedure you have described? How could the clocks in a large number of computers connected by the Internet be synchronized? Discuss the accuracy of that procedure.

  

What is the man disadvantage of distributed systems which exploit the infrastructure offered by the Internet? How can this be overcome?

  

The host computers used in peer-to-peer systems are often simply desktop computers in users’ offices or homes. What are the implications of this for the availability and security of any shared data objects that they hold and to what extent can any weaknesses be overcome through the use of replication?

  

There exist services (e.g.: Network Time Protocol service) that can be used to synchronize computer clocks. Explain why, even with these service, no guaranteed bound is given for the difference between two clocks

  

  
1. Speedup Calculation  
A program spends 60% of its execution time in a part that can be parallelized. The rest (40%) must remain sequential.  
  
According to Amdahl's Law, what is the maximum theoretical speedup if the parallel part is executed on:  
a) 2 processors  
b) 4 processors  
c) An infinite number of processors  
  
2. Finding the Parallel Fraction  
An application achieves a speedup of 5 when running on 8 processors. Use Amdahl's Law to determine the fraction of the program that was parallelized.






Phase 1: Use your own means within your team (phone, laptos, timers etc) to simulate a raft-based leader election (only one round) three times: elect 1 of each : 1 leader, 1 team messenger, 1 teacher messenger. In a round where no-one wants to suggest themselves as the respective role, another player is allowed to nominate themselves and then assign the role (since leaders can pick any value they like). 

 - Teacher messenger of each team comes to communicate with teacher. 
 - Team leader will be responsible for handling discussion with whole class. 
 - Team messenger will have to transfer the messages in phase 3. 

Phase 2: You have the following options (burgers, pizza, kebab, McDonnalds). Together pick a version of the reliable consensus algorithm (slide 7, 10, 19) depending on what you think is best. Purpose is to agree on what your team would like to eat. ATTENTION. For some of these algorithms you will need to pick a funtion to apply to the messages. 

 - We wrap up phase 2. Leaders of teams allowed to discuss with whole classroom. 

Phase 3: Again: use only paper when communicating with other teams. Our university has sent us to a giant CS conference and the teams we have formed had different presentations at different times. We would like to go eat together all the AAU people. Some teams might drop out because they were invited by people in the same session as them to go out. 

 - Use paxos to start communicating with other teams. On your papers write your current message content, team names, and ID or anything else paxos requires. Send your messenger and wait for them to get back with the response from other team. Do this at the speed you can. Avoid huge jumps in sequence numbers.

 - Sent your teacher messenger once you are sure you have found the agreed value on food. 

Phase 4: Okay we sit down again and discuss. How big was a quorum today? Any intuition why?


Q1: Give an example why the centralized algorithm (with leader and token) for Mutex does not satisfy the ordering property. 

  

What mechanism could the leader use to fix this? 

  

  

Q2: Give a summary for the total number of messages for Centralized, Token ring, Maekava, and decentralized (R &A)  algorithm for each one of: client delay , syncronization delay, bandwidth, and a major problem you know with this algorithm. 

  

Would you say token ring is "more" fault tolerant that leader token based algorithm? Explain why. Hint: Consider if processes can crash-recover what happens each time. 

  

  

Q3: If the whole system of clients and servers is fully synchronus and each process is single threaded, is mutual exclusion condition ME3, which

specifies entry in happened-before order, relevant? Can it be mitigated without the algorithm changing? 

  

  

Q4: Give a formula for the maximum throughput of a mutual exclusion system in terms of

the synchronization delay.

  

  

Q5: Adapt the central server algorithm for mutual exclusion to handle the crash failure of any client (in any state), assuming that the server is correct and given a reliable failure

detector. Comment on whether the resultant system is fault-tolerant. What would happen if a client that possesses the token is wrongly suspected to have failed?

  

  

Q6: Give the module pseudocode for all 4 algorithms seen in the message parsing case. 

  

Q7: In a certain system, each process typically uses a critical section many times before another process requires it. Explain why Ricart and Agrawala’s multicast-based mutual exclusion algorithm is inefficient for this case, and describe how to improve its performance. Does your adaptation satisfy liveness condition ME2?

  

Q8: Make a process based description of Dekkers algorithm (for two processes). 

  

Q8.1 In Dekker's Algorithm for N processes, let process i request the critical resource CS and let a process j with j < i to request it when queue  = k ( k< j) and again when queue = j + 1. How many times before i can j be granted entrance to the resource? 

  

  

Q9: When we run the two following processes (initially all variables used are 0)

P1  P2

1. x := 1 1. y := 1

2. x := 2 2. b := x

3. a := y 3. if b = 0 then

4. if a = 0 then   4. CS

5.  if x=0

6.  CS

  

under TSO, which values is it possible for P1 to read at line 4 and for P2 at line 2? 

Can both processes enter the CS at the same time?  Why yes or no? What if we replace line 5 for P1 with if x=1?


1.    We said that consensus is not consistency. How can you implement consistency using consensus? Which kind of consistency did you implement?  
  
2.    Argue if non-Partition tolerant systems can still be considered distributed systems.  
  
3.    Consider slide 21 (interleavings)  
    .    Construct an interleaving that is not linearizable but sequentially consistent  
    .    Construct an interleaving that is not sequentially consistent  
    .    What is the minimum number of clients with which you can construct a non-sequentially consistent interleaving?  
  
4.    What is the message complexity of passive replication? What is its delay?  
  
5.    What is the meaning of "Sacrifice linearizability => offload reads to backups!"? What kind of consistency do you end up with?`  
  
6.    What is the message complexity of active replication? What is its delay?  
  
7.    So, why should somebody use active replication?  
  
8.    What is the message complexity in the case of the gossip architecture? What is its delay?  
  
9.    Read operations in the gossip architecture:  
    .    What happens when your second read operation ends on an outdated replica?  
  
10.    Write operations in the gossip architecture:  
    .    Should you apply all the updates in the log when you receive a read request?  
    .    In slide 37, we say "actually, it uses an Executed operation table not to re-apply them, but keep them forever". Why can't we delete the updates?  
  
11.    Chang-Roberts: how can you overcome a crash, after you detected it?  
  
12.    In the bully algorithm, why is safety broken if:  
    .    too tight deadline?  
    .    process IDs reappears?  
    .    system is not synchronous?

1. Why do you have non-POSIX primitives in GFS? In particular, which requirements led you to needing:  
- snapshot  
- record append  
  
2. Your GFS is configured with the usual chunk size (64MB).   
   Your GFS master is storing these metadata: /foo.txt (0x2ef0, 172.31.177.226:8081) (0x2551, 172.31.177.223:8082)  
                                              /bar.txt (0x144f ,172.31.177.223:8082) (0xaaaa, 172.31.177.226:8081) (0x9233, 172.31.177.226:8081)  
   Your client wants to access the following data in its filesystem. Please write down the queries that the client will issue to the GFS master, and what the GFS master will send back to the client.  
- /foo.txt, byte 1000  
- /bar.txt, first byte in its 66th MB  
- /foo.txt, first byte in its 130th MB  
  
3. If I decide to append 10 MBs to a file already 60MB long, what are the actions taken by the GFS master?  
  
4. We said that GFS uses some kind of passive replication.  
   Which characteristics of passive replication are respected by GFS implementation?  
   Which aspects of GFS implementation are not compliant with the usual passive replication approach?  
  
5. Regarding the fault tolerance of the GFS master, we talked about the operations log and the checkpoints.  
   Why do we need two different mechanisms?  
   Where are operations logs and checkpoints saved?  
   How do we decide which one to use, between operations log and checkpoints?  
  
6. How many computers are usually served by one Chubby cell?  
  
7. Why does Chubby use multi-paxos instead of paxos?  
  
8. In Chubby client sessions,   
   what happens to the client sessions when a client crashes? Why?  
   what happens to the client sessions when a master crashes? Why? (feel free to consider or ignore the "jeaopardy" mechanism)  
  
9. In BigTable,  
   why isn't the master serving meta-data to clients (such as on which tabletserver data are located)?  
   which operations are responsibility of the master?  
  
10. In BigTable, what do you get from Chubby when you look for data?  
  
11. Both GFS and Bigtable make the same core design choice – to have a single master. What are the repercussions of a failure of this single master in each case?


12. What was better from a privacy point of view, between pre-microsoft Skype and post-microsoft Skype? What about scalability? What about reliability?  
  
13. How do you find peers once you are connected to a p2p network? And how do you find a first peer to get into the network n the first place?  
  
14. How are different the requirements of p2p file sharing platform vs p2p collaborative applications platforms?  
  
15. What would happen within Napster if a peer is connected via DHCP and changes IP address?  
  
16. On slide 19, we say that "The client fetches file from best host". What do we mean with best host?  
  
17. In the original Gnutella protocol, how could a peer find where a specific file is stored? What is the message complexity of this operation?  
  
18. In the Gnutella 2.0 protocol, a.k.a. FastTrack, how could a peer find where a specific file is stored? What is the message complexity of this operation? How does it compare with the original Gnutella?  
  
19. Without finger tables, what is the message complexity of a query in Chord? What if we are using a finger table? How do they compare?  
  
20. Write down the Chord finger tables of node 8 from slide 34.  
  
21. Why Pastry provides faster early hops?
## Blocks

Completion requirements

1)    Privacy and confidentiality in blockchains:  
    a.    Which kind of identity privacy can be kept?  
    b.    Can transaction data be kept confidential?  
  
2)    Merkle trees for bitcoin:  
    a.    Is it possible to remove all the "transaction data" of a block from the disk, and keep only the Merkle tree head? What is lost by doing that?  
  
3)    Why is the miner protected from a "while(true) {...}" Denial of Service attack in Ethereum / Solidity?  
  
4)    Let us imagine that we want to build a resource-based defenses using memory. That is, your probability of adding the next block to the blockchain is proportional to how much memory you are reserving for the "mining" process.  
    a.    Does it make sense?  
    b.    (HARD) How could you implement this?  
  
5)    Let us imagine that there is a network partition in a proof of work blockchain.  
    a.    What happens to the transaction data when the network partition ends?  
    b.    Does it introduce any inefficiency?  
    c.    Is there any potential for double spending?