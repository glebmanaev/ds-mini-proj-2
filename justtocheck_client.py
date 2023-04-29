import grpc

import bookstore_pb2
import bookstore_pb2_grpc

def create_chain():
    # First, we create a channel to the gRPC server.
    channel = grpc.insecure_channel('localhost:50051')

    # Then, we create a stub for the ChainReplicator service.
    stub = chain_pb2_grpc.ChainReplicatorStub(channel)

    # We'll use some example data to create the replication chain.
    head = chain_pb2.ChainItem(
        id=1,
        data=chain_pb2.Data(data="Head data")
    )
    tail = chain_pb2.ChainItem(
        id=2,
        data=chain_pb2.Data(data="Tail data")
    )
    request = chain_pb2.CreateChainRequest(
        head=head,
        tail=tail
    )

    # Finally, we make the gRPC call to create the replication chain.
    response = stub.CreateChain(request)
    print(response.message)

if __name__ == '__main__':
    create_chain()
