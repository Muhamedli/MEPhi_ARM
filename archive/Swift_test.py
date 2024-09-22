import roboticstoolbox as rtb

manipulator = rtb.models.MEPhI_ARM()
print(manipulator)
manipulator.plot(q=manipulator.qr)