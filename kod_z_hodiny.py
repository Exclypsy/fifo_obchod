import time
nakupujuci = [150,170,175,210,400]
cas0 = time.time()
while (time.time() - cas0) < 3600/100:
    if len(nakupujuci)>0 and time.time()-cas0 >= nakupujuci[0]/100:
        print("nakupujuci prichadza", nakupujuci[0])
        del(nakupujuci[0])