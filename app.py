import streamlit as sl
import pandas as pd
from model.model_pip import load_pipeline

##############################################
###### START OF THE STREAMLIT INTERFACE ######
##############################################

def markdown20(text):
    sl.markdown(f"<span style='font-size:20px'>{text}</span>", unsafe_allow_html=True)

sl.title("ImmoEliza")
sl.header("🏠 Real Estate Price Prediction 🏠")

# GENERAL INFORMATIONS
sl.markdown("----")
sl.subheader('ℹ️ General informations')
Type = sl.selectbox("House or appartment?", ["HOUSE", "APPARTMENT"])

if Type == 'APPARTMENT': 
    has_lift = sl.checkbox('Has a lift')
    Subtype = sl.selectbox("Which subtype?", ['APARTMENT', 'FLAT_STUDIO', 'DUPLEX', 'PENTHOUSE','APARTMENT_GROUP', 'GROUND_FLOOR', 'APARTMENT_BLOCK', 
    'MIXED_USE_BUILDING', 'TRIPLEX', 'LOFT','CHALET', 'SERVICE_FLAT', 'KOT', 'BUNGALOW','OTHER_PROPERTY'])

else: 
    has_lift = False
    Subtype = sl.selectbox("Which subtype?", ["HOUSE", "TOWN_HOUSE", "VILLA", "CHALET", "BUNGALOW",
    "COUNTRY_COTTAGE", "MANOR_HOUSE", "MANSION", "EXCEPTIONAL_PROPERTY", "CASTLE", "FARMHOUSE", "HOUSE_GROUP", "OTHER_PROPERTY", "PAVILION"])

BuildingCondition = sl.selectbox("Which condition?", ['GOOD', 'TO_BE_DONE_UP', 'AS_NEW','JUST_RENOVATED','TO_RENOVATE','TO_RESTORE'])
BuildingConstructionYear = sl.number_input(label="Construction year", min_value=1850, max_value=2050, value= 2000)
FacadeCount = sl.number_input(label= "Number of facades", min_value=1, max_value=20)

# GEOGRAPHICAL INFORMATIONS
sl.markdown("----")
sl.subheader("📍 Geographical informations")
Province = sl.selectbox("Province", ['Brussels', 'Luxembourg', 'Antwerp', 'Flemish Brabant',
       'East Flanders', 'West Flanders', 'Liège', 'Walloon Brabant',
       'Limburg', 'Namur', 'Hainaut'])
Locality = sl.text_input("Locality")
Postcode = sl.number_input("Postcode")

# ROOMS
sl.markdown("----")
sl.subheader('🛏️ Rooms')
markdown20('How many bedrooms in your property?')
BedroomCount = sl.slider("Bedrooms", 1, 8, 2)
markdown20('How many bathrooms in your property?')
BathroomCount = sl.slider("Bathrooms", 1, 5, 2)
markdown20('How many toilets in your property?')
ToiletCount = sl.slider("Toilets", 1, 6, 2)
HasDinningRoom = sl.checkbox('Has a dinning room')
HasLivingRoom = sl.checkbox('Has a living room')
HasDressingRoom = sl.checkbox('Has a dressing room')
HasOffice = sl.checkbox('Has an office')
HasAttic = sl.checkbox('Has an attic')
HasBasement = sl.checkbox('Has a basement')
KitchenType = sl.selectbox('What\'s the kitchen type?', ['NOT_INSTALLED', 'SEMI_EQUIPPED', 'INSTALLED', 'HYPER_EQUIPPED'])

# SURFACES
sl.markdown("----")
sl.subheader('📐 Surfaces')
markdown20('What\'s the size of your property?')
HabitableSurface = sl.slider("Habitable surface", 0, 800, 200, step=25)
markdown20('What\'s the land surface?')
LandSurface = sl.slider("Land surface", 0, 2000, 150, step=25)

# EXTERIOR SPACE
sl.markdown("----")
sl.subheader('🌳 Exterior space')
has_terrace = sl.checkbox("Has a terrace")
if has_terrace:
    terrace_area = sl.slider("What's the size of the terrace?", 0, 250, 15, step=5)
    sl.write("Superficie sélectionnée :", terrace_area)
else:
    terrace_area = 0

has_garden = sl.checkbox("Has a garden")
if has_garden:
    garden_area = sl.slider("What's the size of the garden?", 0, 2000, 150, step=25)
    sl.write("Superficie sélectionnée :", garden_area)
else:
    garden_area = 0

has_swimming = sl.checkbox('Has a swimmingpool')
flood_zone = sl.selectbox("There is a kind of flood zone?", ["NON_FLOOD_ZONE", "POSSIBLE_N_CIRCUMSCRIBED_WATERSIDE_ZONE", "CIRCUMSCRIBED_WATERSIDE_ZONE", "POSSIBLE_N_CIRCUMSCRIBED_FLOOD_ZONE", "POSSIBLE_FLOOD_ZONE", "CIRCUMSCRIBED_FLOOD_ZONE", "RECOGNIZED_FLOOD_ZONE", "RECOGNIZED_N_CIRCUMSCRIBED_WATERSIDE_FLOOD_ZONE", "RECOGNIZED_N_CIRCUMSCRIBED_FLOOD_ZONE"])

# ENERGY
sl.markdown("----")
sl.subheader('♻️ Energy')
HasHeatPump = sl.checkbox('Has heat pump')
HasPhotovoltaicPanels = sl.checkbox('Has photovoltaic panels')
HasThermicPanels = sl.checkbox('Has thermic panels')
HasAirConditioning = sl.checkbox('Has air conditionning')
EpcScore = sl.selectbox('What\'s the EPC (PEB) score?', ["A++", "A+", "A", "B", "C", "D", "E", "F", "G"])
HeatingType = sl.selectbox('What\'s the heating type?', ['GAS', 'FUELOIL', 'ELECTRIC', 'PELLET', 'WOOD', 'SOLAR', 'CARBON'])

# EXTRA
sl.markdown("----")
sl.subheader('✨ Extra')
HasFireplace = sl.checkbox('Has a fire place')
HasArmoredDoor = sl.checkbox('Has an armored door')
HasVisiophone = sl.checkbox('Has a visiophone')
ParkingIndoor = sl.slider(label= 'Parking places indoor', min_value=0, max_value=5)
ParkingOutdoor = sl.slider(label= 'Parking places outdoor', min_value=0, max_value=3)

##############
# PREDICTION #
##############
sl.markdown("----")
if sl.button('Prediction'):
    new_house_dict = {
    'Unnamed: 0' : 0, 
    'id' : 0,
    'url' : 'abc',
    'type' : Type,
    'subtype' : Subtype,
    'bedroomCount' : BedroomCount,
    'bathroomCount' : BathroomCount,
    'province' : Province,
    'locality' : Locality,
    'postCode' : Postcode,
    'habitableSurface' : HabitableSurface,
    'roomCount' : 0,
    'monthlyCost' : 0,
    'hasAttic' : HasAttic,
    'hasBasement' : HasBasement,
    'hasDressingRoom' : HasDressingRoom,
    'diningRoomSurface' : 0,
    'hasDiningRoom' : HasDinningRoom,
    'buildingCondition' : BuildingCondition,
    'buildingConstructionYear' : BuildingConstructionYear,
    'facedeCount' : FacadeCount,
    'floorCount' : 0,
    'streetFacadeWidth' : 0,
    'hasLift' : has_lift,
    'floodZoneType' : flood_zone,
    'heatingType' : HeatingType,
    'hasHeatPump' : HasHeatPump,
    'hasPhotovoltaicPanels' : HasPhotovoltaicPanels,
    'hasThermicPanels' : HasThermicPanels,
    'kitchenSurface' : 0,
    'kitchenType' : KitchenType,
    'landSurface' : LandSurface,
    'hasLivingRoom' : HasLivingRoom,
    'livingRoomSurface' : 0,
    'hasBalcony' : 'True', 
    'hasGarden' : has_garden,
    'gardenSurface' : garden_area,
    'gardenOrientation' : "",
    'parkingCountIndoor' : ParkingIndoor,
    'parkingCountOutdoor' : ParkingOutdoor,
    'hasAirConditioning' : HasAirConditioning,
    'hasArmoredDoor' : HasArmoredDoor,
    'hasVisiophone' : HasVisiophone, 
    'hasOffice' : HasOffice,
    'toiletCount' : ToiletCount,
    'hasSwimmingPool' : has_swimming,
    'hasFireplace' : HasFireplace,
    'hasTerrace' : has_terrace,
    'terraceSurface' : terrace_area,
    'terraceOrientation' : '',
    'accessibleDisabledPeople' : False,
    'epcScore' : EpcScore
    }

##############################################
###### CREATE DATAFRAME + LOADING MODEL ######
##############################################
    new_house_df = pd.DataFrame([new_house_dict])

    loaded_pip = load_pipeline(local=False)
    price_prediction = loaded_pip.predict(new_house_df)

    sl.write(f"Le prix prédit est {price_prediction[0]:,.0f} € ± 53 000 €".replace(',', ' '))

