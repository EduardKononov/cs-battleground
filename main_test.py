import os
import time

import b0RemoteApi

with b0RemoteApi.RemoteApiClient() as client:
    os.environ['B0_RESOLVER'] = 'tcp://localhost:22000'
    sc = client.simxServiceCall()
    try:
        client.simxStartSimulation(sc)
        _, leftMotor = client.simxGetObjectHandle('Pioneer_p3dx_leftMotor', sc)
        _, rightMotor = client.simxGetObjectHandle('Pioneer_p3dx_rightMotor', sc)
        client.simxSetJointTargetVelocity(leftMotor, 1, sc)
        client.simxSetJointTargetVelocity(rightMotor, 1, sc)
        time.sleep(100)
    finally:
        client.simxStopSimulation(sc)
