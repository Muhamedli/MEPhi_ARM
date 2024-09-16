import roboticstoolbox as rtb

manipulator = rtb.models.Puma560()
print(manipulator)
manipulator.plot(q=manipulator.qz)