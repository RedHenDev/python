

def iterate(iK):
    global fX,fY,fZ,result,iSearchSpace,found
    for i in range(-iSearchSpace,iSearchSpace):
        for j in range(-iSearchSpace,iSearchSpace):
            for k in range(-iSearchSpace,iSearchSpace):
                if i==j or i==k or j==k:
                    # print("Identity: " + str(i) +
                    #     str(j) + str(k))
                    continue
                fX = (i)**3
                fY = (j)**3
                fZ = (k)**3
                result = fX + fY + fZ
                if result==iK:
                    print("Yes! " + str((i)) + " + " +
                        str((j)) + " + " + str((k)))
                    found=True
                    break
            if found: break
        if found: break

    print("All combinations exhausted.")

iSearchSpace = 100

for n in range(1,100):
    iK=n
    print("Target is " + str(iK))
    fX=1
    fY=1
    fZ=1
    result=0
    found=False
    iterate(iK)