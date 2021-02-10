import b0RemoteApi
import time

with b0RemoteApi.RemoteApiClient() as client:
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
