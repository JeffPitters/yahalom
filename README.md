# yahalom
Yahalom implementation on python+flask

# Alice:

1. gen num Ra 
2. send to Bob with own id

# Bob: 

1. gen Rb
2. add Rb to recieved message
3. chiper with Bob/Trent common key 
4. adding own id to message
5. send message to Trent

# Trent:
1. gen seanse key
2. create message with seanse key, Ra, Rb, 
3. chiper message with Alice/Trent common key
4. send message to Bob with own id
5. create message with Alice id and seanse key
6. chiper with Bob/Trent common key
7. send with message to Alice

# Alice:
1. fcompare Ra from first message with own Ra
2. if comparing success, send to Bob second message from Trent, chiphered by seanse key

# Bob:
1. get from message seanse key
2. decrypt message, containing Rb
3. compare Rb with own Rb
