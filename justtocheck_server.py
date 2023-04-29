import grpc
import time

import bookstore_pb2
import bokstore_pb2_grpc

class ChainReplicatorServicer(chain_pb2_grpc.ChainReplicatorServicer):
    def CreateChain(self, request, context):
        # Here, you would implement the logic to create the replication chain
        # using the data from the request. For this example, we'll just sleep
        # for a few seconds to simulate some processing time.
        time.sleep(5)

        # Once the replication chain is created, you can return a response
        # indicating whether the operation was successful, along with a
        # message if desired.
        response = chain_pb2.CreateChainResponse(
            success=True,
            message="Replication chain created successfully."
        )
        return response

server = grpc.server(thread_pool=grpc.ThreadPoolExecutor(max_workers=10))
chain_pb2_grpc.add_ChainReplicatorServicer_to_server(
    ChainReplicatorServicer(), server
)
server.add_insecure_port('[::]:50051')
server.start()
server.wait_for_termination()
