import chunks

class Pixel_0:
    def __init__(this , bit_depth , read):
        this.grayscale = read(bit_depth)
        
    def print(this):
        print(f"grayscale: {this.grayscale}")

    def __eq__(this , b):
        return this.grayscale == b.grayscale
    
    def __hash__(this):
        return this.grayscale
    
class Pixel_2:
    def __init__(this , bit_depth , read):
        this.R = read(bit_depth)
        this.G = read(bit_depth)
        this.B = read(bit_depth)
    
    def print(this): 
        print(f"R: {this.R} G: {this.G} B: {this.B}")

    def __eq__(this , b):
        return this.R == b.R and this.G == b.G and this.B == b.B
    
    def __hash__(this):
        return (this.R << 32) + (this.G << 16) + this.B
    
class Pixel_3:
    def __init__(this , bit_depth , read):
        index = read(bit_depth)
        this.pixel = chunks.plte[0].palette[index]
    
    def print(this):
        this.pixel.print()

    def __eq__(this , b):
        return this.pixel == b.pixel
    
    def __hash__(this):
        return hash(this.pixel)
        
class Pixel_4:
    def __init__(this , bit_depth , read):
        this.grayscale = read(bit_depth)
        this.alpha =     read(bit_depth)
        
    def print(this):
        print(f"grayscale: {this.grayscale} alpha: {this.alpha}")

    def __eq__(this , b):
        return this.grayscale == b.grayscale and this.alpha == b.alpha
    
    def __eq__(this):
        return (this.grayscale << 16) + this.alpha
    
class Pixel_6:
    def __init__(this , bit_depth , read):
        this.R =     read(bit_depth)
        this.G =     read(bit_depth)
        this.B =     read(bit_depth)
        this.alpha = read(bit_depth)
    
    def print(this):
        print(f"R: {this.R} G: {this.G} B: {this.B} alpha: {this.alpha}")

    def __eq__(this , b):
        return this.R == b.R and this.G == b.G and this.B == b.B and this.alpha == b.alpha

    def __hash__(this):
        return (this.R << 48) + (this.G << 32) + (this.B << 16) + this.alpha
    

pixel_type = {0 : Pixel_0 , 2 : Pixel_2 , 3 : Pixel_3 , 4 : Pixel_4 , 6 : Pixel_6}
