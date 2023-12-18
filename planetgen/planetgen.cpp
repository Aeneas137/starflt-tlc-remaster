/*
Starflight Engine
Planet texture generator
To-do:
    look into a lib to convert bmp to png
    add more args to control rendering
    add resolution as an argument

*/

#include "stdafx.h"

#pragma comment(lib,"libnoise.lib")
#include "noise/noise.h"
#include "noiseutils.h"
using namespace noise;

#include <iterator>
#include <vector>
#include <cstdlib>
#include <iomanip>
#include <iostream>
#include <sstream>
#include <string>
using namespace std;

const int HOMEWORLD_ID = 8;

//SpectralClass "M","K","G","F","A","B","O"
//PlanetSize SMALL,MEDIUM,LARGE,HUGE 
//PlanetType ASTEROID,ROCKY,FROZEN,OCEANIC,MOLTEN,GASGIANT,ACIDIC
//PlanetTemperature SUBARCTIC,ARCTIC,TEMPERATE,TROPICAL,SEARING,INFERNO
//PlanetGravity NEGLIGIBLE,VERYLOW,LOW,OPTIMAL,VERYHEAVY,CRUSHING 
//PlanetAtmosphere NONE,TRACEGASES,BREATHABLE,ACIDIC,TOXIC,FIRESTORM 
//PlanetWeather NONE,CALM,MODERATE,VIOLENT,VERYVIOLENT 


void createPlanetSurface(int width, int height, int randomness, std::string planetType, std::string filename)
{
    module::Perlin perlin;
    perlin.SetSeed(randomness);
    perlin.SetFrequency(1.0);
    perlin.SetOctaveCount(6);
    perlin.SetPersistence (0.5);

    if (planetType=="FROZEN")
    {
            perlin.SetOctaveCount(5);
            perlin.SetPersistence (0.4);
    }
    else if (planetType=="GASGIANT" || planetType=="GAS GIANT")
    {
            perlin.SetOctaveCount(3);
            perlin.SetPersistence (0.3);
    }
    else if (planetType=="MOLTEN")
    {
            perlin.SetOctaveCount(6);
            perlin.SetFrequency(1.4);
            perlin.SetPersistence (0.5);
    }

    cout << "Initializing noise map builder...";
    utils::NoiseMap heightMap;
    utils::NoiseMapBuilderSphere heightMapBuilder;
    heightMapBuilder.SetSourceModule (perlin);
    heightMapBuilder.SetDestNoiseMap (heightMap);
    heightMapBuilder.SetDestSize (width, height);
    heightMapBuilder.SetBounds (-90.0, 90.0, -180.0, 180.0);
    heightMapBuilder.Build();
    utils::RendererImage renderer;
    utils::Image image;
    renderer.SetSourceNoiseMap (heightMap);
    renderer.SetDestImage (image);
    renderer.ClearGradient();
    cout << "done." << endl;

    int random_value = 0;
	srand(randomness);

   if (planetType=="OCEANIC")
   {
        renderer.AddGradientPoint (-1.0000, utils::Color (0, 0, 120, 255)); // deeps
        renderer.AddGradientPoint (-0.2500, utils::Color (0, 0, 255, 255)); // shallow
        renderer.AddGradientPoint ( 0.0000, utils::Color (0, 120, 250, 255)); // shore
        renderer.AddGradientPoint ( 0.0625, utils::Color (180, 180, 60, 255)); // sand
        renderer.AddGradientPoint ( 0.1250, utils::Color (50, 160, 0, 255)); // grass
        renderer.AddGradientPoint ( 0.3750, utils::Color (180, 180, 0, 255)); // dirt
        renderer.AddGradientPoint ( 0.7500, utils::Color (150, 150, 150, 255)); // rock
        renderer.AddGradientPoint ( 1.0000, utils::Color (255, 255, 255, 255)); // snow
        cout << "Generating OCEANIC planet: gradient points = 8" << endl;

   }
   else if (planetType=="ACIDIC")
   {
		//renderer.AddGradientPoint (-1.0000, utils::Color (120, 0, 120, 255)); // deeps
		//renderer.AddGradientPoint (-0.2500, utils::Color (175, 0, 175, 255)); // shallow
		//renderer.AddGradientPoint ( 0.0000, utils::Color (220, 0, 220, 255)); // shore
		renderer.AddGradientPoint (-1.0000, utils::Color (0, 115, 27, 255)); // acid
		renderer.AddGradientPoint (-0.2500, utils::Color (0, 255, 0, 255)); // shallow
		renderer.AddGradientPoint ( 0.0000, utils::Color (60, 240, 135, 255)); // shore
		//renderer.AddGradientPoint ( 0.0625, utils::Color (180, 180, 60, 255)); // sand
        renderer.AddGradientPoint ( 0.1250, utils::Color (155, 50, 80, 255)); // grass
        //renderer.AddGradientPoint ( 0.3750, utils::Color (180, 180, 0, 255)); // dirt
        renderer.AddGradientPoint ( 0.7500, utils::Color (30, 30, 100, 255)); // rock
        renderer.AddGradientPoint ( 1.0000, utils::Color (60, 50, 115, 255)); // snow
        cout << "Generating ACIDIC planet: gradient points = 6" << endl;
   }
   else if (planetType=="FROZEN")
   {
       //  renderer.AddGradientPoint (-1.0000, utils::Color (130, 130, 150, 255)); // deeps
		//   renderer.AddGradientPoint (-0.2500, utils::Color (140, 140, 150, 255)); // shallow
		 renderer.AddGradientPoint (-1.0000, utils::Color (65, 65, 150, 255)); // deeps
         renderer.AddGradientPoint (-0.2500, utils::Color (100, 100, 150, 255)); // shallow
         renderer.AddGradientPoint ( 0.0000, utils::Color (150, 150, 150, 255)); // shore
         renderer.AddGradientPoint ( 0.0625, utils::Color (160, 160, 160, 255)); // sand
         renderer.AddGradientPoint ( 0.1250, utils::Color (170, 170, 170, 255)); // grass
         renderer.AddGradientPoint ( 0.3750, utils::Color (200, 200, 200, 255)); // dirt
         renderer.AddGradientPoint ( 0.7500, utils::Color (230, 230, 230, 255)); // rock
         renderer.AddGradientPoint ( 1.0000, utils::Color (255, 255, 255, 255)); // snow
        cout << "Generating FROZEN planet: gradient points = 8" << endl;
   }
   else if (planetType=="ROCKY")
   {
         renderer.AddGradientPoint (-1.0000, utils::Color (120, 100, 100, 255)); // deeps
         renderer.AddGradientPoint (-0.2500, utils::Color (120, 120, 120, 255)); // shallow
         renderer.AddGradientPoint ( 0.0000, utils::Color (160, 150, 160, 255)); // shore
         renderer.AddGradientPoint ( 0.0625, utils::Color (120, 120, 100, 255)); // sand
         renderer.AddGradientPoint ( 0.1250, utils::Color (120, 120, 120, 255)); // grass
         renderer.AddGradientPoint ( 0.3750, utils::Color (150, 160, 170, 255)); // dirt
         renderer.AddGradientPoint ( 0.7500, utils::Color (150, 150, 150, 255)); // rock
         renderer.AddGradientPoint ( 1.0000, utils::Color (160, 150, 160, 255)); // snow
        cout << "Generating ROCKY planet: gradient points = 8" << endl;
   }
   else if (planetType=="GASGIANT" || planetType=="GAS GIANT")
   {
		//randomly choose from 4 gas giant colors
		random_value = rand()%4;
		if(random_value == 0){ //purple
			renderer.AddGradientPoint (-1.0000, utils::Color (80, 0, 80, 255)); 
			renderer.AddGradientPoint (-0.5000, utils::Color (160, 0, 160, 255)); 
			renderer.AddGradientPoint ( 0.0000, utils::Color (175, 150, 175, 255)); 
			renderer.AddGradientPoint ( 0.5000, utils::Color (182, 99, 182, 255)); 
			renderer.AddGradientPoint ( 1.0000, utils::Color (160, 140, 160, 255)); 
            cout << "Generating GAS GIANT planet: color = PURPLE, gradient points = 5" << endl;
		}else if(random_value == 1){ //green
			renderer.AddGradientPoint (-1.0000, utils::Color (0, 100, 0, 255)); 
			renderer.AddGradientPoint (-0.5000, utils::Color (0, 140, 0, 255)); 
			renderer.AddGradientPoint ( 0.0000, utils::Color (100, 180, 100, 255)); 
			renderer.AddGradientPoint ( 0.5000, utils::Color (0, 150, 0, 255)); 
			renderer.AddGradientPoint ( 1.0000, utils::Color (0, 180, 0, 255)); 
            cout << "Generating GAS GIANT planet: color = GREEN, gradient points = 5" << endl;
		}else if(random_value == 2){ //blue
			renderer.AddGradientPoint (-1.0000, utils::Color (0, 45, 110, 255)); 
			renderer.AddGradientPoint (-0.5000, utils::Color (0, 0, 140, 255)); 
			renderer.AddGradientPoint ( 0.0000, utils::Color (100, 100, 180, 255)); 
			renderer.AddGradientPoint ( 0.5000, utils::Color (0, 100, 180, 255)); 
			renderer.AddGradientPoint ( 1.0000, utils::Color (100, 190, 210, 255));
            cout << "Generating GAS GIANT planet: color = BLUE, gradient points = 5" << endl;
		}else{	//red
			renderer.AddGradientPoint (-1.0000, utils::Color (145, 95, 50, 255)); 
			renderer.AddGradientPoint (-0.5000, utils::Color (70, 0, 0, 255)); 
			renderer.AddGradientPoint ( 0.0000, utils::Color (180, 100, 100, 255)); 
			renderer.AddGradientPoint ( 0.5000, utils::Color (150, 0, 0, 255)); 
			renderer.AddGradientPoint ( 1.0000, utils::Color (255, 145, 0, 255));
            cout << "Generating GAS GIANT planet: color = RED, gradient points = 5" << endl;
		}
   }
   else if (planetType=="MOLTEN")
   {
		renderer.AddGradientPoint (-1.0000, utils::Color (200, 30, 30, 255)); 
		renderer.AddGradientPoint (-0.6000, utils::Color (235, 40, 40, 255)); 
		renderer.AddGradientPoint (-0.3000, utils::Color (255, 50, 50, 255)); 
		renderer.AddGradientPoint ( 0.0000, utils::Color (80, 70, 70, 255));
		renderer.AddGradientPoint ( 0.1250, utils::Color (100, 100, 100, 255)); 
		renderer.AddGradientPoint ( 0.5000, utils::Color (150, 120, 100, 255)); 
		renderer.AddGradientPoint ( 1.0000, utils::Color (130, 140, 140, 255)); 
        cout << "Generating MOLTEN planet: gradient points = 7" << endl;
	}
	else if (planetType=="ASTEROID")
	{
		renderer.AddGradientPoint (-1.0000, utils::Color (0, 0, 0, 255)); 
		renderer.AddGradientPoint (-0.6000, utils::Color (20, 20, 20, 255)); 
		renderer.AddGradientPoint (-0.2000, utils::Color (30, 30, 30, 255)); 
		renderer.AddGradientPoint ( 0.0000, utils::Color (40, 40, 40, 255)); 
		renderer.AddGradientPoint ( 0.1000, utils::Color (50, 50, 50, 255));
		renderer.AddGradientPoint ( 0.3000, utils::Color (60, 60, 60, 255)); 
		renderer.AddGradientPoint ( 0.6000, utils::Color (70, 70, 70, 255)); 
		renderer.AddGradientPoint ( 1.0000, utils::Color (90, 90, 90, 255)); 
        cout << "Generating ASTEROID planetoid: gradient points = 8" << endl;
	}
    else {
		// placeholder -- something in case the type is invalid
        cout << "Planet type is invalid: " << planetType << endl;
        cout << "Generating filler texture: gradient points = 8" << endl;
		renderer.AddGradientPoint (-1.0000, utils::Color (120, 100, 100, 255)); // deeps
		renderer.AddGradientPoint (-0.2500, utils::Color (120, 120, 120, 255)); // shallow
		renderer.AddGradientPoint ( 0.0000, utils::Color (160, 150, 160, 255)); // shore
		renderer.AddGradientPoint ( 0.0625, utils::Color (120, 120, 100, 255)); // sand
		renderer.AddGradientPoint ( 0.1250, utils::Color (120, 120, 120, 255)); // grass
		renderer.AddGradientPoint ( 0.3750, utils::Color (150, 160, 170, 255)); // dirt
		renderer.AddGradientPoint ( 0.7500, utils::Color (150, 150, 150, 255)); // rock
		renderer.AddGradientPoint ( 1.0000, utils::Color (160, 150, 160, 255)); // snow
    }

    //create the texture and save to a bmp file
    cout << "Renderer settings:" << endl;
    renderer.EnableLight();
    cout << "Lighting: enabled" << endl;
    renderer.SetLightContrast(3.0);
    cout << "Light contrast: 3.0" << endl;
    renderer.SetLightBrightness(2.0);
    cout << "Light brightness: 2.0" << endl;
    renderer.SetLightColor(utils::Color(255,255,255,255));
    cout << "Light color: 255,255,255" << endl;
    cout << "Rendering...";
    renderer.Render();
    cout << "done." << endl;

    cout << "Saving texture to file...";
    utils::WriterBMP writer;
    writer.SetSourceImage(image);
    writer.SetDestFilename(filename);
    writer.WriteDestFile();
    cout << "done." << endl;
}



static int StringToInt(const std::string &str)
{
    int i;
    try {
        i = std::stoi(str);
    }
    catch (...) {
        return 0;
    }
    return i;
}

std::string ToUpper(std::string& str)
{
	std::string converted;
	for(int i = 0; i < str.size(); ++i)
		converted += toupper(str[i]);
	return converted;
}


int main(int argc, char* argv[])
{
	string spectralClass="";
    string planetSize="";
    string planetType="";
    string planetColor="";
    string planetTemperature="";
    string planetGravity="";
    string planetAtmosphere="";
    string planetWeather="";
    int TEX_SIZE=1024;
    int planetid = 0;

    if (argc < 2)
    {
        cout << "Args: planet_id planet_type (oceanic,molten,etc)" << endl;
        return 0;
    }

    std::vector <std::string> args;
    for (int i = 1; i < argc; ++i) 
        args.push_back(argv[i]); 

    planetid = StringToInt(args[0]);
    if (planetid==0)
    {
        cout << "planet_id must be numeric" << endl;
        return 1;
    }
    cout << "planet_id: " << planetid << endl;

    planetType = ToUpper(args[1]);
    cout << "planet_type: " << planetType << endl;

    std::ostringstream os;

	std::string planetFilename="";

	//use starid and planetid for random seed
	int randomness = planetid;

	//planet textures created using starid and planetid as a random seed

	os.str("");
	os << "planet_" << randomness << "_" << TEX_SIZE << ".bmp";
	planetFilename = os.str();
	cout << "Filename: " << planetFilename << endl;

    createPlanetSurface(TEX_SIZE, TEX_SIZE, randomness, planetType, planetFilename);

	string line;
	getline(cin, line);

    return 0;
}

