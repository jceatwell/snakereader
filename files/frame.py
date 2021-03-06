# -*- coding: utf8 -*-
"""Module docstring"""

from PIL import Image #musiałem dodać bo mi się nie włącza Lisu
#import math

class Frame :
    """
        Class Frame is a virtual class having all the methods and functions,
        which are needed for
        processing text images in general, no matter if it is a block, line or
        single character. Inheriting classes (BlockFrame, LineFrame and
        CharFrame) use them for teir own purposes.
        """
    
    def __init__(self,f=None,new=False) :
            if new:
                self.matrix=Image.new('1',(1,1))
            else:
                self.matrix=Image.open(f)
            pass
   

    def rotate (self,angle) :
            """Rotates an image by an angle counter clockwise"""
            self.matrix=self.matrix.rotate(angle, expand=True)
            return self
            pass

    def blackWhite (self, quality='ok') :
            """Converts an image to single-band binary image"""
            self.matrix=self.matrix.convert('L')
            if quality=='ok':
                import ImageEnhance
                self.matrix=self.matrix.point(lambda i: i+20)
                self.matrix = ImageEnhance.Contrast(self.matrix)
                self.matrix = self.matrix.enhance(2.5)
                self.matrix=self.matrix.convert('1')   
            if quality=='poor':
                from PIL import ImageFilter #Lisu
                self.matrix = self.matrix.filter(ImageFilter.MinFilter(3))
                self.matrix=self.matrix.convert('1')

    def putPixel (self, x, y) :
            """Method sets the pixel colour to black (for single-band images)"""
            self.matrix.putpixel((x,y),0)

    def makeWhite(self, x, y) :
            """Method sets the pixel colour to white (for single-band images)"""
            self.matrix.putpixel((x,y),255)

    def getPixel (self, x, y) :
            """Method returns integer for single-band images (255:white, 0:black) and n-tuple for n-band images"""
            value = self.matrix.getpixel((x,y))
            return value

    def hLineHistogram (self, number) :
            """Returns the sum of black pixels in the horizontal line of particular number"""
            count=0
            for i in range(self.matrix.size[0]):
                if self.getPixel(i,number)<=128:
                    count+=1
            return count
    def vLineHistogram (self, number) :
            """Returns the sum of black pixels in the vertical line of particular number"""
            count=0
            for i in range(self.matrix.size[1]):
                if self.getPixel(number,i)<=128:
                    count+=1
            return count
            pass
    def vLinesHistogram (self) :
            """Returns the list of results from vLineHistogram (self, number) for all pixel columns"""
            v_histogram=[]
            for number in range(self.matrix.size[0]):
                v_histogram.append(self.vLineHistogram (number))
            return v_histogram
            pass
    def hLinesHistogram (self) :
            """Returns the list of results from vLineHistogram (self, number) for all pixel columns"""
            h_histogram=[]
            for number in range(self.matrix.size[1]):
                h_histogram.append(self.hLineHistogram (number))
            return h_histogram
            pass
    def reScale (self, xSize, ySize) :
            """method docstring"""
            self.matrix=self.matrix.resize((xSize, ySize))
            pass
    
    def clear (self, quality='ok') :
            """Clears single black pixels and makes single white pixels black"""
            pix=self.matrix.load()
            for y in range(self.matrix.size[1]):
                pix[0,y]=255
                pix[self.matrix.size[0]-1,y]=255
            for x in range(1,self.matrix.size[0]-1):
                
                if pix[x,0]<=128 and pix[x+1,0]>128 and pix[x-1,0]>128 and pix[x,1]>128:
                    pix[x,0]=255
                if pix[x,0]>128 and pix[x+1,0]<=128 and pix[x-1,0]<=128 and pix[x,1]<=128:
                    pix[x,0]=0
                    
                for y in range(1,self.matrix.size[1]-1):
                    if quality=='poor':
                        i=0
                        a=0
                        if pix[x,y]<=128:
                            if pix[x+1,y+1]>128: i+=1
                            if pix[x+1,y-1]>128: i+=1
                            if pix[x-1,y+1]>128: i+=1
                            if pix[x-1,y-1]>128: i+=1
                            if pix[x+1,y]>128: i+=1
                            if pix[x-1,y]>128: i+=1
                            if pix[x,y+1]>128: i+=1
                            if pix[x,y-1]>128: i+=1

                            if i>=6: pix[x,y]=255

                        if pix[x,y]>128:
                            if pix[x+1,y+1]<=128: a+=1
                            if pix[x+1,y-1]<=128: a+=1
                            if pix[x-1,y+1]<=128: a+=1
                            if pix[x-1,y-1]<=128:  a+=1
                            
                            if pix[x+1,y]<=128: a+=1
                            if pix[x-1,y]<=128: a+=1
                            if pix[x,y+1]<=128: a+=1
                            if pix[x,y-1]<=128: a+=1
    
                            if a>=6: pix[x,y]=0

                    if quality=='ok':                        
                        if pix[x,y]<=128 and pix[x+1,y]>128 and pix[x-1,y]>128 and pix[x,y+1]>128 and pix[x,y-1]>128:
                            pix[x,y]=255
                        if pix[x,y]>128 and pix[x+1,y]<=128 and pix[x-1,y]<=128 and pix[x,y+1]<=128 and pix[x,y-1]<=128:
                            pix[x,y]=0
                            
                if pix[x,self.matrix.size[1]-1]<=128 and pix[x+1,self.matrix.size[1]-1]>128 and pix[x-1,self.matrix.size[1]-1]>128 and pix[x,self.matrix.size[1]-2]>128:
                    pix[x,self.matrix.size[1]-1]=255
                if pix[x,self.matrix.size[1]-1]>128 and pix[x+1,self.matrix.size[1]-1]<=128 and pix[x-1,self.matrix.size[1]-1]<=128 and pix[x,self.matrix.size[1]-2]<=128:
                    pix[x,self.matrix.size[1]-1]=0
                
            pass
    
    def leftCut(self) :
        """Cuts the image from the left to the beginning of text"""
        l_cutpoint=0
        treshold=0.005*self.matrix.size[1]
        for i in range(self.matrix.size[0]-1):
                if self.vLineHistogram(i) >= treshold:
                    l_cutpoint = i
                    break
        self.matrix=self.matrix.crop((l_cutpoint,0,self.matrix.size[0],self.matrix.size[1]))
        return self
        pass

    def vCut(self):
        """Cuts the sides of the image to the text borders"""
        self.leftCut()
        self.matrix=self.matrix.rotate(180)
        self.leftCut()
        self.matrix=self.matrix.rotate(180)
        return self
        pass
    
    def upperCut (self) :
            """Cuts the image from the upper side to the beginning of text"""
            u_cutpoint=0
            treshold=0.005*self.matrix.size[0]
            for i in range(self.matrix.size[1]-1):
                if self.hLineHistogram(i) >= treshold:
                    u_cutpoint = i
                    break
            self.matrix=self.matrix.crop((0,u_cutpoint,self.matrix.size[0],self.matrix.size[1]))
            return self
            pass
    def hCut(self) :
        """Cuts the image from the upper side to the beginning of text"""
        self.upperCut()
        self.matrix=self.matrix.rotate(180)
        self.upperCut()
        self.matrix=self.matrix.rotate(180)
        return self
        pass
    
    def hLineChangeHistogram (self, number) :
            """method docstring"""
            count=0
            for i in range(self.matrix.size[0]-1):
                if (self.getPixel(i,number)<=128 and self.getPixel(i+1,number)>128) or (self.getPixel(i,number)>128 and self.getPixel(i+1,number)<=128):
                    count+=1
            return count
            pass
    
    def hLinesChangeHistogram (self) :
            """method docstring"""
            h_change_histogram=[]
            for number in range(self.matrix.size[1]):
                h_change_histogram.append(self.hLineChangeHistogram(number))
            return h_change_histogram
            pass
        
    def vLineChangeHistogram (self, number) :
            """method docstring"""
            count=0
            for i in range(self.matrix.size[1]-1):
                if (self.getPixel(number,i)<=128 and self.getPixel(number,i+1)>128) or (self.getPixel(number,i)>128 and self.getPixel(number,i+1)<=128):
                    count+=1
            return count
            pass
    def vLinesChangeHistogram (self) :
            """method docstring"""
            v_change_histogram=[]
            for number in range(self.matrix.size[0]):
                v_change_histogram.append(self.vLineChangeHistogram(number))
            return v_change_histogram
            pass

    def getSize(self):
        return self.matrix.size
        

    

        
##########        test methods            ##########

        
    def showPicture(self) :
            self.matrix.show()
            
    def savePicture(self,filename,format):
            """dodałem ją, gdyż do testów będzie bardzo potrzebna, a jej implementacja nie powinna Ci nastręczyć trudnosci"""
            self.matrix.save(filename,format)
		

if __name__ == "__main__": #this runs, when code is running as an own program, not as a module
	#you can use this section to test your module
    f=open("0.bmp",'rb')
    im=Frame(f)
##    im.blackWhite('poor')
    im.blackWhite()
    
##    print list(im.matrix.getdata())
##    im.clear()
##    im.showPicture()
##    im.clear()
##    im.clear('poor')
####    print im.getSize()
    im=im.hCut()
    im=im.vCut()
####    print im.getSize()
##    im.rotate(45)
##    im.rotate(45)
##    im.blackWhite()
##    print im.vLinesHistogram()
    for i in range(im.matrix.size[1]):
        print im.getPixel(1,i)

##    im.showPicture()
    pass
##    im=Frame(new=True)
##    im.showPicture()
