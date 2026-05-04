import json
import time
import random

class LocalStorage:
    def __init__(self, path="storage.json"):
        self.path = path
        self.data = self._load()
    
    def _load(self):
        try:
            with open(self.path, 'r') as f:
                return json.load(f)
        except:
            return {}
    
    def _save(self):
        with open(self.path, 'w') as f:
            json.dump(self.data, f)
    
    def set(self, key, value, domain="global"):
        if domain not in self.data:
            self.data[domain] = {}
        self.data[domain][key] = value
        self._save()
    
    def get(self, key, domain="global"):
        return self.data.get(domain, {}).get(key)
    
    def delete(self, key, domain="global"):
        if domain in self.data and key in self.data[domain]:
            del self.data[domain][key]
            self._save()
    
    def clear_domain(self, domain):
        if domain in self.data:
            del self.data[domain]
            self._save()
    
    def get_all(self):
        return self.data
