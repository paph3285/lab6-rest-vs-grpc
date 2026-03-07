from concurrent import futures
import grpc
import io
import base64
from PIL import Image

import lab6_pb2
import lab6_pb2_grpc


class Lab6ServiceServicer(lab6_pb2_grpc.Lab6ServiceServicer):
    def Add(self, request, context):
        return lab6_pb2.addReply(sum=request.a + request.b)

    def RawImage(self, request, context):
        try:
            io_buffer = io.BytesIO(request.img)
            img = Image.open(io_buffer)
            return lab6_pb2.imageReply(width=img.size[0], height=img.size[1])
        except Exception:
            return lab6_pb2.imageReply(width=0, height=0)

    def DotProduct(self, request, context):
        try:
            result = sum(x * y for x, y in zip(request.a, request.b))
            return lab6_pb2.dotProductReply(dotproduct=result)
        except Exception:
            return lab6_pb2.dotProductReply(dotproduct=0.0)

    def JsonImage(self, request, context):
        try:
            img_bytes = base64.b64decode(request.img)
            io_buffer = io.BytesIO(img_bytes)
            img = Image.open(io_buffer)
            return lab6_pb2.imageReply(width=img.size[0], height=img.size[1])
        except Exception:
            return lab6_pb2.imageReply(width=0, height=0)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    lab6_pb2_grpc.add_Lab6ServiceServicer_to_server(Lab6ServiceServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("gRPC server running on port 50051")
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
