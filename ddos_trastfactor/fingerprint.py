import random
import hashlib
import time
import uuid

class FingerprintGenerator:
    def __init__(self):
        self.fingerprint_id = str(uuid.uuid4())
        self.created = time.time()
        self.session_id = hashlib.md5(str(random.random()).encode()).hexdigest()
        self._init_dynamic_data()
    
    def _init_dynamic_data(self):
        self.canvas_history = []
        self.webgl_history = []
        self.audio_history = []
        for _ in range(random.randint(5, 15)):
            self.canvas_history.append(self.get_canvas())
            self.webgl_history.append(self.get_webgl())
            self.audio_history.append(self.get_audio())
    
    def get_canvas(self, variant=None):
        variants = ["2d", "webgl", "bitmap", "offscreen"]
        selected = variant or random.choice(variants)
        return {
            "type": selected,
            "hash": hashlib.sha256(str(random.random()).encode()).hexdigest(),
            "winding": random.choice([True, False]),
            "data": "".join(random.choices("0123456789abcdef", k=64)),
            "width": random.choice([300, 500, 800, 1920]),
            "height": random.choice([150, 300, 600, 1080])
        }
    
    def get_webgl(self):
        vendors = ["Intel Inc.", "NVIDIA Corporation", "AMD", "Apple", "Google Inc.", "Qualcomm", "ARM", "Microsoft"]
        renderers = ["ANGLE", "Metal", "OpenGL", "DirectX", "Vulkan", "WebGL"]
        extensions_list = [
            "ANGLE_instanced_arrays", "EXT_blend_minmax", "EXT_color_buffer_half_float",
            "EXT_disjoint_timer_query", "EXT_float_blend", "EXT_frag_depth", "EXT_shader_texture_lod",
            "EXT_texture_compression_bptc", "EXT_texture_compression_rgtc", "EXT_texture_filter_anisotropic",
            "OES_element_index_uint", "OES_fbo_render_mipmap", "OES_standard_derivatives", "OES_texture_float",
            "OES_texture_float_linear", "OES_texture_half_float", "OES_texture_half_float_linear", "OES_vertex_array_object",
            "WEBGL_color_buffer_float", "WEBGL_compressed_texture_s3tc", "WEBGL_compressed_texture_s3tc_srgb",
            "WEBGL_debug_renderer_info", "WEBGL_debug_shaders", "WEBGL_depth_texture", "WEBGL_draw_buffers",
            "WEBGL_lose_context", "WEBGL_multi_draw"
        ]
        return {
            "vendor": random.choice(vendors),
            "renderer": random.choice(renderers),
            "version": f"{random.randint(1,5)}.{random.randint(0,9)}.{random.randint(0,9)}",
            "shading_language": f"WebGL GLSL ES {random.randint(1,3)}.0",
            "max_texture_size": random.choice([4096, 8192, 16384]),
            "max_vertex_attribs": random.randint(8, 16),
            "extensions": random.sample(extensions_list, random.randint(5, 15))
        }
    
    def get_audio(self):
        return {
            "hash": hashlib.md5(str(random.random()).encode()).hexdigest(),
            "sample_rate": random.choice([44100, 48000, 96000]),
            "channel_count": random.choice([1, 2, 6]),
            "fft_size": random.choice([256, 512, 1024, 2048])
        }
    
    def get_fonts(self):
        all_fonts = ["Arial", "Helvetica", "Times New Roman", "Courier New", "Verdana", "Calibri", "Georgia", 
                     "Tahoma", "Trebuchet MS", "Arial Black", "Impact", "Comic Sans MS", "Lucida Console", 
                     "Palatino", "Bookman", "Century Gothic", "Garamond", "Franklin Gothic Medium", 
                     "Segoe UI", "Roboto", "Open Sans", "Lato", "Montserrat", "Source Sans Pro"]
        random.shuffle(all_fonts)
        return all_fonts[:random.randint(15, 25)]
    
    def get_webrtc(self):
        return {
            "local_ip": f"192.168.{random.randint(1,254)}.{random.randint(1,254)}",
            "public_ip": f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,254)}",
            "port": random.randint(49152, 65535),
            "mDNS": f"{uuid.uuid4()}.local",
            "candidates": random.randint(3, 10)
        }
    
    def get_client_rects(self):
        return {
            "screen": f"{random.choice([1920, 1366, 1536, 2560, 3440])}x{random.choice([1080, 768, 864, 1440, 1600])}",
            "available": f"{random.choice([1920, 1366, 1536, 2560])}x{random.choice([1040, 728, 824, 1400])}",
            "color_depth": random.choice([24, 30, 32, 48]),
            "pixel_depth": random.choice([24, 30, 32, 48]),
            "device_pixel_ratio": random.choice([1, 1.25, 1.5, 2, 2.5, 3])
        }
    
    def get_navigator_properties(self):
        return {
            "platform": random.choice(["Win32", "MacIntel", "Linux x86_64", "iPhone", "Android"]),
            "vendor": random.choice(["Google Inc.", "Apple Computer Inc.", "Mozilla", ""]),
            "vendor_sub": "",
            "product": "Gecko",
            "product_sub": random.choice(["20100101", "20030107"]),
            "hardware_concurrency": random.choice([2, 4, 6, 8, 10, 12, 16]),
            "device_memory": random.choice([2, 4, 8, 16, 32, 64]),
            "max_touch_points": random.choice([0, 1, 2, 5, 10]),
            "do_not_track": random.choice(["0", "1", "unspecified"])
        }
    
    def get_permissions(self):
        permissions = ["geolocation", "notifications", "microphone", "camera", "midi"]
        granted = random.sample(permissions, random.randint(1, 3))
        return {p: "granted" for p in granted}
    
    def get_storage_quota(self):
        return {
            "quota": random.randint(1024**3, 10*1024**3),
            "usage": random.randint(0, 1024**3),
            "persistent": random.choice([True, False])
        }
    
    def get_full(self):
        return {
            "id": self.fingerprint_id,
            "session": self.session_id,
            "created": self.created,
            "canvas": self.get_canvas(),
            "canvas_history": random.sample(self.canvas_history, min(3, len(self.canvas_history))),
            "webgl": self.get_webgl(),
            "audio": self.get_audio(),
            "fonts": self.get_fonts(),
            "webrtc": self.get_webrtc(),
            "client_rects": self.get_client_rects(),
            "navigator": self.get_navigator_properties(),
            "permissions": self.get_permissions(),
            "storage": self.get_storage_quota()
        }
    
    def rotate(self):
        self.session_id = hashlib.md5(str(random.random()).encode()).hexdigest()
        self.canvas_history.append(self.get_canvas())
        self.webgl_history.append(self.get_webgl())
        self.audio_history.append(self.get_audio())
        if len(self.canvas_history) > 20:
            self.canvas_history.pop(0)
            self.webgl_history.pop(0)
            self.audio_history.pop(0)
        return self.get_full()
