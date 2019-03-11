import pickle

fp = open("shareddata.pkl",'rb')
print('2')
value = pickle.load(fp)
print('3')
available = int(value['available'])
print('4')
print(available)
print(type(available))
