import framebuf

class SH1106(framebuf.FrameBuffer):
    def __init__(self, i2c, width=128, height=64, addr=0x3C):
        self.width = width
        self.height = height
        self.pages = height // 8
        self.buffer = bytearray(self.pages * self.width)
        self.i2c = i2c
        self.addr = addr
        super().__init__(self.buffer, self.width, self.height, framebuf.MONO_VLSB)
        self.init_display()

    def init_display(self):
        # Initialization sequence for SH1106 OLED display
        init_cmds = [
            0xAE,         # Display OFF
            0xD5, 0x80,   # Set display clock divide ratio/oscillator frequency
            0xA8, 0x3F,   # Set multiplex ratio (1 to 64)
            0xD3, 0x00,   # Set display offset
            0x40,         # Set start line address
            0xAD, 0x8B,   # Set DC-DC control mode
            0xA1,         # Set segment re-map
            0xC8,         # Set COM Output Scan Direction
            0xDA, 0x12,   # Set COM pins hardware configuration
            0x81, 0x80,   # Set contrast control
            0xD9, 0xF1,   # Set pre-charge period
            0xDB, 0x40,   # Set VCOMH deselect level
            0xA4,         # Entire display ON
            0xA6,         # Set normal display
            0xAF          # Display ON
        ]
        for cmd in init_cmds:
            self.write_cmd(cmd)
        self.fill(0)
        self.show()

    def write_cmd(self, cmd):
        # Send a command to the display
        self.i2c.writeto(self.addr, bytearray([0x80, cmd]))

    def show(self):
        # Refresh the display with current buffer content
        for page in range(0, self.height // 8):
            self.write_cmd(0xB0 + page)
            self.write_cmd(0x02)
            self.write_cmd(0x10)
            self.i2c.writeto(self.addr, bytearray([0x40]) + self.buffer[page * self.width:(page + 1) * self.width])
