import time
import random
import math

class TrustFactor:
    def __init__(self, level="medium"):
        self.level = level
        self.score = 50
        self.history = []
        self.request_times = []
        self.success_rate = 1.0
        self.captcha_solves = 0
        self.unique_domains = set()
        self.session_start = time.time()
        self._init_level()
    
    def _init_level(self):
        levels = {
            "low": 30,
            "medium": 50,
            "high": 70,
            "max": 85
        }
        self.score = levels.get(self.level, 50)
    
    def record_request(self, status_code, response_time=None):
        success = 200 <= status_code < 300
        self.history.append({
            "time": time.time(),
            "success": success,
            "status": status_code,
            "response_time": response_time
        })
        if response_time:
            self.request_times.append(response_time)
        if len(self.history) > 1000:
            self.history.pop(0)
        if len(self.request_times) > 500:
            self.request_times.pop(0)
        self._update_score(success)
    
    def _update_score(self, success):
        if success:
            self.score = min(100, self.score + 0.5)
        else:
            self.score = max(0, self.score - 0.3)
        
        age_factor = min(30, (time.time() - self.session_start) / 3600)
        self.score += age_factor * 0.1
        self.score = min(100, max(0, self.score))
    
    def record_captcha_solve(self, solved):
        if solved:
            self.captcha_solves += 1
            self.score = min(100, self.score + 2)
        else:
            self.score = max(0, self.score - 5)
    
    def record_domain(self, domain):
        self.unique_domains.add(domain)
        if len(self.unique_domains) > 10:
            self.score = min(100, self.score + 5)
    
    def get_score(self):
        score = self.score
        if self.request_times:
            avg_time = sum(self.request_times) / len(self.request_times)
            if avg_time < 0.5:
                score -= 10
            elif avg_time > 5:
                score += 5
        
        recent_success = 0
        for h in self.history[-50:]:
            if h["success"]:
                recent_success += 1
        recent_rate = recent_success / max(1, len(self.history[-50:]))
        score += (recent_rate - 0.5) * 20
        
        return int(min(100, max(0, score)))
    
    def get_recommendation(self):
        score = self.get_score()
        if score < 30:
            return "aggressive"
        elif score < 60:
            return "normal"
        else:
            return "stealth"
    
    def is_trusted(self):
        return self.get_score() > 50
    
    def get_stats(self):
        return {
            "current_score": self.get_score(),
            "total_requests": len(self.history),
            "success_rate": sum(1 for h in self.history if h["success"]) / max(1, len(self.history)),
            "captcha_solves": self.captcha_solves,
            "unique_domains": len(self.unique_domains),
            "session_duration": time.time() - self.session_start,
            "level": self.level
        }
    
    def reset(self):
        self.score = 50
        self.history = []
        self.request_times = []
        self.captcha_solves = 0
        self.unique_domains = set()
        self.session_start = time.time()
