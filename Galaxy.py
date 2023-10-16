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


#region "STAR CLASS"
"""
---------------------------------------------------------------------
STAR CLASS
---------------------------------------------------------------------
"""

# spectral classes
class SpectralClass(Enum):
    SC_INVALID = 0
    SC_M = 1
    SC_K = 2
    SC_G = 3
    SC_F = 4
    SC_A = 5
    SC_B = 6
    SC_O = 7
SpectralClass = Enum('SpectralClass',['INVALID','M','K','G','F','A','B','O'])


class Star:

    def __init__(self):
        self.id = -1
        self.name:str = ""
        self.x:int = 0
        self.y:int = 0
        #self.spectralClass:SpectralClass = SpectralClass.SC_INVALID
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


    def GetNumPlanets(self)->int:
        return self.totalPlanets


    def SpectralClassFromString(self, spectralClass:str)->SpectralClass:
        result:SpectralClass = SpectralClass.SC_INVALID
        match spectralClass:
            case "M": result = SpectralClass.SC_M
            case "K": result = SpectralClass.SC_K
            case "G": result = SpectralClass.SC_G
            case "F": result = SpectralClass.SC_F
            case "A": result = SpectralClass.SC_A
            case "B": result = SpectralClass.SC_B
            case "O": result = SpectralClass.SC_O
            case _: result = SpectralClass.SC_INVALID
        return result


    def SpectralClassToString(self, spectralClass:SpectralClass)->str:
        result:str = ""
        match spectralClass:
            case SpectralClass.SC_M: result = "M"
            case SpectralClass.SC_K: result = "K"
            case SpectralClass.SC_G: result = "G"
            case SpectralClass.SC_F: result = "F"
            case SpectralClass.SC_A: result = "A"
            case SpectralClass.SC_B: result = "B"
            case SpectralClass.SC_O: result = "O"
            case _: result = "INVALID"
        return result


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
            print(str(star))

        self.totalplanets = 0
        for child in root.findall("planet"):
            self.totalplanets += 1
            
        
        return True 

"""
        TiXmlElement * galaxy = doc.FirstChildElement("galaxy");
        if (galaxy == NULL)
            return false;

        // load all stars first, since the planets reference them
        TiXmlElement * star = galaxy->FirstChildElement("star");
        while (star != NULL)
        {
            Star newStar;
            TiXmlHandle starHandle(star);

            TiXmlText * text;

            text = starHandle.FirstChild("id").FirstChild().Text();
            if (text != NULL)
            {
                newStar.id = atoi(text->Value());
            }

            text = starHandle.FirstChild("name").FirstChild().Text();
            if (text == NULL)
                newStar.name = "";
            else
                newStar.name = text->Value();

            text = starHandle.FirstChild("x").FirstChild().Text();
            if (text != NULL)
            {
                newStar.x = atoi(text->Value());
            }

            text = starHandle.FirstChild("y").FirstChild().Text();
            if (text != NULL)
            {
                newStar.y = atoi(text->Value());
            }

            text = starHandle.FirstChild("spectralclass").FirstChild().Text();
            if (text != NULL)
            {
                newStar.spectralClass = Star::SpectralClassFromString(text->Value());
            }

            text = starHandle.FirstChild("color").FirstChild().Text();
            if (text != NULL)
            {
                newStar.color = text->Value();
            }

            text = starHandle.FirstChild("temperature").FirstChild().Text();
            if (text != NULL)
            {
                newStar.temperature = atol(text->Value());
            }

            text = starHandle.FirstChild("mass").FirstChild().Text();
            if (text != NULL)
            {
                newStar.mass = atol(text->Value());
            }

            text = starHandle.FirstChild("radius").FirstChild().Text();
            if (text != NULL)
            {
                newStar.radius = atol(text->Value());
            }

            text = starHandle.FirstChild("luminosity").FirstChild().Text();
            if (text != NULL)
            {
                newStar.luminosity = atol(text->Value());
            }

            // make sure a star with this ID doesn't already exist
            Star * existingStar = GetStarByID(newStar.id);
            if (existingStar == NULL)
            {
                // add the star
                Star * toAdd = new Star(newStar);
                stars.push_back(toAdd);
                starsByID[newStar.id] = toAdd;
                starsByLocation[make_pair(newStar.x,newStar.y)] = toAdd;
            }

            star = star->NextSiblingElement("star");
        }

        // now load all planets
        TiXmlElement * planet = galaxy->FirstChildElement("planet");
        while (planet != NULL)
        {
        Planet newPlanet;
        TiXmlHandle planetHandle(planet);

        TiXmlText * text;

        text = planetHandle.FirstChild("id").FirstChild().Text();
        if (text != NULL)
        {
            newPlanet.id = atoi(text->Value());
        }

        text = planetHandle.FirstChild("hoststar").FirstChild().Text();
        if (text != NULL)
        {
            newPlanet.hostStarID = atoi(text->Value());
        }

        text = planetHandle.FirstChild("name").FirstChild().Text();
        if (text != NULL)
        {
            newPlanet.name = text->Value();
        }

        text = planetHandle.FirstChild("size").FirstChild().Text();
        if (text != NULL)
        {
            newPlanet.size = Planet::PlanetSizeFromString(text->Value());
        }

        text = planetHandle.FirstChild("type").FirstChild().Text();
        if (text != NULL)
        {
            newPlanet.type = Planet::PlanetTypeFromString(text->Value());
        }

        text = planetHandle.FirstChild("color").FirstChild().Text();
        if (text != NULL)
        {
            newPlanet.color = text->Value();
        }

        text = planetHandle.FirstChild("temperature").FirstChild().Text();
        if (text != NULL)
        {
            newPlanet.temperature = Planet::PlanetTemperatureFromString(text->Value());
        }

        text = planetHandle.FirstChild("gravity").FirstChild().Text();
        if (text != NULL)
        {
            newPlanet.gravity = Planet::PlanetGravityFromString(text->Value());
        }

        text = planetHandle.FirstChild("atmosphere").FirstChild().Text();
        if (text != NULL)
        {
            newPlanet.atmosphere = Planet::PlanetAtmosphereFromString(text->Value());
        }

        text = planetHandle.FirstChild("weather").FirstChild().Text();
        if (text != NULL)
        {
            newPlanet.weather = Planet::PlanetWeatherFromString(text->Value());
        }

        //added to prevent landing on homeworlds
        newPlanet.landable = true;
        text = planetHandle.FirstChild("landable").FirstChild().Text();
        if (text != NULL) {
            string str = Util::ToString(text->Value());
            //all planets are landable unless otherwise specified in galaxy data
            if (str == "false") newPlanet.landable = false;
        }

        //sanity checks
        if ( newPlanet.size        == PS_INVALID   ||
                newPlanet.type        == PT_INVALID   ||
                newPlanet.temperature == PTMP_INVALID ||
                newPlanet.gravity     == PG_INVALID   ||
                newPlanet.atmosphere  == PA_INVALID )
        {
                std::string msg = "loadGalaxy: error loading planet #" + newPlanet.id;
                msg += " , name -- " + newPlanet.name + " --";
                msg += " , size " + Planet::PlanetSizeToString(newPlanet.size);
                msg += " , type " + Planet::PlanetTypeToString(newPlanet.type);
                msg += " , temperature " + Planet::PlanetTemperatureToString(newPlanet.temperature);
                msg += " , gravity " + Planet::PlanetGravityToString(newPlanet.gravity);
                msg += " , atmosphere " + Planet::PlanetAtmosphereToString(newPlanet.atmosphere);
                msg += "\n";
                TRACE(msg.c_str());
                ASSERT(0);
        }

        // make sure the host star does exist
        Star * hostStar = GetStarByID(newPlanet.hostStarID);
        if (hostStar != NULL)
        {
            // make sure a planet with this ID doesn't already exist in the host star
            Planet * existingPlanet = hostStar->GetPlanetByID(newPlanet.id);
            if (existingPlanet == NULL)
            {
            // add the planet to the host star
            Planet * toAdd = new Planet(newPlanet);
            hostStar->planets.push_back(toAdd);
            hostStar->planetsByID[newPlanet.id] = toAdd;
            }
        }


        // add to the large list of all planets (not bound by host star)
        Planet * toAdd = new Planet(newPlanet);
        allPlanets.push_back(toAdd);
        allPlanetsByID[newPlanet.id] = toAdd;


            planet = planet->NextSiblingElement("planet");
        }

        return true;
"""

#endregion
