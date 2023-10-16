


"""
#define MAX_FLUX 2000
typedef std::list<Flux*>::iterator flux_iter;

// item types
typedef enum
{
   IT_INVALID = 0,
   IT_ARTIFACT = 1,
   IT_RUIN = 2,
   IT_MINERAL = 4,
   IT_LIFEFORM = 8,
   IT_TRADEITEM = 16
} ItemType;

// item age
typedef enum
{
   IA_INVALID = 0,
   IA_STONE,
   IA_METAL,
   IA_INDUSTRIAL,
   IA_SPACEFARING
} ItemAge;

// an item
class Item
{
public:

   Item();
   Item(const Item& rhs);
   virtual ~Item();
   Item& operator=(const Item& rhs);

   void Reset();

   bool IsArtifact() {return itemType == IT_ARTIFACT;};
   bool IsMineral()  {return itemType == IT_MINERAL;};
   bool IsLifeForm() {return itemType == IT_LIFEFORM;};

   ID id;                   // the ID of this item
   ItemType itemType;       // the type of item
   std::string name;        // the name
   double value;            // value
   double size;             // size (m^3)
   double speed;            // speed
   double danger;           // danger
   double damage;           // damage
   ItemAge itemAge;         // age
   bool shipRepairMetal;    // is this a ship repair metal?
   bool blackMarketItem;    // is this a blackmarket item?
   std::string portrait;    //This refers to the image file

   //for Artifact items these properties are used:
   int planetid;
   int x;
   int y;

   //additional properties for Ruins:
   std::string description;

   // helper methods for working with the enumerated types
   static ItemType ItemTypeFromString(std::string s);
   static std::string ItemTypeToString(ItemType itemType);
   static ItemAge ItemAgeFromString(std::string s);
   static std::string ItemAgeToString(ItemAge itemAge);
};

// used to represent a collection of items; the collection is comprised of
// stacks of items; for example, 100 cans of root beer, 3 slim jims, etc; you can request
// the # of stacks, and then iterate over all the stacks; each stack returns
// to you the item and the quantity in that stack
class Items
{
public:
   Items();
   Items(const Items& rhs);
   virtual ~Items();
   Items& operator=(const Items& rhs);

   void Reset();
   bool Serialize(Archive& ar);

   /**
    * initializes this object to contain a random collection of items.
    * @param maxNumStacks # of stacks will not exceed this value
    * @param maxNumItemsPerStack # of items in any stack will not exceed this value
    * @param typeFilter if provided, only items of the specified type mask will be generated
    */
   void RandomPopulate(int maxNumStacks, int maxNumItemsPerStack, ItemType typeFilter = IT_INVALID);

   /**
    * returns the number of stacks, each stack contains a set of a single item type
    */
   int GetNumStacks();

   /**
    * returns a single stack of items - the item info and the number of that item in the stack
    */
   void GetStack(int idx, Item& item, int& numItemsInStack);

   /**
    * add the specified quantity of the item ID to this object; the item(s) will be
    * added to the stack of that item type if already present.
    */
   void AddItems(ID id, int numItemsToAdd);

   /**
	* this function should be called before any item is added to the inventory!
	* returns true if it finds space for the list of items, and false if it doesn't.
	* the ellipse takes in the item ids of each item to be added
    */
	bool CheckForSpace(int spaceLimit, ... );
	bool CheckForSpace(int spaceLimit, int totalSentIDs, int itemIDs[] );



   /**
    * remove the specified quantity of the item ID from this object; the stack of this
    * item type will be decremented by the specified amount; it will not go below zero.
    */
   void RemoveItems(ID id, int numItemsToRemove);

   /**
    * sets the # of the specified item to the value provided, overwriting the existing
    * value if the item is already present or adding it if not.
    */
   void SetItemCount(ID id, int numItems);

	/**
    * scan the vector for the item with the given id value and set the item placeholder to the item matching that id
    */
   void Get_Item_By_ID(int id, Item& item, int &num_in_stack);

   void Get_Item_By_Name(std::string name, Item& item, int &num_in_stack);


private:
   std::vector<std::pair<ID,int> > stacks; // holds the stacks (each stack is a set of one item type)
};


class DataMgr
{
public:

   // don't create new instances of this class, use the instance provided in the Module class
   DataMgr();
   virtual ~DataMgr();

   // only called once at game initialization to load in all the data and prepare it for access
   // shouldn't need to call this.
   bool Initialize();

   // used to access available items; memory is owned by this class; you should not delete
   // any returned objects
   int GetNumItems();
   Item* GetItem(int idx);			// by index [0..N)
   Item* GetItemByID(ID id);		// by ID
   Item* GetItem(std::string name); // by name

   // used to access the available stars; memory is owned by this class; you should not delete
   // any returned objects
   int GetNumStars();
   Star* GetStar(int idx); // by index [0...N)
   Star* GetStarByID(ID id); // by ID
   Star* GetStarByLocation(CoordValue x, CoordValue y); // by location

   //this version does not require a star parent class
   std::vector<Planet*> allPlanets;
   std::map<ID,Planet*> allPlanetsByID;
   Planet *GetPlanetByID(ID id);

   int GetNumHumanNames();
   std::string GetFullName(int id);
   std::string GetFirstName(int id);
   std::string GetLastName(int id);
   std::string GetRandWholeName();
   std::string GetRandMixedName();

  //this should have only be needed during testing
   //Officer* GetRandOfficer(int type);
   std::list<Flux*> flux;


private:
   bool m_initialized;
   bool LoadItems();
   bool LoadGalaxy();
   bool LoadHumanNames();

   std::vector<Item*> items;
   std::map<ID,Item*> itemsByID;
   std::vector<Star*> stars;
   std::map<ID,Star*> starsByID;
   std::map<std::pair<CoordValue,CoordValue>,Star*> starsByLocation;
   std::vector<std::pair<std::string*,std::string*>*> humanNames;

};



#define ITEMS_FILE "data/strfltitems.xml"
#define GALAXY_FILE "data/galaxy.xml"
#define HUMANNAMES_FILE "data/human.xml"

Item::Item()
{
   Reset();
}

Item::Item(const Item& rhs)
{
   *this = rhs;
}

Item::~Item()
{
}

Item& Item::operator=(const Item& rhs)
{
   id = rhs.id;
   itemType = rhs.itemType;
   name = rhs.name;
   value = rhs.value;
   size = rhs.size;
   speed = rhs.speed;
   danger = rhs.danger;
   damage = rhs.damage;
   itemAge = rhs.itemAge;
   shipRepairMetal = rhs.shipRepairMetal;
   blackMarketItem = rhs.blackMarketItem;
   portrait = rhs.portrait;
   planetid = rhs.planetid;
   x = rhs.x;
   y = rhs.y;
   description = rhs.description;

   return *this;
}

void Item::Reset()
{
   id = 0;
   itemType = IT_INVALID;
   name = "";
   value = 0;
   size = 0;
   speed = 0;
   danger = 0;
   damage = 0;
   itemAge = IA_INVALID;
   shipRepairMetal = false;
   blackMarketItem = false;
   portrait = "";
   planetid = 0;
   x = 0;
   y = 0;
}

ItemType Item::ItemTypeFromString(std::string s)
{
   ItemType result = IT_INVALID;

   if (s == "Artifact")
   {
      result = IT_ARTIFACT;
   }
   else if (s == "Ruin")
   {
      result = IT_RUIN;
   }
   else if (s == "Mineral")
   {
      result = IT_MINERAL;
   }
   else if (s == "Life Form")
   {
      result = IT_LIFEFORM;
   }
   else if (s == "Trade Item")
   {
      result = IT_TRADEITEM;
   }

   return result;
}

std::string Item::ItemTypeToString(ItemType itemType)
{
   string result;

   switch (itemType)
   {
   case IT_ARTIFACT:
      result = "Artifact";
      break;
   case IT_RUIN: 
      result = "Ruin";
      break;
   case IT_MINERAL:
      result = "Mineral";
      break;
   case IT_LIFEFORM:
      result = "Life Form";
      break;
   case IT_TRADEITEM:
      result = "Trade Item";
      break;
   default:
      result = "INVALID";
      break;
   }

   return result;
}

ItemAge Item::ItemAgeFromString(std::string s)
{
   ItemAge result = IA_INVALID;

   if (s == "Stone")
   {
      result = IA_STONE;
   }
   else if (s == "Metal")
   {
      result = IA_METAL;
   }
   else if (s == "Industrial")
   {
      result = IA_INDUSTRIAL;
   }
   else if (s == "Space Faring")
   {
      result = IA_SPACEFARING;
   }

   return result;
}

std::string Item::ItemAgeToString(ItemAge itemAge)
{
   string result;

   switch (itemAge)
   {
   case IA_STONE:
      result = "Stone";
      break;
   case IA_METAL:
      result = "Metal";
      break;
   case IA_INDUSTRIAL:
      result = "Industrial";
      break;
   case IA_SPACEFARING:
      result = "Space Faring";
      break;
   default:
      result = "INVALID";
      break;
   }

   return result;
}



DataMgr::DataMgr()
: m_initialized(false)
{
}

DataMgr::~DataMgr()
{
   for (vector<Star*>::iterator i = stars.begin(); i != stars.end(); ++i)
   {
      delete (*i);
   }

   for (vector<std::pair<std::string*,std::string*>*>::iterator i = humanNames.begin(); i != humanNames.end(); ++i)
   {
      delete (*i);
   }
   for (flux_iter i = g_game->dataMgr->flux.begin(); i != g_game->dataMgr->flux.end(); i++){
		delete (*i);
	}
	flux.clear();
}

int DataMgr::GetNumItems()
{
   return (int)items.size();
}

Item* DataMgr::GetItem(int idx)
{
   Item* result = NULL;

   if ((idx >= 0) && (idx < (int)items.size()))
   {
      result = items[idx];
   }

   return result;
}

Item* DataMgr::GetItemByID(ID id)
{
   Item* result = NULL;

   map<ID,Item*>::iterator i = itemsByID.find(id);
   if (i != itemsByID.end())
   {
      result = i->second;
   }

   return result;
}

Item* DataMgr::GetItem(string name) {
	Item* result= NULL;
	for (vector<Item *>::iterator i= items.begin(); i != items.end(); ++i){
		if ((*i)->name == name) result= *i;
	}
	return result;
}

int DataMgr::GetNumStars()
{
   return (int)stars.size();
}

Star * DataMgr::GetStar(int idx)
{
   Star * result = NULL;

   if ((idx >= 0) && (idx < (int)stars.size()))
   {
      result = stars[idx];
   }

   return result;
}

Star * DataMgr::GetStarByID(ID id)
{
   Star * result = NULL;

   map<ID,Star*>::iterator i = starsByID.find(id);
   if (i != starsByID.end())
   {
      result = i->second;
   }

   return result;
}

Star* DataMgr::GetStarByLocation(CoordValue x, CoordValue y)
{
   Star * result = NULL;

   map<pair<CoordValue,CoordValue>,Star*>::iterator i = starsByLocation.find(make_pair(x,y));
   if (i != starsByLocation.end())
   {
      result = i->second;
   }

   return result;
}

Planet* DataMgr::GetPlanetByID(ID id)
{
   Planet * result = NULL;

   map<ID,Planet*>::iterator i = allPlanetsByID.find(id);
   if (i != allPlanetsByID.end())
   {
      result = i->second;
   }

   return result;
}


int DataMgr::GetNumHumanNames()
{
	return (int)humanNames.size();
}

string DataMgr::GetFullName(int id)
{
	if (id < (int)humanNames.size() && id >= 0)
		return *humanNames[id]->first + " " + *humanNames[id]->second;
	else
		return "";
}

string DataMgr::GetFirstName(int id)
{
	if (id < (int)humanNames.size() && id >= 0)
		return *humanNames[id]->first;
	else
		return "";
}

string DataMgr::GetLastName(int id)
{
	if (id < (int)humanNames.size() && id >= 0)
		return *humanNames[id]->second;
	else
		return "";
}

string DataMgr::GetRandWholeName()
{
	int randomID = Util::Random(0, (int)humanNames.size()-1);
	return *humanNames[randomID]->first + " " + *humanNames[randomID]->second;
}

string DataMgr::GetRandMixedName()
{
	try {
		if (humanNames.size() == 0) {
			g_game->message("ERROR: The human names data has not been loaded.");
			return "<Error>";
		}

		int randomID = Util::Random(0, (int)humanNames.size()-1);
		int randomID2 = Util::Random(0, (int)humanNames.size()-1);

		return *humanNames[randomID]->first + " " + *humanNames[randomID2]->second;
	}
	catch(...) {
		g_game->message("ERROR: The human names data has not been loaded.");
		return "<error>";
	}
	return "<Error>";
}



bool DataMgr::Initialize()
{
   if (m_initialized)
      return true;

   m_initialized = true;

   if (!LoadItems())
      return false;

   if (!LoadGalaxy())
      return false;

   if (!LoadHumanNames())
	   return false;


   return true;
}

bool DataMgr::LoadItems()
{

   //open the strfltitems.xml file

   TiXmlDocument doc(ITEMS_FILE);
   if (!doc.LoadFile())
      return false;

   //load root of xml hierarchy
   TiXmlElement * itemSet = doc.FirstChildElement("items");
   if (itemSet == NULL)
      return false;

   // load all items
   TiXmlElement * item = itemSet->FirstChildElement("item");
   while (item != NULL)
   {
      Item newItem;
      TiXmlHandle itemHandle(item);

      TiXmlText * text;

      text = itemHandle.FirstChild("ID").FirstChild().Text();
      if (text != NULL)
      {
         newItem.id = atoi(text->Value());
      }

      text = itemHandle.FirstChild("Type").FirstChild().Text();
      if (text != NULL)
      {
         newItem.itemType = Item::ItemTypeFromString(text->Value());
      }

      text = itemHandle.FirstChild("Name").FirstChild().Text();
      if (text != NULL)
      {
         newItem.name = text->Value();
      }

      text = itemHandle.FirstChild("Value").FirstChild().Text();
      if (text != NULL)
      {
         newItem.value = atof(text->Value());
      }

      text = itemHandle.FirstChild("Size").FirstChild().Text();
      if (text != NULL)
      {
         newItem.size = atof(text->Value());
      }

      text = itemHandle.FirstChild("Speed").FirstChild().Text();
      if (text != NULL)
      {
         newItem.speed = atof(text->Value());
      }

      text = itemHandle.FirstChild("Danger").FirstChild().Text();
      if (text != NULL)
      {
         newItem.danger = atof(text->Value());
      }

      text = itemHandle.FirstChild("Damage").FirstChild().Text();
      if (text != NULL)
      {
         newItem.damage = atof(text->Value());
      }

      text = itemHandle.FirstChild("Age").FirstChild().Text();
      if (text != NULL)
      {
         newItem.itemAge = Item::ItemAgeFromString(text->Value());
      }

      text = itemHandle.FirstChild("ShipRepairMetal").FirstChild().Text();
      if (text != NULL)
      {
         string v(text->Value());
         newItem.shipRepairMetal = v == "true";
      }

      text = itemHandle.FirstChild("BlackMarket").FirstChild().Text();
      if (text != NULL)
      {
         string v(text->Value());
         newItem.blackMarketItem = v == "true";
      }

	  text = itemHandle.FirstChild("Portrait").FirstChild().Text();
      if (text != NULL)
      {
		 newItem.portrait = text->Value();
      }

	  //new property for Artifacts
	  text = itemHandle.FirstChild("planetid").FirstChild().Text();
	  if (text != NULL)
	  {
		  newItem.planetid = atof(text->Value());
	  }
	  //new property for Artifacts
	  text = itemHandle.FirstChild("x").FirstChild().Text();
	  if (text != NULL)
	  {
		newItem.x = atof(text->Value());
	  }
	  //new property for Artifacts
	  text = itemHandle.FirstChild("y").FirstChild().Text();
	  if (text != NULL)
	  {
		newItem.y = atof(text->Value());
	  }

	  //new property for Ruins (and now for lifeForms too).
	  text = itemHandle.FirstChild("Description").FirstChild().Text();
	  if (text != NULL)
	  {
        newItem.description = text->Value();
	  }

      // make sure an item with this ID doesn't already exist
      Item * existingItem = GetItemByID(newItem.id);
      if (existingItem == NULL)
      {
         // add the item
         Item * toAdd = new Item(newItem);
         items.push_back(toAdd);
         itemsByID[newItem.id] = toAdd;
      }

      item = item->NextSiblingElement("item");
   }

   return true;
}




bool DataMgr::LoadHumanNames()
{
	TiXmlDocument doc(HUMANNAMES_FILE);
	if (!doc.LoadFile())
	  return false;

	TiXmlElement * people = doc.FirstChildElement("Names");
	if (people == NULL)
	  return false;

	// load all stars first, since the planets reference them
	TiXmlElement * name = people->FirstChildElement("Name");
	while (name != NULL)
	{
		string firstName;
		string lastName;
		TiXmlHandle nameHandle(name);

		TiXmlText * text;

		//Check for first name
		text = nameHandle.FirstChild("First").FirstChild().Text();
		if (text == NULL)
			firstName = "";
		else
			firstName = text->Value();

		//Check for last name
		text = nameHandle.FirstChild("Last").FirstChild().Text();
		if (text == NULL)
			lastName = "";
		else
			lastName = text->Value();

		//Add the name to the list
		std::pair<std::string*,std::string*> * newName = new std::pair<std::string*,std::string*>;
		newName->first = new string(firstName);
		newName->second = new string(lastName);
        humanNames.push_back(newName);

		//Grab next name
		 name = name->NextSiblingElement("Name");
	}

	return true;
}

/*
 * THIS CODE WAS ONLY NEEDED FOR TEMPORARY OFFICER DATA
 */
//Officer* DataMgr::GetRandOfficer(int type)
//{
//	Officer *o = new Officer();
//
//	o->name = g_game->dataMgr->GetRandMixedName();
//
//	o->SetOfficerType(type);
//
//	for (int i=0; i < 6; i++)
//		o->attributes[i] = Util::Random(0,200);
//
//	o->attributes[6] = Util::Random(1,25);
//	o->attributes[7] = Util::Random(1,25);
//
//	return o;
//}

Items::Items()
{
   Reset();
}

Items::Items(const Items& rhs)
{
   *this = rhs;
}

Items::~Items()
{
}

Items& Items::operator=(const Items& rhs)
{
   Reset();

   for (vector<pair<ID,int> >::const_iterator i = rhs.stacks.begin(); i != rhs.stacks.end(); ++i)
   {
      stacks.push_back(*i);
   }

   return *this;
}

void Items::Reset()
{
   stacks.clear();
}

bool Items::Serialize(Archive& ar)
{
   string ClassName = "Items";
   int Schema = 0;

   if (ar.IsStoring())
   {
      ar << ClassName;
      ar << Schema;

      int numStacks = (int)stacks.size();
      ar << numStacks;
      for (vector<pair<ID,int> >::iterator i = stacks.begin(); i != stacks.end(); ++i)
      {
         int id = i->first;
         int numItems = i->second;

         ar << id;
         ar << numItems;
      }
   }
   else
   {
      Reset();

      string LoadClassName;
      ar >> LoadClassName;
      if (LoadClassName != ClassName)
         return false;

      int LoadSchema;
      ar >> LoadSchema;
      if (LoadSchema > Schema)
         return false;

      int numStacks;
      ar >> numStacks;
      for (int i = 0; i < numStacks; i++)
      {
         int id;
         ar >> id;
         int numItems;
         ar >> numItems;
         stacks.push_back(make_pair(id,numItems));
      }
   }

   return true;
}

void Items::RandomPopulate(int maxNumStacks, int maxNumItemsPerStack, ItemType typeFilter /*= IT_INVALID*/)
{
   Reset();

   int numStacks = rand() % maxNumStacks + 1;
   int numItemTypes = g_game->dataMgr->GetNumItems();

   map<int,bool> usedItemTypes;

   for (int i = 0; i < numStacks; i++)
   {
      int itemTypeIdx = -1;
      Item* pItem = NULL;
      while (itemTypeIdx < 0)
      {
         int randItemTypeIdx = rand() % numItemTypes;
         pItem = g_game->dataMgr->GetItem(randItemTypeIdx);;
         if (usedItemTypes.find(randItemTypeIdx) == usedItemTypes.end())
         {
            if ((typeFilter == IT_INVALID) ||
                ((typeFilter & pItem->itemType) != 0))
            {
               usedItemTypes[randItemTypeIdx] = true;
               itemTypeIdx = randItemTypeIdx;
            }
         }
      }

      int numItemsInStack = rand() % maxNumItemsPerStack + 1;
      stacks.push_back(make_pair(pItem->id,numItemsInStack));
   }
}

int Items::GetNumStacks()
{
   return (int)stacks.size();
}

void Items::GetStack(int idx, Item& item, int& numItemsInStack)
{
   item.Reset();
   numItemsInStack = 0;

   if (idx < 0)
      return;
   if (idx >= GetNumStacks())
      return;

   pair<ID,int> stack = stacks[idx];

   Item * pItem = g_game->dataMgr->GetItemByID(stack.first);
   if (pItem == NULL)
      return;

   item = *pItem;
   numItemsInStack = stack.second;
}

bool Items::CheckForSpace(int spaceLimit, ... )
{
	int totalIDs = 0;
	va_list itemIDs;

	va_start( itemIDs, spaceLimit );

	for (int id = va_arg( itemIDs, int ), lastID = id; id != lastID; lastID = id, id = va_arg( itemIDs, int ))
	{
		++totalIDs;
		for (vector<pair<ID,int> >::iterator i = stacks.begin(); i != stacks.end(); ++i)
		{
		  if (i->first == id)
		  {
			  --totalIDs;
			 break;
		  }
		}
	}

	va_end( itemIDs );

	return (spaceLimit >= (int)stacks.size() + totalIDs);
}


bool Items::CheckForSpace(int spaceLimit, int totalSentIDs, int itemIDs[] )
{
	int totalIDs = 0;

	for (int id = 0; id < totalSentIDs; ++id )
	{
		++totalIDs;
		for (vector<pair<ID,int> >::iterator i = stacks.begin(); i != stacks.end(); ++i)
		{
		  if (i->first == itemIDs[id])
		  {
			 --totalIDs;
			 break;
		  }
		}
	}

	return (spaceLimit >= (int)stacks.size() + totalIDs);
}


void Items::AddItems(ID id, int numItemsToAdd)
{
   if (numItemsToAdd <= 0)
      return;

   Item * pItem = g_game->dataMgr->GetItemByID(id);
   if (pItem == NULL)
      return;

   bool itemStackExisted = false;
   for (vector<pair<ID,int> >::iterator i = stacks.begin(); i != stacks.end(); ++i)
   {
      if (i->first == id)
      {
         pair<ID,int>& existingStack = *i;
         existingStack.second += numItemsToAdd;
         itemStackExisted = true;
         break;
      }
   }

   if (itemStackExisted)
      return;

   stacks.push_back(make_pair(id,numItemsToAdd));

}

void Items::RemoveItems(ID id, int numItemsToRemove)
{
   if (numItemsToRemove <= 0)
      return;

   Item * pItem = g_game->dataMgr->GetItemByID(id);
   if (pItem == NULL)
      return;

   for (vector<pair<ID,int> >::iterator i = stacks.begin(); i != stacks.end(); ++i)
   {
      if (i->first == id)
      {
         pair<ID,int>& existingStack = *i;
         existingStack.second -= numItemsToRemove;
         if (existingStack.second <= 0)
            stacks.erase(i);
         break;
      }
   }
}

void Items::SetItemCount(ID id, int numItems)
{
   if (numItems < 0)
      return;

   Item * pItem = g_game->dataMgr->GetItemByID(id);
   if (pItem == NULL)
      return;

   bool itemStackExisted = false;
   for (vector<pair<ID,int> >::iterator i = stacks.begin(); i != stacks.end(); ++i)
   {
      if (i->first == id)
      {
         pair<ID,int>& existingStack = *i;
         existingStack.second = numItems;
         itemStackExisted = true;
         if (numItems == 0)
            stacks.erase(i);
         break;
      }
   }

   if (itemStackExisted)
      return;

   stacks.push_back(make_pair(id,numItems));
}


void Items::Get_Item_By_ID(int id, Item& item, int &num_in_stack){
   item.Reset();
   num_in_stack = 0;

   Item * pItem = NULL;
   for (vector<pair<ID,int> >::iterator i = stacks.begin(); i != stacks.end(); ++i){
      if (i->first == id){
         pItem = g_game->dataMgr->GetItemByID(i->first);
		 num_in_stack = i->second;
         break;
      }
   }
   if (pItem == NULL){
      return;
   }
   item = *pItem;
}

void Items::Get_Item_By_Name(std::string name, Item& item, int &num_in_stack){
   item.Reset();
   num_in_stack = 0;

   Item * pItem = new Item();
   for (vector<pair<ID,int> >::iterator i = stacks.begin(); i != stacks.end(); ++i){
         pItem = g_game->dataMgr->GetItemByID(i->first);
		 if(pItem->name == name){
			 num_in_stack = i->second;
			 break;
		 }else{
			pItem = NULL;
		 }
   }
   if (pItem == NULL){
      return;
   }
   item = *pItem;
}


"""
