import random
import time
import asyncio

class BehaviorSimulator:
    def __init__(self):
        self.action_history = []
        self.mouse_movements = []
        self.key_presses = []
    
    async def before_request(self):
        delay = random.uniform(0.05, 0.5)
        await asyncio.sleep(delay)
        
        if random.random() > 0.9:
            mouse_move = self._simulate_mouse()
            self.mouse_movements.append(mouse_move)
        
        if random.random() > 0.8:
            key_press = self._simulate_keyboard()
            self.key_presses.append(key_press)
        
        self.action_history.append({"time": time.time(), "type": "before_request"})
    
    async def after_request(self, response_time):
        delay = random.uniform(0.1, 1.5) * min(1, response_time / 10)
        await asyncio.sleep(delay)
        self.action_history.append({"time": time.time(), "type": "after_request"})
    
    def _simulate_mouse(self):
        return {
            "x": random.randint(0, 1920),
            "y": random.randint(0, 1080),
            "type": random.choice(["click", "move", "scroll"]),
            "time": time.time()
        }
    
    def _simulate_keyboard(self):
        return {
            "key": random.choice(["ArrowDown", "ArrowUp", "Enter", "Escape", "Tab"]),
            "time": time.time()
        }
