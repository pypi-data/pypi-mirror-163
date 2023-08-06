from .const import Const, constants as const
from .raster import Raster
from .gridenvelope2d import GridEnvelope2D
import os.path
from math import fabs

__author__ = "Steven B. Hoek"

# Abstract class
class BandRaster(Raster, GridEnvelope2D):
    # Attributes
    _const = None
    
    # Data attributes
    nbands = 3 #default
    nbits = 8  #default
    nodatavalue = 256; #default
    dataformat = "h" # Default data format (2-byte signed short int)
    folder = os.getcwd();

    def __init__(self, filepath, *dataformat):
        # Class and subclass wide constants
        self._const = Const()
        self._const.INTEL = 'I'; # Least significant byte first
        self._const.UNSIGNEDINT = 'UNSIGNEDINT'
        self._const.PIXELTYPE = 'PIXELTYPE'
        self._const.NODATA = 'NODATA'
        
        # Initialise
        Raster.__init__(self, filepath)
        GridEnvelope2D.__init__(self, 1, 1, 0.0, 0.0, 0.1, 0.1)
                        
        # Retrieve the name from the filepath and assign - incl. extension
        self.name = os.path.basename(filepath);
        # Also derive the folder
        self.folder = os.path.dirname(filepath);
        # Finally set the dataformat
        # TODO: get this from the header file?
        if len(dataformat) > 0:
            self.dataformat = dataformat[0]
    
    def open(self, mode, ncols=1, nrows=1, nbands=1, xll=0.0, yll=0.0, cellsize=1.0, nodatavalue=-9999.0):
        super(BandRaster, self).open(mode);
        # If file does not exist and mode[0] = 'w', create it!
        if (mode[0] == 'w'):
            # Set data attributes and write header file anyhow
            self.nbands = nbands;
            self.cellsize = cellsize
            self.nodatavalue = nodatavalue
            
            # If dx and dy have been set to different values already, make sure those are written to disk
            if abs(self.dx - self.dy) < const.epsilon:
                self.envelope = GridEnvelope2D.__init__(self, ncols, nrows, xll, yll, cellsize, cellsize)
            else:
                self.envelope = GridEnvelope2D.__init__(self, ncols, nrows, xll, yll, self.dx, self.dy)
            self.writeheader()
            if not self.file_exists:
                self.datafile = open(os.path.join(self.folder, self.name), 'w')
            else:
                self.datafile = open(os.path.join(self.folder, self.name), mode[0] + 'b') 
            return True
        else:    
            # Open the file
            if self.file_exists:            
                # Open the file and retrieve the data attributes from the header file
                self.datafile = open(os.path.join(self.folder, self.name), mode[0] + 'b'); 
                self.readheader();
                self.xll = self.xul;
                if self.ycoords_sort == const.DESC:
                    self.yll = self.yul - self.nrows * self.dy;
                else:
                    self.yll = self.yul + self.nrows * self.dy;
                self.envelope = GridEnvelope2D.__init__(self, self.ncols, self.nrows, self.xll, self.yll, self.dx, self.dy)
                return True
            else: return False
            
    def readheader(self):
        # See if we can find the header file to use. Then read it and assign all attributes
        hdrFilename = ""
        if os.path.isfile(os.path.join(self.folder, self.name + "." + const.HEADEREXT)): #@UndefinedVariable
            hdrFilename = os.path.join(self.folder, self.name + "." + const.HEADEREXT) #@UndefinedVariable
        else:
            name_wo_ext = os.path.splitext(os.path.join(self.folder, self.name))[0]
            if os.path.isfile(name_wo_ext + "." + const.HEADEREXT ): #@UndefinedVariable
                hdrFilename = os.path.join(name_wo_ext + "." + const.HEADEREXT) #@UndefinedVariable
        if hdrFilename == "":
            raise ValueError("Not sure about name of header file: " + hdrFilename + "?");
        hdrFilename = os.path.normpath(hdrFilename)
        if not os.path.exists(hdrFilename):  
            raise ValueError("Header file not found: " + hdrFilename);
        hf = open(hdrFilename, 'r');     
        if (hf != None):           
            hl = hf.readline();
            self.byteorder = str(hl.replace(const.BYTEORDER, '').strip()); 
            if self.byteorder != self._const.INTEL:
                raise ValueError("Unsupported byte order")
            hl = hf.readline();
            layout = str(hl.replace('LAYOUT', '').strip());
            extuc = self._const.DATAFILEXT.upper() 
            if layout != extuc:
                raise ValueError("Incorrect layout in header - apparently not a " + extuc + " file");
            hl = hf.readline();
            self.nrows = int(hl.replace(const.NROWS.upper(), ''));
            hl = hf.readline();
            self.ncols = int(hl.replace(const.NCOLS.upper(), ''));                
            hl = hf.readline();
            self.nbands = int(hl.replace('NBANDS', ''));
            hl = hf.readline();
            self.nbits = int(hl.replace('NBITS', ''));
            hl = hf.readline();
            bandrowbytes = int(hl.replace('BANDROWBYTES', ''));
            if self.nbits * self.ncols / 8 != bandrowbytes:
                raise ValueError("Incorrect number of bytes per band row in header");
            hl = hf.readline();
            totalrowbytes = int(hl.replace('TOTALROWBYTES', ''));
            if self.nbands * bandrowbytes != totalrowbytes:
                raise ValueError("Incorrect total bytes per row in header");
            hl = hf.readline();
            if hl.find(self._const.PIXELTYPE) != -1:
                # Assume ESRI style header
                self.pixeltype = str(hl.replace(self._const.PIXELTYPE, '').strip());
                hl = hf.readline();
                ulxmap = float(hl.replace('ULXMAP', ''));         
                hl = hf.readline();
                ulymap = float(hl.replace('ULYMAP', ''));        
                hl = hf.readline();
                self.dx = float(hl.replace('XDIM', ''));        
                hl = hf.readline();
                self.dy = float(hl.replace('YDIM', ''));  
                
                # ulxmap - The x-axis map coordinate of the center of the upper left pixel
                # ulymap - The y-axis map coordinate of the center of the upper left pixel
                self.xul = ulxmap - 0.5*self.dx
                self.yul = ulymap + 0.5*self.dy 
                hl = hf.readline();
                if self.dataformat in ['f', 'd']:
                    self.nodatavalue = float(hl.replace(self._const.NODATA, '').strip());
                else:
                    self.nodatavalue = int(hl.replace(self._const.NODATA, '').strip());
                hf.close()
            else:
                # Assume that the rest of the information has to be read from a world file
                name_wo_ext = os.path.splitext(os.path.join(self.folder, self.name))[0]
                if os.path.isfile(name_wo_ext + "." + self.WORLDEXT):
                    # TODO: Adapt the following so that it accounts also for rotated mapsheets
                    sign = lambda x: (1, -1)[x<0];
                    hdrFilename = os.path.normpath(os.path.join(name_wo_ext + "." + self.WORLDEXT))
                    hf = open(hdrFilename, 'r')
                    hl = hf.readline();
                    self.dx = float(hl.strip());
                    hl = hf.readline();
                    self.roty = float(hl.strip());
                    hl = hf.readline();
                    self.rotx = float(hl.strip());
                    eps = 0.0001;
                    if abs(self.rotx)>eps or abs(self.roty)>eps:
                        raise NotImplementedError("Cannot handle rotated mapsheets yet!")
                    hl = hf.readline();            
                    self.dy = fabs(float(hl.strip()));
                    if sign(float(hl.strip())) == 1.0: self.ycoords_sort = 'ASC';
                    hl = hf.readline();
                    self.xul = float(hl.strip()) - 0.5 * self.dx;
                    hl = hf.readline();
                    self.yul = float(hl.strip()) + 0.5 * self.dy;
                    hf.close();
            self.cellsize = (self.dx + self.dy) / 2
        else: 
            msg = "Unable to open header file " + hdrFilename + " in folder " + self.folder;
            raise IOError(msg);

    def writeheader(self):
        # TODO: test!
        # TODO rather use class WorldFile 
        # Write header file with all attributes
        hdrFilename = os.path.join(self.folder, self.name + "." + const.HEADEREXT) #@UndefinedVariable
        hdrFilename = os.path.normpath(hdrFilename)
        try:
            # Open the file if it exists, otherwise create it
            if os.path.exists(hdrFilename):
                hf = open(hdrFilename, 'w');
            else:
                hf = open(hdrFilename, 'w');

            # Now write all the attributes
            hf.write(const.BYTEORDER + "     " + str(self.byteorder) + "\n")
            hf.write("LAYOUT        " + self._const.DATAFILEXT.upper() + "\n")
            hf.write(const.NROWS.upper() + "         " + str(self.nrows) + "\n")
            hf.write(const.NCOLS.upper() + "         " + str(self.ncols) + "\n")
            hf.write("NBANDS        " + str(self.nbands) + "\n")
            hf.write("NBITS         " + str(self.nbits) + "\n") 
            bandrowbytes = int(self.nbits * self.ncols / 8)
            hf.write("BANDROWBYTES  " + str(bandrowbytes) + "\n")
            hf.write("TOTALROWBYTES " + str(self.nbands * bandrowbytes) + "\n")
            if self.dataformat.lower() == 'i':
                if self.dataformat.isupper(): hf.write(self._const.PIXELTYPE + "     UNSIGNEDINT\n") 
                else: hf.write(self._const.PIXELTYPE + "     SIGNEDINT\n")
            else: hf.write(self._const.PIXELTYPE + "     FLOAT\n")
                
            # ulxmap - The x-axis map coordinate of the center of the upper left pixel
            ulxmap = self.xll + 0.5*self.dx
            hf.write("ULXMAP        " + str(ulxmap) + "\n");
            # ulymap - The y-axis map coordinate of the center of the upper left pixel
            ulymap = self.yll + self.nrows*self.dy - 0.5*self.dy # Check this!!!
            hf.write("ULYMAP        " + str(ulymap) + "\n");
            hf.write("XDIM          " + str(self.dx) + "\n");
            hf.write("YDIM          " + str(self.dy) + "\n");
            hf.write(self._const.NODATA + "  " + str(self.nodatavalue) + "\n");
        except Exception as e:
            msg = "Header file " + hdrFilename + " could not be written in folder " + self.folder;
            raise IOError(msg + "(" + str(e) + ")");
        
    def _is_sequence(self, arg):
        return (not hasattr(arg, "strip") and hasattr(arg, "__getitem__") or hasattr(arg, "__iter__"))
    
    def next(self, parseLine=True):
        pass

    def writenext(self, sequence_with_data):
        # input is sequence type - e.g. list, array.array or numpy.array
        pass
    
    @staticmethod
    def getDataFileExt(self):
        return self.DATAFILEXT;
    
    @staticmethod
    def getHeaderFileExt():
        return const.HEADEREXT 
    
    def close(self):
        if self.datafile:
            if not self.datafile.closed:
                self.datafile.close(); 

    def reset(self):
        self.currow = 0; 
        self.datafile.seek(0);
        
    def __exit__(self, exception_type, exception_value, traceback):
        self.close()
        
    def __enter__(self):
        return self
    