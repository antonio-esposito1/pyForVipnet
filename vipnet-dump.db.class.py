from pyForVipnet import XR_VPE
import shelve
db = shelve.open('devicedb-20240701-132543')
print(len(db))
print(list(db.keys()))
for key in db:
    print(key, '=>', db[key])
    
fieldnames =('devicename', 'bgp_vpnv4_unicast_neighbors', 'isis_neighbors' )
    
while True:
    key = input('\nkey? => ')
    #subkey = input('\nsubkey? => ')
    if not key: break
    try:
        record = db[key]
    except:
        print('No such key "%s"!' % key)
    else:
        print(record)
        for field in fieldnames:
            print(field, '=> ', getattr(record, field))
        #print(db[key].isis_neighbors)
        #print(db[key].bgp_vpnv4_unicast_neighbors)
        
    