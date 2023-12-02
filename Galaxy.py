"""
Starflight: The Lost Colony (Remastered)

ENGINE-LEVEL CODE

Requires Python 3.10
See Engine.py for dependent libraries
"""

from enum import Enum
import xml.etree.ElementTree as et



#region "PLANET CLASS"
"""
---------------------------------------------------------------------
PLANET CLASS
---------------------------------------------------------------------
"""

# planet types
class PlanetType(Enum):
   PT_INVALID = 0
   PT_ASTEROID = 1
   PT_ROCKY = 2
   PT_FROZEN = 3
   PT_OCEANIC = 4
   PT_MOLTEN = 5
   PT_GASGIANT = 6
   PT_ACIDIC = 7
PlanetType = Enum('PlanetType', ['Invalid','Asteroid','Rocky','Frozen','Oceanic','Molten','Gas Giant','Acidic'])


# planet sizes
class PlanetSize(Enum):
   PS_INVALID = 0
   PS_SMALL = 1
   PS_MEDIUM = 2
   PS_LARGE = 3
   PS_HUGE = 4
PlanetSize = Enum('PlanetSize',['Invalid','Small','Medium','Large','Huge'])


# planet temperatures
class PlanetTemperature(Enum):
   PTMP_INVALID = 0
   PTMP_SUBARCTIC = 1
   PTMP_ARCTIC = 2
   PTMP_TEMPERATE = 3
   PTMP_TROPICAL = 4
   PTMP_SEARING = 5
   PTMP_INFERNO = 6
PlanetTemperature = Enum('PlanetTemperature',['Invalid','Subarctic','Arctic','Temperate','Tropical','Searing','Inferno'])


# planet gravity
class PlanetGravity(Enum):
   PG_INVALID = 0
   PG_NEGLIGIBLE = 1
   PG_VERYLOW = 2
   PG_LOW = 3
   PG_OPTIMAL = 4
   PG_VERYHEAVY = 5
   PG_CRUSHING = 6
PlanetGravity = Enum('PlanetGravity',['Invalid','Negligible','Very Low','Low','Optimal','Very Heavy','Crushing'])


# planet atmosphere
class PlanetAtmosphere(Enum):
   PA_INVALID = 0
   PA_NONE = 1
   PA_TRACEGASES = 2
   PA_BREATHABLE = 3
   PA_ACIDIC = 4
   PA_TOXIC = 5
   PA_FIRESTORM = 6
PlanetAtmosphere = Enum('PlanetAtmosphere',['Invalid','None','Trace Gases','Breathable','Acidic','Toxic','Firestorm'])


# planet weather
class PlanetWeather(Enum):
   PW_INVALID = 0
   PW_NONE = 1
   PW_CALM = 2
   PW_MODERATE = 3
   PW_VIOLENT = 4
   PW_VERYVIOLENT = 5
PlanetWeather = Enum('PlanetWeather',['Invalid','None','Calm','Moderate','Violent','Very Violent'])


# a planet within a star system
class Planet:

    def __init__(self):
        self.id:int = -1
        self.hostStarID:int = -1
        self.name:str = ""
        self.size:PlanetSize = PlanetSize.PS_INVALID
        self.type:PlanetType = PlanetType.PT_INVALID
        self.color:str = ""
        self.temperature:PlanetTemperature = PlanetTemperature.PTMP_INVALID
        self.gravity:PlanetGravity = PlanetGravity.PG_INVALID
        self.atmosphere:PlanetAtmosphere = PlanetAtmosphere.PA_INVALID
        self.weather:PlanetWeather = PlanetWeather.PW_INVALID
        self.landable:bool = False 


    def copy(self, other):
        self.id = other.id
        self.hostStarID = other.hostStarID
        self.name = other.name
        self.size = other.size
        self.type = other.type
        self.color = other.color
        self.temperature = other.temperature
        self.gravity = other.gravity
        self.atmosphere = other.atmosphere
        self.weather = other.weather
        self.landable = other.landable


    def PlanetSizeFromString(self, size:str)->PlanetSize:
        result:PlanetSize = PlanetSize.PS_INVALID
        match size.upper():
            case "SMALL": result = PlanetSize.PS_SMALL
            case "MEDIUM": result = PlanetSize.PS_MEDIUM
            case "LARGE": result = PlanetSize.PS_LARGE
            case "HUGE": result = PlanetSize.PS_HUGE
            case _: result = PlanetSize.PS_INVALID
        return result

    def PlanetSizeToString(self, size:PlanetSize)->str:
        result:str = ""
        match size:
            case PlanetSize.PS_SMALL: result = "SMALL"
            case PlanetSize.PS_MEDIUM: result = "MEDIUM"
            case PlanetSize.PS_LARGE: result = "LARGE"
            case PlanetSize.PS_HUGE: result = "HUGE"
            case _: result = "INVALID"
        return result

    def PlanetTypeFromString(self, type:str)->PlanetType:
        result:PlanetType = PlanetType.PT_INVALID
        match type.upper():
            case "ASTEROID": result = PlanetType.PT_ASTEROID
            case "ROCKY": result = PlanetType.PT_ROCKY
            case "FROZEN": result = PlanetType.PT_FROZEN
            case "OCEANIC": result = PlanetType.PT_OCEANIC
            case "MOLTEN": result = PlanetType.PT_MOLTEN
            case "GAS GIANT": result = PlanetType.PT_GASGIANT
            case "GASGIANT": result = PlanetType.PT_GASGIANT
            case "ACIDIC": result = PlanetType.PT_ACIDIC
            case _: result = PlanetType.PT_INVALID
        return result

    def PlanetTypeToString(self, type:PlanetType)->str:
        result:str = ""
        match type:
            case PlanetType.PT_ASTEROID: result = "ASTEROID"
            case PlanetType.PT_ROCKY: result = "ROCKY"
            case PlanetType.PT_FROZEN: result = "FROZEN"
            case PlanetType.PT_OCEANIC: result = "OCEANIC"
            case PlanetType.PT_MOLTEN: result = "MOLTEN"
            case PlanetType.PT_GASGIANT: result = "GAS GIANT"
            case PlanetType.PT_ACIDIC: result = "ACIDIC"
            case _: result = "INVALID"
        return result


    def PlanetTemperatureFromString(self, temperature:str)->PlanetTemperature:
        result:PlanetTemperature = PlanetTemperature.PTMP_INVALID
        match temperature:
            case "SUBARCTIC": result = PlanetTemperature.PTMP_SUBARCTIC
            case "SUB-ARCTIC": result = PlanetTemperature.PTMP_SUBARCTIC
            case "ARCTIC": result = PlanetTemperature.PTMP_ARCTIC
            case "TEMPERATE": result = PlanetTemperature.PTMP_TEMPERATE
            case "TROPICAL": result = PlanetTemperature.PTMP_TROPICAL
            case "SEARING": result = PlanetTemperature.PTMP_SEARING
            case "INFERNO": result = PlanetTemperature.PTMP_INFERNO
            case _: result = PlanetTemperature.PTMP_INVALID
        return result


    def PlanetTemperatureToString(self, temperature:PlanetTemperature)->str:
        result:str = ""
        match temperature:
            case PlanetTemperature.PTMP_SUBARCTIC: result = "SUBARCTIC"
            case PlanetTemperature.PTMP_ARCTIC: result = "ARCTIC"
            case PlanetTemperature.PTMP_TEMPERATE: result = "TEMPERATE"
            case PlanetTemperature.PTMP_TROPICAL: result = "TROPICAL"
            case PlanetTemperature.PTMP_SEARING: result = "SEARING"
            case PlanetTemperature.PTMP_INFERNO: result = "INFERNO"
            case _: result = "INVALID";

        return result


    def PlanetGravityFromString(self, gravity:str)->PlanetGravity:
        result:PlanetGravity = PlanetGravity.PG_INVALID
        match gravity:
            case "NEGLIGIBLE": result = PlanetGravity.PG_NEGLIGIBLE
            case "VERY LOW": result = PlanetGravity.PG_VERYLOW
            case "LOW": result = PlanetGravity.PG_LOW
            case "OPTIMAL": result = PlanetGravity.PG_OPTIMAL
            case "VERY HEAVY": result = PlanetGravity.PG_VERYHEAVY
            case "VERYHEAVY": result = PlanetGravity.PG_VERYHEAVY
            case "CRUSHING": result = PlanetGravity.PG_CRUSHING
            case _: result = PlanetGravity.PG_INVALID
        return result


    def PlanetGravityToString(self, gravity:PlanetGravity)->str:
        result:str = ""
        match gravity:
            case PlanetGravity.PG_NEGLIGIBLE: result = "NEGLIGIBLE";
            case PlanetGravity.PG_VERYLOW: result = "VERY LOW";
            case PlanetGravity.PG_LOW: result = "LOW";
            case PlanetGravity.PG_OPTIMAL: result = "OPTIMAL";
            case PlanetGravity.PG_VERYHEAVY: result = "VERY HEAVY";
            case PlanetGravity.PG_CRUSHING: result = "CRUSHING";
            case _: result = "INVALID";
        return result


    def PlanetAtmosphereFromString(self, atmosphere:str)->PlanetAtmosphere:
        result:PlanetAtmosphere = PlanetAtmosphere.PA_INVALID
        match atmosphere:
            case "NONE": result = PlanetAtmosphere.PA_NONE
            case "TRACEGASES": result = PlanetAtmosphere.PA_TRACEGASES
            case "TRACE GASES": result = PlanetAtmosphere.PA_TRACEGASES
            case "BREATHABLE": result = PlanetAtmosphere.PA_BREATHABLE
            case "ACIDIC": result = PlanetAtmosphere.PA_ACIDIC
            case "TOXIC": result = PlanetAtmosphere.PA_TOXIC
            case "FIRESTORM": result = PlanetAtmosphere.PA_FIRESTORM
            case _: result = PlanetAtmosphere.PA_INVALID
        return result


    def PlanetAtmosphereToString(self, atmosphere:PlanetAtmosphere)->str:
        result:str = ""
        match atmosphere:
            case PlanetAtmosphere.PA_NONE: result = "NONE"
            case PlanetAtmosphere.PA_TRACEGASES: result = "TRACEGASES"
            case PlanetAtmosphere.PA_BREATHABLE: result = "BREATHABLE"
            case PlanetAtmosphere.PA_ACIDIC: result = "ACIDIC"
            case PlanetAtmosphere.PA_TOXIC: result = "TOXIC"
            case PlanetAtmosphere.PA_FIRESTORM: result = "FIRESTORM"
            case _: result = "INVALID"
        return result


    def PlanetWeatherFromStngri(self, weather:str)->PlanetWeather:
        result:PlanetWeather = PlanetWeather.PW_INVALID
        match weather:
            case "NONE": result = PlanetWeather.PW_NONE
            case "CALM": result = PlanetWeather.PW_CALM
            case "MODERATE": result = PlanetWeather.PW_MODERATE
            case "VIOLENT": result = PlanetWeather.PW_VIOLENT
            case "VERYVIOLENT": result = PlanetWeather.PW_VERYVIOLENT
            case "VERY VIOLENT": result = PlanetWeather.PW_VERYVIOLENT
        return result


    def PlanetWeatherToString(self, weather:PlanetWeather)->str:
        result:str = ""
        match weather:
            case PlanetWeather.PW_NONE: result = "NONE"
            case PlanetWeather.PW_CALM: result = "CALM"
            case PlanetWeather.PW_MODERATE: result = "MODERATE"
            case PlanetWeather.PW_VIOLENT: result = "VIOLENT"
            case PlanetWeather.PW_VERYVIOLENT: result = "VERY VIOLENT"
            case _: result = "INVALID"
        return result

#endregion


# spectral classes
class SpectralClass(Enum):
    INVALID = 0
    M = 1
    K = 2
    G = 3
    F = 4
    A = 5
    B = 6
    O = 7
SpectralClass = Enum('SpectralClass',['INVALID','M','K','G','F','A','B','O'])

def SpectralIndex(sc:str):
    ret = 0
    match sc:
        case 'M': ret = 1
        case 'K': ret = 2
        case 'G': ret = 3
        case 'F': ret = 4
        case 'A': ret = 5
        case 'B': ret = 6
        case 'O': ret = 7
    return ret 


#region "STAR CLASS"
"""
---------------------------------------------------------------------
STAR CLASS
---------------------------------------------------------------------
"""

class Star:

    def __init__(self):
        self.id = -1
        self.name:str = ""
        self.x:int = 0
        self.y:int = 0
        self.spectralClass:str = ""
        self.color:str = ""
        self.temperature:int = 0
        self.mass:float = 1.0
        self.radius:float = 1.0
        self.luminosity:float = 1.0
        #this array should be filled once and not manipulated
        self.maxPlanets = 20
        self.totalPlanets = 0
        self.planets = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] #max 20 planet IDs

    def __str__(self)->str:
        s = str(self.id) + ","
        s+= str(self.name) + ","
        s+= str(self.x) + "," + str(self.y) + ","
        s+= str(self.spectralClass) + ","
        s+= str(self.color) + ","
        s+= str(self.temperature) + ","
        s+= str(self.mass) + ","
        s+= str(self.radius) + ","
        s+= str(self.luminosity)
        return s 


    def copy(self,other):
        self.id = other.id
        self.name = other.name 
        self.x = other.x 
        self.y = other.y 
        self.spectralClass = other.spectralClass
        self.color = other.color 
        self.temperature = other.temperature
        self.mass = other.mass
        self.radius = other.radius
        self.luminosity = other.luminosity


    def get_color(self):
        color = (255,255,255)
        match self.spectralClass:
            case 'M': color=(255,255,255)
            case 'K': color=(165,255,255)
            case 'G': color=(255,255,100)
            case 'F': color=(255,160,20)
            case 'A': color=(190,90,220)
            case 'B': color=(255,64,64)
            case 'O': color=(10,40,255)
        return color 
    

    def get_num_planets(self)->int:
        return self.totalPlanets



class Galaxy:
    
    def __init__(self):
        self.totalstars = 0
        self.totalplanets = 0

        self.stars = []
        self.planets = []

    def GetTotalStars(self)->int:
        return len(self.stars)

    def GetTotalPlanets(self)->int:
        return self.totalplanets #len(self.planets)

    def Load(self,filename:str)->bool:

        tree = et.parse(filename)
        if tree==None:
            return False 
            
        root = tree.getroot()
        if root.tag != "galaxy":
            return False
        
        self.totalstars = 0
        for child in root.findall("star"):
            self.totalstars += 1
            star = Star()
            star.id = int(child.find("id").text)
            star.name = child.find("name").text
            star.x = int(child.find("x").text)
            star.y = int(child.find("y").text)
            star.spectralClass = child.find("spectralclass").text
            star.color = child.find("color").text
            star.temperature = child.find("temperature").text 
            star.mass = float(child.find("mass").text)
            star.radius = float(child.find("radius").text)
            star.luminosity = float(child.find("luminosity").text)
            self.stars.append(star)
            #print(str(star))

        self.totalplanets = 0
        for child in root.findall("planet"):
            self.totalplanets += 1
            
        
        return True 

#endregion
