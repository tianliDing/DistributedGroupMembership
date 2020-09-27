# DistributedGroupMembership
A distributed group membership simulation, including gossip-style heartbeating and all-to-all heartbeating

### install
To run the scheduler, you have to install APScheduler  

    pip3 install --user apscheduler

### Compile:  
Start server:    

    python ./server.py

Start client:   
 
    python ./client.py

It will start automatically in gossip style heartbeating. You could switch to All-to-all mode by typing in  


    all  
  
in the terminal running server. If you need to switch back to gossip style heartbeating, type the following instead:
  
    gossip

### Method: 
In gossip-style heartbeating, within each round of gossiping(T=1s), each process will randomly send 4 other processes in its membership list (or all processes on list if there are less than four processes on list). In all to all, each processes will send all processes on list.  

### New join:  
Each time there is a new join process, the server will detect and tell the introducer (the first process connected into the server), and the introducer will put it in its own membership list.  

### Leave/Failure detection: 
When there is a failed process or a voluntarily-left process, the timestamp of that process will not be able to be updated after it is down. Therefore, all processes who have it on the membership list will be able to delete it.  

