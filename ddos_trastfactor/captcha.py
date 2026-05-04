import re
import random
import time
import hashlib
import base64

class CaptchaSolver:
    def __init__(self):
        self.solved_count = 0
        self.failed_count = 0
        self.patterns = {
            "recaptcha": re.compile(r'(?:recaptcha|g-recaptcha|data-sitekey)', re.I),
            "hcaptcha": re.compile(r'hcaptcha|data-hcaptcha', re.I),
            "turnstile": re.compile(r'cf-turnstile|turnstile', re.I),
            "simple_math": re.compile(r'(\d+)\s*([+\-/*])\s*(\d+)\s*=\s*\?'),
            "simple_text": re.compile(r'(\d+)\s*:\s*(\w+)|[Вв]ведите [0-9]+|[Cc]aptcha code')
        }
    
    def detect(self, html):
        for captcha_type, pattern in self.patterns.items():
            if pattern.search(html):
                return captcha_type
        return None
    
    async def solve(self, html, page_url=None):
        captcha_type = self.detect(html)
        if not captcha_type:
            return html
        
        if captcha_type == "simple_math":
            solved_html = self._solve_math(html)
            if solved_html != html:
                self.solved_count += 1
                return solved_html
        
        elif captcha_type == "simple_text":
            solved_html = self._solve_text(html)
            if solved_html != html:
                self.solved_count += 1
                return solved_html
        
        self.failed_count += 1
        return html
    
    def _solve_math(self, html):
        match = self.patterns["simple_math"].search(html)
        if not match:
            return html
        
        a, op, b = match.group(1), match.group(2), match.group(3)
        a, b = int(a), int(b)
        
        if op == '+':
            result = a + b
        elif op == '-':
            result = a - b
        elif op == '*':
            result = a * b
        elif op == '/':
            result = a // b if b != 0 else 0
        else:
            return html
        
        answer_str = str(result)
        input_pattern = r'<input[^>]*name=["\']?(?:captcha|answer|result)["\']?[^>]*>'
        
        def replace_input(m):
            tag = m.group(0)
            if 'value=' not in tag:
                tag = tag[:-1] + f' value="{answer_str}">'
            return tag
        
        new_html = re.sub(input_pattern, replace_input, html)
        
        form_pattern = r'<form[^>]*>.*?</form>'
        def add_hidden(m):
            form = m.group(0)
            if 'captcha' in form.lower():
                hidden = f'<input type="hidden" name="captcha_solution" value="{answer_str}">'
                return form.replace('</form>', hidden + '</form>')
            return form
        
        new_html = re.sub(form_pattern, add_hidden, new_html, flags=re.DOTALL)
        
        return new_html if new_html != html else html.replace(match.group(0), f"{a} {op} {b} = {answer_str}")
    
    def _solve_text(self, html):
        text_pattern = r'[Вв]ведите\s+([0-9]+)|([0-9]+)\s*:\s*(\w+)|[Cc]aptcha code:\s*([A-Z0-9]+)'
        match = re.search(text_pattern, html)
        if not match:
            return html
        
        if match.group(1):
            code = match.group(1)
        elif match.group(2) and match.group(3):
            code = match.group(3)
        elif match.group(4):
            code = match.group(4)
        else:
            return html
        
        input_pattern = r'<input[^>]*name=["\']?(?:captcha|code|verification)["\']?[^>]*>'
        
        def replace_input(m):
            tag = m.group(0)
            if 'value=' not in tag:
                tag = tag[:-1] + f' value="{code}">'
            return tag
        
        return re.sub(input_pattern, replace_input, html)
    
    def get_stats(self):
        return {
            "solved": self.solved_count,
            "failed": self.failed_count,
            "success_rate": self.solved_count / max(1, self.solved_count + self.failed_count)
        }
    
    def reset(self):
        self.solved_count = 0
        self.failed_count = 0 
