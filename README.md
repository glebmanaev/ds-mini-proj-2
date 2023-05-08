# Distributed Systems, mini-project 2
Dmytro Fedorenko, Glib Manaiev, Ekaterina Sedykh

## Distributed Online Bookstore
The Distributed Online Bookstore project is a distributed system that allows for the storage and retrieval of book prices. The project consists of multiple nodes that communicate with each other to maintain a consistent database of book prices. The nodes are connected in a chain structure, where each node has a successor node to which it forwards requests.

## Usage
To run the project, you will first need to generate the gRPC code from the protocol buffer file. This can be done using the following command:
```
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. bookstore.proto
```

This command generates the Python files bookstore_pb2.py and bookstore_pb2_grpc.py, which are used by the project.

Once the gRPC code has been generated, you can start the nodes using the merged.py script.
```
python merged.py
```

The following commands are available:

1. Local-store-ps: This command creates a number of k processes that act as underlying data stores for the online book shop. These processes are created locally within the Node that executed the command. All processes can be seen as equal at this stage.
```
Local-store-ps k
```
2. Create-chain: This command takes a global view about all the existing data store processes running in all the involved machines and it creates a replication chain based on these processes. Here, processes are required to be interconnected with their respective predecessor and successors references. Moreover, the head and tail of the chains are also selected.
```
Create-chain
```
3. List-chain: After a chain is created, it is possible to list it. This command should list the current status of the chain, highlighting successor, predecessor, head and tail.
```
List-chain
```
4. Write-operation: This command creates a data item with the name of the book passed as parameter along with its respective price. This command can be utilized to update the price of a specific book over time.
```
Write-operation <book-name>, <price>
```
5. List-books: This command lists the available books in the store.
```
List-books
```
6. Read-operation: This command retrieves the price of a particular book name passed as parameter. Notice here that to improve scalability and performance of the system, any data store process can provide a response for a request.
```
Read-operation <book-name>
```
7. Time-out: This sets the time-out to propagate a write update between processes.

8. Data-status: This command will list the status of each data item, whether clean or dirty.
```
Data-status
```
9. Remove-head: This command will remove the current head from the chain.
```
Remove-head
```
10. Restore-head: This command will restore the most recent removed head back to the chain. If the order deviation of operations is higher than 5, then the head to be restored is instead permanently deleted. In contrast, if the order deviation is lower than 5, then the restored head rejoins the chain as a new head and this new head is reconciled (meaning is brought up to date).
```
Restore-head
```

### Bonus ML online bookshop

We used a pre-trained autoregressive language model (GPT-3 by OpenAI) to generate book names based on an input as small as a single keyword or larger.

  Usage is simple `<ML-list-recommend “keyword/part of the name/etc”>`:

``` 
ML-list-recommend melody lady
```
Output:
```
I suggest you: Melody Lady and the Quest for the Perfect Song
```

It generates input based on `"Generate a book name based on the keyword '{keyword}'. Name:"` query. Sometimes the result is too short or too long, so we are regenerationg the response until it has [5,50] symbols length.

* You can get your OpenAI API key [on their website](https://openai.com/product#made-for-developers).
