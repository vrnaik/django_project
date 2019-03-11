import time, json, pickle

# shared = {"Foo":"Bar", "Parrot":"Dead"}
# fp = open("shared.pkl","w")
# pickle.dump(shared, fp)


try:
    while True:
        with open('/home/vikas/Desktop/Desk/AvailableResource.json') as f:
            data = json.load(f)
            f.close()
        # print(data)
        # print(type(data))
        val = data['available']
        print(val)
        print(type(val))
        # inti = int(val)
        # print(inti)
        # print(type(inti))

        fp = open("shareddata.pkl","wb")
        pickle.dump(data, fp)
        time.sleep(1)  # 1s

except KeyboardInterrupt:
    print("checking stopped")

#
# one.py
#
# import pickle
#
# shared = {"Foo":"Bar", "Parrot":"Dead"}
# fp = open("shared.pkl","w")
# pickle.dump(shared, fp)
#
#
# two.py
#
# import pickle
#
# fp = open("shared.pkl")
# shared = pickle.load(fp)
# print shared["Foo"]
