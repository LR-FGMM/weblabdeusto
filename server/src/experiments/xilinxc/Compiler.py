
import subprocess


class Compiler(object):
    
    BASE_PATH = "C:/pfc/PruebaWL"
    
    def __init__(self):
        pass
    
    def synthesize(self):
        process = subprocess.Popen(["xst", "-intstyle", "ise", "-ifn", "Untitled.xst", 
                                    "-ofn", "Untitled.syr"], 
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                   cwd = self.BASE_PATH)
        
        so, se = process.communicate()
        
        if len(se) > 0 or "ERROR:" in so:
            return False
        
        return True
    
    def ngdbuild(self):
        process = subprocess.Popen(["ngdbuild", "-intstyle", "ise", "-dd", "_ngo", "-nt", "timestamp", "-uc", "C:/Users/lrg/Downloads/PINES_FPGA_2012_2013_def (1).ucf", 
                                    "-p", "xc3s1000-ft256-4", "Untitled.ngc", "Untitled.ngd"],
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                   cwd = self.BASE_PATH)

        so, se = process.communicate()

        if len(se) == 0 and "NGDBUILD done." in so:
            return True
        
        return False
    
    def map(self):
        process = subprocess.Popen(["map", "-intstyle", "ise", "-p", "xc3s1000-ft256-4", 
                                    "-cm", "area", "-ir", "off", "-pr", "off", "-c", "100", 
                                    "-o", "Untitled_map.ncd", "Untitled.ngd", "Untitled.pcf"],
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                   cwd = self.BASE_PATH)
        
        so, se = process.communicate()
        
        if len(se) == 0 and "Mapping completed." in so:
            return True
        
        return False;
        
    def par(self):
        process = subprocess.Popen(["par", "-w", "-intstyle", "ise", "-ol", "high", "-t", "1",
                                    "Untitled_map.ncd", "Untitled.ncd", "Untitled.pcf"],
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                   cwd = self.BASE_PATH)
        
        so, se = process.communicate()
        
        if len(se) == 0 and "PAR done!" in so:
            return True
        
        return False
    
    def implement(self):
        result = self.ngdbuild()
        if(result):
            result = self.map()
            if(result):
                result = self.par()
                return result
        return False
    
    def generate(self):
        process = subprocess.Popen(["bitgen", "-intstyle", "ise", "-f", "Untitled.ut", 
                                    "Untitled.ncd"],
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                   cwd = self.BASE_PATH)
        
        # We use process.wait rather than process.communicate because
        # when bitgen is executed, WebTalk stays running in the background,
        # which causes an error. And there seems to be no way to disable it.
        
        r = process.wait()
        
        if(r == 0):
            return True
        
        return False
        

c = Compiler()

print c.synthesize()
print c.implement()
print c.generate()

print "Good bye"