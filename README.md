# MerkelTree_Blockchain
## **BLOCK**

**PROPERTIES**

1. Data: Data to be held in the block in Character Array
2. Previous hash: Character Array of Hash of the previous block in the chain. If this is the first block to be added, pass in the Genesis Block&#39;s hash.
3. Nonce: Number used only once, will start from 0, irrespective of the input
4. Difficulty: Controls the mine rate for the blockchain. Difficulty of 1 to Start is recommended
5. Hash: hash of the current block
6. Timestamp: Date Time object of the current time.

**FUNCTIONS**

1. Constructor to create a block object by getting all its properties as input. The function should get all the properties as input, create a new block object and assign the input properties as the properties corresponding to the newly created block object.
2. Function to mine genesis block by getting mine rate alone as input. This function must create a new block object and assign some default values as its properties.
3. Function to mine a new block by getting data for the current block and previous block object as input. In this function the nonce value should be set to 0 and a Boolean variable found must be set to 0. Using a while loop until the found variable is false, the following operations must be performed:
  1. Increment the values of nonce by 1
  2. Set the value of timestamp to current data ant time
  3. Set the difficulty of the block using a user-defined method
  4. Create a list called text data for calculating hash value
  5. Let &#39;n&#39; be the values of difficulty, then check if the first &#39;n&#39; characters of hash are zeros, if yes make found as true, else the while loop will be executed again.
4. To set difficulty based on timestamp previous block and current timestamp. In this method we need to check if the time taken for computation of current hash is greater than mine rate, if yes reduce the value of difficulty by one, in other cases increase the value of difficulty.

## **BLOCKCHAIN**

**PROPERTIES**

Chain: Array of Blocks, gets populated with a genesis block

**FUNCTIONS:**

1. Constructor which creates and empty instance of blockchain and mines the genesis block using the method created in previous class.
2. Function which adds a block instance to the blockchain getting the name and data as input. This is done using the method created for mining a block in previous class.
3. Function for replacing the current variable of blockchain with another instance of the blockchain. This method gets the new instance of blockchain as input validates it and if the chain is valid, it replaces the current chain with the new instance.
4. Method to validate a blockchain. In this method using a while loop we iterate through each block of the blockchain. Initially in this while loop we compute the has of the blockchain at that moment and store it in a new variable. The validation of block must contain the following steps.
  1. Compare the values of calculated hash and hash stored in the block of blockchain
  2. Compare the previous hash of the current block and current hash of the previous block
  3. Check if the unsigned value of difference between difficulty of current hash and previous hash is exactly 1.
  4. Check the datatype of the following
    1. Data – number, character or string
    2. Nonce – numeric
    3. Difficulty – numeric

## **NODE**

PROPERTIES

1. Left: left child node object of the current node, initially set to null
2. Right: right child node object of the current node, initially set to null
3. String: string data for corresponding to the node
4. Hash: hash value corresponding to the string present in the node

FUNCTIONS

1. Constructor which initiates the current node object by getting the left child node object, right child node object, string of the current node object and its hash value
2. Method to find the hash value corresponding to the string input

## **MERKLE TREE**

1. Constructor which creates an instance of Merkle tree by getting the list of strings as it&#39;s input.
2. Method which must get string list as an input and create a list of node objects corresponding to all the strings present in list. Then it must check if there are even number of objects present in the list of nodes, if not the method must make a copy of the last node object and append it to the list, preprocessing the list of strings before Merkle tree construction.
3. Method which must get the list of node objects as input construct a Merkle tree. If the number of present in the list is more than two, the right half must be separated, the left half must be separated and must be passed into this same method (recursion). If the number of nodes being passed into the function is exactly two, a new node must be created which turns out to be the root of the two input nodes. The hash value corresponding to this root node is the hash of sum of the hash value corresponding to the two input nodes.
4. Method which returns the root node of the constructed Merkle tree, which turns out to be the final hash.

## **ACCESS DATABASE**

1. Method to check for the presence of a particular login id and if it is present show load the database corresponding to that id or return error telling id doesn&#39;t exist.
2. Method for creating new id which gets the login id and password as input check if user id is unique, if not throw error and updating the database with the new unique id and password. Create a new database in the name of user id for the newly added user.
