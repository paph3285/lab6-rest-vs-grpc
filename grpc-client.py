import sys
import time
import random
import base64
import grpc

import lab6_pb2
import lab6_pb2_grpc


def doAdd(stub, debug=False):
    response = stub.Add(lab6_pb2.addMsg(a=5, b=10))
    if debug:
        print(response)


def doRawImage(stub, debug=False):
    img = open('Flatirons_Winter_Sunrise_edit_2.jpg', 'rb').read()
    response = stub.RawImage(lab6_pb2.rawImageMsg(img=img))
    if debug:
        print(response)


def doDotProduct(stub, debug=False):
    a = [random.random() for _ in range(100)]
    b = [random.random() for _ in range(100)]
    response = stub.DotProduct(lab6_pb2.dotProductMsg(a=a, b=b))
    if debug:
        print(response)


def doJsonImage(stub, debug=False):
    img = open('Flatirons_Winter_Sunrise_edit_2.jpg', 'rb').read()
    encoded_img = base64.b64encode(img).decode('utf-8')
    response = stub.JsonImage(lab6_pb2.jsonImageMsg(img=encoded_img))
    if debug:
        print(response)


if len(sys.argv) < 4:
    print(f"Usage: {sys.argv[0]} <server ip> <cmd> <reps>")
    print("where <cmd> is one of add, rawImage, dotProduct or jsonImage")
    sys.exit(1)

host = sys.argv[1]
cmd = sys.argv[2]
reps = int(sys.argv[3])

channel = grpc.insecure_channel(f"{host}:50051")
stub = lab6_pb2_grpc.Lab6ServiceStub(channel)

print(f"Running {reps} reps against {host}:50051")

if cmd == 'add':
    start = time.perf_counter()
    for _ in range(reps):
        doAdd(stub)
    delta = ((time.perf_counter() - start) / reps) * 1000
    print("Took", delta, "ms per operation")

elif cmd == 'rawImage':
    start = time.perf_counter()
    for _ in range(reps):
        doRawImage(stub)
    delta = ((time.perf_counter() - start) / reps) * 1000
    print("Took", delta, "ms per operation")

elif cmd == 'dotProduct':
    start = time.perf_counter()
    for _ in range(reps):
        doDotProduct(stub)
    delta = ((time.perf_counter() - start) / reps) * 1000
    print("Took", delta, "ms per operation")

elif cmd == 'jsonImage':
    start = time.perf_counter()
    for _ in range(reps):
        doJsonImage(stub)
    delta = ((time.perf_counter() - start) / reps) * 1000
    print("Took", delta, "ms per operation")

else:
    print("Unknown option", cmd)
