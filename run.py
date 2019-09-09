from helpers import Helpers
import string
import syft as sy
import torch as th
hook = sy.TorchHook(th)

class EncryptedDB():

    def __init__(self, *owners, max_key_len=8, max_val_len=8):
        self.helpers = Helpers()
        self.max_key_len = max_key_len
        self.max_val_len = max_val_len

        self.keys = list()
        self.values = list()
        self.owners = owners

    def add_entry(self, key, value):
        key = self.helpers.string2one_hot_matrix(key)
        key = key.share(*self.owners)
        self.keys.append(key)

        value = self.helpers.string2values(value, max_len=self.max_val_len)
        value = value.share(*self.owners)
        self.values.append(value)

    def query(self, query_str):
        query_matrix = self.helpers.string2one_hot_matrix(query_str)

        query_matrix = query_matrix.share(*self.owners)

        key_matches = list()
        for key in self.keys:

            key_match = self.helpers.strings_equal(key, query_matrix)
            key_matches.append(key_match)

        result = self.values[0] * key_matches[0]
        for i in range(len(self.values) - 1):
            result += self.values[i + 1] * key_matches[i + 1]

        result = result.get()
        return self.helpers.values2string(result).replace(".","")

bob = sy.VirtualWorker(hook, id="bob").add_worker(sy.local_worker)
alice = sy.VirtualWorker(hook, id="alice").add_worker(sy.local_worker)
secure_worker = sy.VirtualWorker(hook, id="secure_worker").add_worker(sy.local_worker)

db = EncryptedDB(bob, alice, secure_worker, max_val_len=256)

db.add_entry("Bob","(123) 456 7890")
db.add_entry("Bill", "(234) 567 8901")
db.add_entry("Sam","(345) 678 9012")
db.add_entry("Key","really big json value")

print(db.query("Bob"))
