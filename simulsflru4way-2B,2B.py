#128K data cache and instruction cache with 2 bytes block for instruction cache and 2 bytes per block data cache
file=open("D:/Computer architecture/Project/main/benchmarks/spice.din","r")
addresses=file.readlines()
addresses_new=[]
for i in range(len(addresses)):
    addresses_new.append(bin(int(addresses[i][2:],16))[2:]) #converting the hexadecimal addreses to binary
    addresses_new[i]=addresses_new[i].zfill(32)
print "total number of addresses in trace"
print len(addresses)
p1=2
p2=0
p3=1
m1="%x"%p1
m2="%x"%p2
m3="%x"%p3
dc={}#1st associativity data cache
dl={}#2nd associativity data cache
dp={}#3rd associativity data cache
dq={}#4th associativity data cache
ic={}#1st associativity icache
il={}#2nd associativity icache
ip={}#3rd associativity icache
iq={}#4th associativity icache
ifreq={}
dfreq={}
#initialisation of icache
for i in range(16384):
        p=(bin(i))[2:].zfill(14)
        ic[p]=0
        il[p]=0
        ip[p]=0
        iq[p]=0
#initiallisation of dcache
for i in range(16384):
        p=(bin(i))[2:].zfill(14)
        dc[p]=0
        dl[p]=0
        dp[p]=0
        dq[p]=0
l=[]
ind=[]
tagi=[]#tag list of icache
tagd=[]#tag list of dcache
k=0#count of instruction addresses
kd=0#count of data addresses
hitd=0#count for data hits
missd=0#count for data misses
hiti=0#count for instruction hits
missi=0#count for data misses
for i in range(len(addresses)):
    if addresses[i][0]==m1:
        ind.append(addresses_new[i][17:31])
        k=k+1
        tagi.append(addresses_new[i][0:17])
    elif addresses[i][0]==m2 or addresses[i][0]==m3:
        tagd.append(addresses_new[i][0:17])
        kd=kd+1
#initialization of frequency counters for instruction cache
for i in tagi:
    ifreq[i]=0
#initialization of frequency counters for data cache
for i in tagd:
    dfreq[i]=0
ifreq[0]=0
dfreq[0]=0
for i in range(len(addresses_new)):
    if addresses[i][0]==m1:  
            indi=addresses_new[i][17:31]    
            tagi=addresses_new[i][0:17]
            if ic[indi]==tagi:
                hiti=hiti+1
                t1=iq[indi]
                t2=ip[indi]
                t3=il[indi]
                t4=ic[indi]
                ic[indi]=ip[indi]
                ip[indi]=il[indi]
                il[indi]=iq[indi]
                iq[indi]=t4
                ifreq[tagi]=ifreq[tagi]+1
            elif ip[indi]==tagi:
                hiti=hiti+1
                t1=iq[indi]
                t2=ip[indi]
                t3=il[indi]
                t4=ic[indi]
                ip[indi]=il[indi]
                il[indi]=iq[indi]
                iq[indi]=t2
                ifreq[tagi]=ifreq[tagi]+1
            elif il[indi]==tagi:
                hiti=hiti+1
                t1=iq[indi]
                t2=ip[indi]
                t3=il[indi]
                t4=ic[indi]
                il[indi]=iq[indi]
                iq[indi]=t3
                ifreq[tagi]=ifreq[tagi]+1
            elif iq[indi]==tagi:
                hiti=hiti+1
                ifreq[tagi]=ifreq[tagi]+1
            else:
                missi=missi+1
                if ifreq[ic[indi]]>ifreq[ip[indi]]:
                    ifreq[ip[indi]]=0
                    ip[indi]=tagi
                    t1=iq[indi]
                    t2=ip[indi]
                    t3=il[indi]
                    t4=ic[indi]
                    il[indi]=t1
                    ip[indi]=t3
                    ic[indi]=t4
                    iq[indi]=t2
                    ifreq[ic[indi]]=1
                    ifreq[iq[indi]]=1
                else:
                    ic[indi]=tagi
                    ifreq[ic[indi]]=0
                    t1=iq[indi]
                    t2=ip[indi]
                    t3=il[indi]
                    t4=ic[indi]
                    il[indi]=t1
                    ip[indi]=t3
                    ic[indi]=t2
                    iq[indi]=t4
                    ifreq[iq[indi]]=1 
    elif addresses[i][0]==m2 or addresses[i][0]==m3:
        indid=addresses_new[i][17:31]
        tagid=addresses_new[i][0:17]
        if dc[indid]==tagid:
            hitd=hitd+1
            t1=dq[indid]
            t2=dp[indid]
            t3=dl[indid]
            t4=dc[indid]
            dc[indid]=dp[indid]
            dp[indid]=dl[indid]
            dl[indid]=dq[indid]
            dq[indid]=t4
            dfreq[tagid]=dfreq[tagid]+1
        elif dp[indid]==tagid:
            hitd=hitd+1
            t1=dq[indid]
            t2=dp[indid]
            t3=dl[indid]
            t4=dc[indid]
            dp[indid]=dl[indid]
            dl[indid]=dq[indid]
            dq[indid]=t2
            dfreq[tagid]=dfreq[tagid]+1
        elif dl[indid]==tagid:
            hitd=hitd+1
            t1=dq[indid]
            t2=dp[indid]
            t3=dl[indid]
            t4=dc[indid]
            dl[indid]=dq[indid]
            dq[indid]=t3
            dfreq[tagid]=dfreq[tagid]+1
        elif dq[indid]==tagid:
            hitd=hitd+1
            dfreq[tagid]=dfreq[tagid]+1
        else:
            missd=missd+1
            if dfreq[dc[indid]]>dfreq[dp[indid]]:
                dfreq[dp[indid]]=0
                dp[indid]=tagid
                t1=dq[indid]
                t2=dp[indid]
                t3=dl[indid]
                t4=dc[indid]
                dl[indid]=t1
                dp[indid]=t3
                dc[indid]=t2
                dq[indid]=t4 
                dfreq[dc[indid]]=1
                dfreq[dq[indid]]=1
            else:
                dc[indid]=tagid
                t1=dq[indid]
                t2=dp[indid]
                t3=dl[indid]
                t4=dc[indid]
                dl[indid]=t1
                dp[indid]=t3
                dc[indid]=t2
                dq[indid]=t4
                dfreq[dq[indid]]=1
    else:
        print "no raedable address"           
print "number of hits in instruction cache:"                    
print hiti
print "number of misses in instruction cache:"
print missi 
print "number of instruction accesses:"
print k
print "miss rate in instruction cache"
print missi/float(k)
print "number of hits in data cache:"
print hitd
print "number of misses in data cache:"
print missd
print "number of data accesses:"
print kd                                            
print "miss rate in instruction cache"
print missd/float(kd)                