import time
class BrowserHistory:
    def __init__(self, max_size=1000):
        self.history = []
        self.max_size = max_size
        self.visits_count = {}
    
    def add(self, url, status, response_time=0):
        self.history.insert(0, {
            "url": url,
            "status": status,
            "response_time": response_time,
            "time": time.time()
        })
        self.visits_count[url] = self.visits_count.get(url, 0) + 1
        if len(self.history) > self.max_size:
            removed = self.history.pop()
            del self.visits_count[removed["url"]]
    
    def get_visited(self):
        return [h["url"] for h in self.history]
    
    def get_most_visited(self, limit=10):
        sorted_items = sorted(self.visits_count.items(), key=lambda x: x[1], reverse=True)
        return sorted_items[:limit]
    
    def get_stats(self):
        if not self.history:
            return {}
        success = sum(1 for h in self.history if 200 <= h["status"] < 300)
        total = len(self.history)
        return {
            "total": total,
            "success": success,
            "success_rate": success / total if total > 0 else 0,
            "unique_domains": len(set(h["url"].split("//")[1].split("/")[0] for h in self.history if "//" in h["url"]))
        }
