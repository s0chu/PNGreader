import chunks

def print_pixel(R , G , B , alpha):
    proc = (100 * alpha) / 255
    proc = float(f"{proc:.2f}")

    if 0 <= proc and proc < 25: 
        char = "\u2591"
    if 25 <= proc and proc < 50:
        char = "\u2592"
    if 50 <= proc and proc < 75:
        char = "\u2593"
    if 75 <= proc and proc <= 100:
        char = " "
    
    color = "\x1b[48;2;" + str(R) + ";" + str(G) + ";" + str(B) + "m"
    text = "\x1b[38;2;" + str(R) + ";" + str(G) + ";" + str(B) + "m"
    hex_color = "#" + f"{R:02x}" + f"{G:02x}" + f"{B:02x}"
    reset = "\x1b[m"

    if proc < 10:
        blanks = "  "
    elif proc < 100:
        blanks = " "
    else:
        blanks = ""

    proc_string = blanks + f"{proc:0.2f}"
    print(color + char * 3 + reset + "  " + text + hex_color + reset + "  " + proc_string + "%")

class Pixel_0: #bit_depth = 1 , 2 , 4 , 8 , 16
    def __init__(this , bit_depth , read):
        this.grayscale = read(bit_depth)
        
    def print(this):
        print_pixel(this.grayscale & 0xFF , this.grayscale & 0xFF , this.grayscale & 0xFF , 255)

    def __eq__(this , b):
        return this.grayscale == b.grayscale
    
    def __hash__(this):
        return this.grayscale
    
class Pixel_2: #bit_depth = 8 16
    def __init__(this , bit_depth , read):
        this.R = read(bit_depth)
        this.G = read(bit_depth)
        this.B = read(bit_depth)
    
    def print(this): 
        print_pixel(this.R & 0xFF , this.G & 0xFF , this.B & 0xFF , 255)

    def __eq__(this , b):
        return this.R == b.R and this.G == b.G and this.B == b.B
    
    def __hash__(this):
        return (this.R << 32) + (this.G << 16) + this.B
    
class Pixel_3: #bit_depth = 1 2 4 8
    def __init__(this , bit_depth , read):
        index = read(bit_depth)
        this.pixel = chunks.plte[0].palette[index]
    
    def print(this):
        this.pixel.print()

    def __eq__(this , b):
        return this.pixel == b.pixel
    
    def __hash__(this):
        return hash(this.pixel)
        
class Pixel_4: #bit_depth = 8 16
    def __init__(this , bit_depth , read):
        this.grayscale = read(bit_depth)
        this.alpha =     read(bit_depth)
        
    def print(this):
        print_pixel(this.grayscale & 0xFF , this.grayscale & 0xFF , this.grayscale & 0xFF , this.alpha)

    def __eq__(this , b):
        return this.grayscale == b.grayscale and this.alpha == b.alpha
    
    def __eq__(this):
        return (this.grayscale << 16) + this.alpha
    
class Pixel_6: #bit_depth = 8 16
    def __init__(this , bit_depth , read):
        this.R =     read(bit_depth)
        this.G =     read(bit_depth)
        this.B =     read(bit_depth)
        this.alpha = read(bit_depth)
    
    def print(this):
        print_pixel(this.R & 0xFF , this.G & 0xFF , this.B & 0xFF , this.alpha)

    def __eq__(this , b):
        return this.R == b.R and this.G == b.G and this.B == b.B and this.alpha == b.alpha

    def __hash__(this):
        return (this.R << 48) + (this.G << 32) + (this.B << 16) + this.alpha
    

pixel_type = {0 : Pixel_0 , 2 : Pixel_2 , 3 : Pixel_3 , 4 : Pixel_4 , 6 : Pixel_6}
