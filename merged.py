import grpc
from concurrent import futures
import random
import time
import bookstore_pb2
import bookstore_pb2_grpc
from threading import Timer
import openai

def generate_book_name(keyword):
    prompt = (f"Generate a book name based on the keyword '{keyword}'. Name:")

    # Generate book name with GPT-3
    # If book name is too short or too long, try again
    book_name = [0]*51
    while len(book_name) < 5 or len(book_name) > 50:
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=prompt,
            max_tokens=50,
            n=1,
            stop=None,
            temperature=0.5,
        )
        book_name = response.choices[0].text.strip()

    return book_name

class DataStoreService(bookstore_pb2_grpc.DataStoreServicer):
    def __init__(self, port):
        self.data = {}
        self.port = port
        self.successor = None
        self.head = False
        self.tail = False
        self.timeout = 10
        self.head_node = None
        self.data_status = {}
        print(f"DataStoreService initialized at port {self.port}")

    def SetSuccessor(self, request, context):
        response = bookstore_pb2.SetSuccessorResponse(success = True)
        try:
            print(f"Connecting to successor at port {request.successor}")
            self.successor = bookstore_pb2_grpc.DataStoreStub(grpc.insecure_channel(f"localhost:{request.successor}"))
        except grpc.RpcError:
            response.success = False
            print(f"Could not connect to successor at port {request.successor}")
        
        return response
    
    def SetHeadNode(self, request, context):
        print(f"Setting head node to {request.head_node_port}")
        response = bookstore_pb2.SetHeadNodeResponse(success = True)
        try:
            head_node_stub = bookstore_pb2_grpc.DataStoreStub(grpc.insecure_channel(f"localhost:{request.head_node_port}"))
            self.head_node = head_node_stub
            if not self.tail:
                self.successor.SetHeadNode(request)
        except grpc.RpcError:
            response.success = False
            print(f"Could not connect to node {self.successor.port}")
        
        return response
    
    def DeclareHead(self, request, context):
        self.head = True
        print(f"Head node declared at port {self.port}")
        self.successor.SetHeadNode(bookstore_pb2.SetHeadNodeRequest(head_node_port=self.port))
        return bookstore_pb2.DeclareHeadResponse(success = True)
    
    def DeclareTail(self, request, context):
        self.tail = True
        return bookstore_pb2.DeclareTailResponse(success = True)
    
    def UnsetHead(self, request, context):
        self.head = False
        return bookstore_pb2.UnsetHeadResponse(success = True)
    
    def UnsetTail(self, request, context):
        self.tail = False
        return bookstore_pb2.UnsetTailResponse(success = True)
    
    def DeleteData(self, request, context):
        self.data = {}
        self.data_status = {}
        if not self.tail:
            return self.successor.DeleteData(request)
        return bookstore_pb2.DeleteDataResponse(success = True)
    
    def _propagate_write(self, request):
        try:
            response = self.successor.WriteOperation(request)
            return response.success
        except grpc.RpcError:
            print(f"Error propagating update to {self.successor}")
            return False
        
    def ConfirmWrite(self, request, context):
        if request.book_name in self.data.keys():
            return bookstore_pb2.ConfirmWriteResponse(success = True)
        else:
            return bookstore_pb2.ConfirmWriteResponse(success = False)
    
    def WriteOperation(self, request, context):
        if not self.head:        
            response = self.head_node.ConfirmWrite(bookstore_pb2.ConfirmWriteRequest(book_name=request.book_name))
        if self.head or response.success:
            self.data[request.book_name] = request.price
            success = True
            self.data_status[request.book_name] = "dirty"
            if not self.tail:
                Timer(self.timeout, self._propagate_write, [request]).start()
            if self.tail:
                print(f"Update to {request.book_name} propagated to tail")
                try:
                    response = self.successor.ConfirmTransaction(bookstore_pb2.ConfirmTransactionRequest(book_name=request.book_name))
                    success = response.success
                except grpc.RpcError:
                    print(f"Error confirming transaction with {self.successor}")
                    success = False
            
            return bookstore_pb2.WriteOperationResponse(book_name=request.book_name, price=request.price, success=success)
        return bookstore_pb2.WriteOperationResponse(book_name=request.book_name, price=request.price, success=False)
    
    def UpdateDataStatus(self, request, context):
        data_status = {}
        for i, book_name in enumerate(request.book_names):
            self.data_status[book_name] = request.statuses[i]
        if not self.tail:
            return self.successor.UpdateDataStatus(request)
        return bookstore_pb2.UpdateDataStatusResponse(success = True)

    def ConfirmTransaction(self, request, context):
        if request.book_name in self.data.keys():
            self.data_status[request.book_name] = "clean"
            book_names, statuses = [], []
            for book_name, status in self.data_status.items():
                book_names.append(book_name)
                statuses.append(status)
            self.successor.UpdateDataStatus(bookstore_pb2.UpdateDataStatusRequest(book_names=book_names, statuses=statuses))
            return bookstore_pb2.ConfirmTransactionResponse(success = True)
        return bookstore_pb2.ConfirmTransactionResponse(success = False)
    
    def ConfirmRead(self, request, context):
        if request.book_name in self.data.keys() and self.data_status[request.book_name] == "clean":
            return bookstore_pb2.ConfirmReadResponse(success = True)
        else:
            return bookstore_pb2.ConfirmReadResponse(success = False)
    
    def ReadOperation(self, request, context):
        if self.head:
            if request.book_name in self.data.keys():
                return bookstore_pb2.ReadOperationResponse(price=self.data[request.book_name])
            else:
                return bookstore_pb2.ReadOperationResponse(price=0)
        else:
            confirmation = self.head_node.ConfirmRead(bookstore_pb2.ConfirmReadRequest(book_name=request.book_name))
            if confirmation.success:
                return bookstore_pb2.ReadOperationResponse(price=self.data[request.book_name])
            else:
                response = self.head_node.ReadOperation(bookstore_pb2.ReadOperationRequest(book_name=request.book_name))
                return response
            
    def ListOperation(self, request, context):
        if self.head:
            return bookstore_pb2.ListOperationResponse(books=[str(key) + " = " + str(value) + " EUR" for key, value in self.data.items()])
        else:
            return self.head_node.ListOperation(request)
        
    def DataStatus(self, request, context):
        if self.head:
            return bookstore_pb2.DataStatusResponse(data_status=[str(key) + " – " + str(value) for key, value in self.data_status.items()])
        else:
            return self.head_node.DataStatus(request)
        
    def SetTimeout(self, request, context):
        self.timeout = request.timeout
        if not self.tail:
            return self.successor.SetTimeout(request)
        return bookstore_pb2.SetTimeoutResponse(success = True)


class BookStoreService(bookstore_pb2_grpc.BookStoreServicer):
    def __init__(self, node_id, other_nodes):
        self.local_datastores = []
        self.chain = []
        self.node_id = node_id
        self.other_nodes = other_nodes
        self.data_servers = []
        self.last_removed_head = None

    def LocalStorePs(self, request, context):
        if not self.local_datastores:
            for i in range(request.k):
                ps_port = int(f"5{self.node_id:02}{i+1:02}")

                self.data_servers.append(grpc.server(futures.ThreadPoolExecutor(max_workers=10)))
                bookstore_pb2_grpc.add_DataStoreServicer_to_server(DataStoreService(ps_port), self.data_servers[-1])
                self.data_servers[-1].add_insecure_port(f"localhost:{ps_port}")
                self.data_servers[-1].start()

                self.local_datastores.append(ps_port)

            return bookstore_pb2.LocalStorePsResponse(message=f"{request.k} processes created in Node #{self.node_id}")
        return bookstore_pb2.LocalStorePsResponse(message=f"Node #{self.node_id} already has data store processes")
    
    def GetLocalDataStores(self, request, context):
        return bookstore_pb2.GetLocalDataStoresResponse(data_stores=self.local_datastores)
    
    def RemoveChain(self, request, context):
        with grpc.insecure_channel(f"localhost:{self.chain[0]}") as channel:
            stub = bookstore_pb2_grpc.DataStoreStub(channel)
            response = stub.DeleteData(bookstore_pb2.DeleteDataRequest())
            if not response.success:
                return bookstore_pb2.CreateChainResponse(success=False, message="Error removing chain")
            else:
                print("Data deleted successfully")

        with grpc.insecure_channel(f"localhost:{self.chain[0]}") as channel:
            stub = bookstore_pb2_grpc.DataStoreStub(channel)
            response = stub.UnsetHead(bookstore_pb2.UnsetHeadRequest())
        
        with grpc.insecure_channel(f"localhost:{self.chain[-1]}") as channel:
            stub = bookstore_pb2_grpc.DataStoreStub(channel)
            response = stub.UnsetTail(bookstore_pb2.UnsetTailRequest())
        
        self.chain = []

        return self.CreateChain(request, context)

    def CreateChain(self, request, context):
        if self.chain:
            #TODO: Implement chain re-creation
            return bookstore_pb2.CreateChainResponse(success=False, message="Chain already exists. Use RemoveHead to remove the current head.")
        
        datastores = self.local_datastores.copy()
        for node_id in self.other_nodes:
            with grpc.insecure_channel(f"localhost:5{node_id:02}00") as channel:
                stub = bookstore_pb2_grpc.BookStoreStub(channel)
                response = stub.GetLocalDataStores(bookstore_pb2.GetLocalDataStoresRequest())
                datastores+=response.data_stores
        
        self.chain = [random.choice(datastores)]
        while len(self.chain) < len(datastores):
            successors = [k for k in datastores if k not in self.chain]
            successor = random.choice(successors)

            with grpc.insecure_channel(f"localhost:{self.chain[-1]}") as channel:
                stub = bookstore_pb2_grpc.DataStoreStub(channel)
                response = stub.SetSuccessor(bookstore_pb2.SetSuccessorRequest(successor=int(successor)))

            self.chain.append(successor)
            print(f"Successor of {self.chain[-2]} is {self.chain[-1]}")

        with grpc.insecure_channel(f"localhost:{self.chain[-1]}") as channel:
            print(f"Setting head as successor of tail")
            stub = bookstore_pb2_grpc.DataStoreStub(channel)
            response = stub.SetSuccessor(bookstore_pb2.SetSuccessorRequest(successor=self.chain[0]))
            
        with grpc.insecure_channel(f"localhost:{self.chain[-1]}") as channel:
            print(f"Setting {self.chain[-1]} as tail")
            stub = bookstore_pb2_grpc.DataStoreStub(channel)
            response = stub.DeclareTail(bookstore_pb2.DeclareTailRequest())

        with grpc.insecure_channel(f"localhost:{self.chain[0]}") as channel:
            print(f"Setting {self.chain[0]} as head")
            stub = bookstore_pb2_grpc.DataStoreStub(channel)
            response = stub.DeclareHead(bookstore_pb2.DeclareHeadRequest())
        
        for other_node_id in self.other_nodes:
            with grpc.insecure_channel(f"localhost:5{other_node_id:02}00") as channel:
                stub = bookstore_pb2_grpc.BookStoreStub(channel)
                response = stub.SetChain(bookstore_pb2.SetChainRequest(chain=self.chain))

        return bookstore_pb2.CreateChainResponse(success=True, message="Chain created successfully")
    
    def SetChain(self, request, context):
        self.chain = request.chain
        return bookstore_pb2.SetChainResponse(message="Chain set successfully")

    def ListChain(self, request, context):
        if not self.chain:
            return bookstore_pb2.ListChainResponse(chain="No chain found. Use CreateChain to create a chain.")
        chain_str = "->".join([f"Node{int(str(port)[1:3])}-ps{int(str(port)[3:])} (Head)" if i == 0 else f"Node{int(str(port)[1:3])}-ps{int(str(port)[3:])} (Tail)" if i == len(self.chain)-1 else f"Node{int(str(port)[1:3])}-ps{int(str(port)[3:])}" for i, port in enumerate(self.chain)])
        return bookstore_pb2.ListChainResponse(chain=chain_str)

    def WriteOperation(self, request, context):
        if not self.chain:
            return bookstore_pb2.WriteOperationResponse(success=False, book_name="", price=-1)
        head_port = self.chain[0]
        with grpc.insecure_channel(f"localhost:{head_port}") as channel:
            stub = bookstore_pb2_grpc.DataStoreStub(channel)
            response = stub.WriteOperation(request)
        return response

    def ListBooks(self, request, context):
        if not self.chain:
            return bookstore_pb2.ListBooksResponse()
        with grpc.insecure_channel(f"localhost:{self.chain[0]}") as channel:
            stub = bookstore_pb2_grpc.DataStoreStub(channel)
            response = stub.ListOperation(request)
        return response

    def ReadOperation(self, request, context):
        if not self.chain:
            return bookstore_pb2.ReadOperationResponse(price=0)
        current_ps = random.choice(self.chain)
        with grpc.insecure_channel(f"localhost:{current_ps}") as channel:
            stub = bookstore_pb2_grpc.DataStoreStub(channel)
            response = stub.ReadOperation(request)
        return response

    def SetTimeout(self, request, context):
        if not self.chain:
            return bookstore_pb2.SetTimeoutResponse(success=False)
        with grpc.insecure_channel(f"localhost:{self.chain[0]}") as channel:
            stub = bookstore_pb2_grpc.DataStoreStub(channel)
            response = stub.SetTimeout(request)
        return response

    def DataStatus(self, request, context):
        if not self.chain:
            return bookstore_pb2.DataStatusResponse()
        with grpc.insecure_channel(f"localhost:{self.chain[0]}") as channel:
            stub = bookstore_pb2_grpc.DataStoreStub(channel)
            response = stub.DataStatus(request)
        return response

    def RemoveHead(self, request, context):
        if not self.chain:
            return bookstore_pb2.ListChainResponse(chain="")
        if len(self.chain) == 1:
            self.chain = []
        else:
            self.last_removed_head = self.chain.pop(0)
            with grpc.insecure_channel(f"localhost:{self.chain[0]}") as channel:
                stub = bookstore_pb2_grpc.DataStoreStub(channel)
                response = stub.DeclareHead(bookstore_pb2.DeclareHeadRequest())
            with grpc.insecure_channel(f"localhost:{self.chain[-1]}") as channel:
                stub = bookstore_pb2_grpc.DataStoreStub(channel)
                response = stub.SetSuccessor(bookstore_pb2.SetSuccessorRequest(successor=self.chain[0]))
            with grpc.insecure_channel(f"localhost:{self.last_removed_head}") as channel:
                stub = bookstore_pb2_grpc.DataStoreStub(channel)
                response = stub.UnsetHead(bookstore_pb2.UnsetHeadRequest())
            for other_node_id in self.other_nodes:
                with grpc.insecure_channel(f"localhost:5{other_node_id:02}00") as channel:
                    stub = bookstore_pb2_grpc.BookStoreStub(channel)
                    response = stub.SetChain(bookstore_pb2.SetChainRequest(chain=self.chain))
        return self.ListChain(request, context)

    #def RestoreHead(self, request, context):
    #    # TODO: Implement RestoreHead
    #    return bookstore_pb2.RestoreHeadResponse(message="Head restored successfully")\

    def RestoreHead(self, request, context): 
        if self.last_removed_head is None: 
            return bookstore_pb2.RestoreHeadResponse(success=False, message="No head to restore") 
    
        order_deviation = self._get_order_deviation() 
        if order_deviation > 5: 
            self.last_removed_head = None 
            return bookstore_pb2.RestoreHeadResponse(success=False, message="Head could not be restored") 
    
        with grpc.insecure_channel(f"localhost:{self.last_removed_head}") as channel: 
            stub = bookstore_pb2_grpc.DataStoreStub(channel) 
            response = stub.DeclareHead(bookstore_pb2.DeclareHeadRequest()) 
            if not response.success: 
                self.last_removed_head = None 
                return bookstore_pb2.RestoreHeadResponse(success=False, message="Head could not be restored") 
        
        self.chain.insert(0, self.last_removed_head) 
        self.last_removed_head = None 
        for other_node_id in self.other_nodes: 
            with grpc.insecure_channel(f"localhost:5{other_node_id:02}00") as channel: 
                stub = bookstore_pb2_grpc.BookStoreStub(channel) 
                response = stub.SetChain(bookstore_pb2.SetChainRequest(chain=self.chain)) 
    
        return bookstore_pb2.RestoreHeadResponse(success=True, message="Head restored successfully") 
 
    def _get_order_deviation(self): 
        if not self.chain: 
            return 0 
        with grpc.insecure_channel(f"localhost:{self.chain[0]}") as channel: 
            stub = bookstore_pb2_grpc.DataStoreStub(channel) 
            response = stub.DataStatus(bookstore_pb2.DataStatusRequest()) 
        if not response.data_status: 
            return 0 
        head_operations = response.data_status
        chain_operations = [f"{self.node_id}-{i}" for i in range(len(self.chain)-1, -1, -1)] 
        deviation = 0 
        while deviation < len(head_operations) and deviation < len(chain_operations): 
            if head_operations[deviation] != chain_operations[deviation]: 
                break 
            deviation += 1 
        return len(head_operations) - deviation + len(chain_operations) - deviation

if __name__ == '__main__':
    openai.api_key = "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"
    
    while True:
        try:
            node_id = int(input("Enter node id: "))
            master_port = int(f"5{node_id:02}00")
            break
        except KeyboardInterrupt:
            exit(0)
        except:
            print("Invalid node id. Node id must be integer value. Try again.")
            continue
    while True:
        try:
            other_nodes = input("Enter other node ids (comma separated): ")
            other_nodes = [int(node) for node in other_nodes.split(",")] if other_nodes else []
            break
        except KeyboardInterrupt:
            exit(0)
        except:
            print("Invalid node ids. Node ids must be integer values. Try again.")
            continue
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    bookstore_pb2_grpc.add_BookStoreServicer_to_server(BookStoreService(node_id, other_nodes), server)
    server.add_insecure_port(f"localhost:{master_port}")
    server.start() 
    print(f"bookstore server started on port {master_port}...")
    try:
        while True:
            with grpc.insecure_channel(f"localhost:{master_port}") as channel:
                stub = bookstore_pb2_grpc.BookStoreStub(channel)

                while True:
                    command = input("Enter a command: ").strip()
                    if not command:
                        continue

                    parts = command.split()
                    if parts[0] == "Local-store-ps":
                        if len(parts) < 2:
                            print("Usage: Local-store-ps <k>")
                            continue
                        try:
                            k = int(parts[1])
                        except ValueError:
                            print("Invalid value for k")
                            continue
                        response = stub.LocalStorePs(bookstore_pb2.LocalStorePsRequest(k=k))
                        print(response.message)

                    elif parts[0] == "Create-chain":
                        response = stub.CreateChain(bookstore_pb2.CreateChainRequest())
                        print(response.message)
                        if not response.success:
                            command = input("Do you wish to re-create chain (all data will be lost) answer yes/no: ").strip()
                            if command == "yes":
                                response = stub.RemoveChain(bookstore_pb2.CreateChainRequest())
                                print(response.message)
                            elif command != "no":
                                print("Invalid command, chain not re-created")
                            

                    elif parts[0] == "List-chain":
                        response = stub.ListChain(bookstore_pb2.ListChainRequest())
                        print(response.chain)

                    elif parts[0] == "Write-operation":
                        if len(parts) < 3:
                            print("Usage: Write-operation <book_name> <price>")
                            continue
                        try:
                            price = float(parts[-1])
                        except ValueError:
                            print("Invalid price value")
                            continue
                        book_name = " ".join(parts[1:-1])
                        response = stub.WriteOperation(bookstore_pb2.WriteOperationRequest(book_name=book_name, price=price))
                        print(f"{response.book_name} = {response.price} EUR")
                       
                    elif parts[0] == "ML-list-recommend":
                        if len(parts) < 2:
                            print("Usage: ML-list-recommend <keyword/part of the name/etc>")
                            continue
                        keywords = " ".join(parts[1:])
                        book_name = generate_book_name(keywords)
                        print(f"I suggest you: {book_name}")

                    elif parts[0] == "List-books":
                        response = stub.ListBooks(bookstore_pb2.ListBooksRequest())
                        for i, book in enumerate(response.books):
                            print(f"{i+1}) {book}")

                    elif parts[0] == "Read-operation":
                        if len(parts) < 2:
                            print("Usage: Read-operation <book_name>")
                            continue
                        book_name = " ".join(parts[1:])
                        response = stub.ReadOperation(bookstore_pb2.ReadOperationRequest(book_name=book_name))
                        if response.price > 0:
                            print(f"{book_name} = {response.price} EUR")
                        else:
                            print(f"{book_name} not yet in stock")

                    elif parts[0] == "Set-timeout":
                        if len(parts) < 2:
                            print("Usage: Set-timeout <seconds>")
                            continue
                        try:
                            timeout = int(parts[1])
                        except ValueError:
                            print("Invalid value for time")
                            continue
                        if timeout < 0:
                            print("Invalid value for time")
                            continue
                        response = stub.SetTimeout(bookstore_pb2.SetTimeoutRequest(timeout=timeout))
                        if response.success:
                            print("Timeout set successfully")
                        else:
                            print("Timeout could not be set")

                    elif parts[0] == "Data-status":
                        response = stub.DataStatus(bookstore_pb2.DataStatusRequest())
                        for i, data_status in enumerate(response.data_status):
                            print(f"{i+1}) {data_status}")

                    elif parts[0] == "Remove-head":
                        response = stub.RemoveHead(bookstore_pb2.ListChainRequest())
                        print(response.chain)

                    elif parts[0] == "Restore-head":
                        response = stub.RestoreHead(bookstore_pb2.RestoreHeadRequest())
                        print(response.message)

                    else:
                        print(f"Unknown command: {parts[0]}")
    except KeyboardInterrupt:
        server.stop(0)
   
