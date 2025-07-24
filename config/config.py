# ===================================
# BOOL
# ===================================
bool_cols = ['hasAttic', 'hasBasement', 'hasLift', 'hasHeatPump', 'hasPhotovoltaicPanels', 'hasThermicPanels', 
             'hasDiningRoom', 'hasVisiophone', 'hasOffice', 'hasSwimmingPool']
conditional_helpers_cols = ['hasLivingRoom', 'hasGarden', 'hasTerrace']
# ===================================
# NUMERICAL
# ===================================
numerical_median_cols = ['bedroomCount', 'bathroomCount', 'habitableSurface', 'toiletCount']
numerical_zero_cols = ['postCode', 'buildingConstructionYear', 'landSurface', 'parkingCountIndoor', 'parkingCountOutdoor']

numerical_conditional_dict = {
    'strategy' : {
        'if_true' : 'median',
        'if_false' : 0,
        'if_missing' : 0
    },
    'columns' : {
        'livingRoomSurface' : 'hasLivingRoom',
        'gardenSurface' : 'hasGarden',
        'terraceSurface' : 'hasTerrace'
    }
}

# ===================================
# CATEGORICAL
# ===================================
one_hot_cols = ['type', 'province']

to_map_cols = {
    'subtype' : {
        'APARTMENT': 1, 'FLAT_STUDIO': 1, 'DUPLEX': 1, 'TRIPLEX': 1,
        'PENTHOUSE': 1, 'LOFT': 1, 'SERVICE_FLAT': 1, 'GROUND_FLOOR': 1,
        'KOT': 1, 'MIXED_USE_BUILDING': 1,
        'HOUSE': 2, 'TOWN_HOUSE': 2, 'VILLA': 2, 'CHALET': 2, 
        'BUNGALOW': 2, 'COUNTRY_COTTAGE': 2,
        'MANOR_HOUSE': 3, 'MANSION': 3, 'EXCEPTIONAL_PROPERTY': 3, 
        'CASTLE': 3, 'FARMHOUSE': 3,
        'APARTMENT_BLOCK': 4, 'APARTMENT_GROUP' : 4, 'HOUSE_GROUP': 4,
        'OTHER_PROPERTY': 5, 'PAVILION': 5
    },
    'buildingCondition' : {
        'TO_RESTORE' : 1, 'TO_RENOVATE' : 2, 'TO_BE_DONE_UP' : 3, 
        'GOOD' : 4, 'JUST_RENOVATED' : 5, 'AS_NEW' : 6
    },
    'floodZoneType' : {
        'RECOGNIZED_N_CIRCUMSCRIBED_FLOOD_ZONE': 1, 'RECOGNIZED_N_CIRCUMSCRIBED_WATERSIDE_FLOOD_ZONE':1, 'RECOGNIZED_FLOOD_ZONE':1, 
        'CIRCUMSCRIBED_FLOOD_ZONE': 2, 'CIRCUMSCRIBED_WATERSIDE_ZONE':2, 
        'POSSIBLE_N_CIRCUMSCRIBED_WATERSIDE_ZONE' : 3, 'POSSIBLE_N_CIRCUMSCRIBED_FLOOD_ZONE':3, 'POSSIBLE_FLOOD_ZONE':3,
        'NON_FLOOD_ZONE': 4
    }, 
    'heatingType' : {
        'GAS' : 1, 
        'FUELOIL' : 2, 
        'ELECTRIC' : 3, 
        'PELLET' : 4, 'WOOD' : 4, 'SOLAR' : 4, 'CARBON' : 4
    }, 
    'kitchenType' : {
        "NOT_INSTALLED": 0, "USA_UNINSTALLED": 0,
        "USA_SEMI_EQUIPPED": 1, "SEMI_EQUIPPED": 1,
        "USA_INSTALLED": 2, "INSTALLED": 2,
        "USA_HYPER_EQUIPPED": 3, "HYPER_EQUIPPED": 3
    }, 
}

epc_config = {
    'wallonia_provinces' : ['Liège', 'Walloon Brabant', 'Namur', 'Hainaut', 'Luxembourg'],
    'flanders_provinces' : ['Antwerp', 'Flemish Brabant', 'East Flanders', 'West Flanders', 'Limburg'],
    'epc_unwanted' : ['C_A', 'F_C', 'G_C', 'D_C', 'F_D', 'E_C', 'G_E', 'E_D', 'C_B', 'X', 'G_F'],
    'mapping' : {
        'wallonia' : {'A++':0, 'A+':30, 'A':65, 'B':125, 'C':200, 'D':300, 'E':375, 'F':450, 'G':510},
        'flanders' : {'A++':0, 'A+':0, 'A':50, 'B':150, 'C':250, 'D':350, 'E':450, 'F':500, 'G':510},
        'brussels' : {'A++':0, 'A+':0, 'A':45, 'B':75, 'C':125, 'D':175, 'E':250, 'F':300, 'G':350}
    } 
}

# ===================================
# TO DROP
# ===================================
to_drop_cols = ['Unnamed: 0', 'id', 'url', 'locality', 'roomCount', 'monthlyCost', 'diningRoomSurface', 
                'facedeCount', 'floorCount', 'streetFacadeWidth', 'hasDressingRoom', 'kitchenSurface',
                'hasBalcony', 'gardenOrientation', 'parkingCountIndoor', 'parkingCountOutdoor', 
                'hasAirConditioning', 'hasArmoredDoor', 'hasFireplace', 'terraceOrientation',
                'accessibleDisabledPeople'] + conditional_helpers_cols