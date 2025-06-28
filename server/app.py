#import required libraries
from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import numpy as np
import joblib
from sklearn.preprocessing import OrdinalEncoder


# Initialize the FastAPI app
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#Load the pre-trained model
loaded_model = joblib.load('./model/saved_models/linear_regression_model.pkl')

#check if the model is loaded successfully

if loaded_model:
    print("Model loaded successfully")  
else:
    print("Failed to load the model")

possible_fuel_types = ['X', 'Z', 'D', 'E', 'N']

possible_models = [
        '1.6EL', '3.2TL', '3.5RL', 'INTEGRA', 'INTEGRA GSR/TYPE R', 'NSX',
        'A4', 'A4 QUATTRO', 'A6', 'A6 AVANT QUATTRO', 'A6 QUATTRO',
        'A8 QUATTRO', 'S4 QUATTRO', 'TT COUPE QUATTRO',
        'TT COUPE QUATTRO (SUPERCHARGED)', 'TT ROADSTER',
        'TT ROADSTER QUATTRO (SUPERCHARGED)', '323 CONVERTIBLE', '323Ci',
        '323i', '328Ci', '328i', '528i', '528i TOURING', '540i',
        '540i TOURING', '740i', '740iL', '750iL', 'M COUPE', 'M ROADSTER',
        'M5', 'X5', 'Z3', 'Z8', 'CENTURY', 'LESABRE', 'PARK AVENUE',
        'PARK AVENUE #', 'REGAL', 'REGAL #', 'CATERA', 'DEVILLE',
        'ELDORADO', 'ESCALADE 4X4', 'SEVILLE', 'ASTRO AWD CARGO',
        'ASTRO AWD PASSENGER', 'ASTRO CARGO', 'ASTRO PASSENGER', 'BLAZER',
        'BLAZER 4X4', 'C1500 SILVERADO', 'C2500 SILVERADO', 'CAMARO',
        'CAVALIER', 'CAVALIER BIFUEL', 'CORVETTE', 'G15/G25 CHEVY VAN',
        'G1500/G2500 CHEVY EXPRESS', 'IMPALA', 'K1500 SILVERADO 4X4',
        'K1500 TAHOE 4X4', 'LUMINA/MONTE CARLO', 'MALIBU', 'METRO',
        'NEW C1500 SUBURBAN', 'NEW C1500 TAHOE', 'NEW K1500 TAHOE 4X4',
        'S10', 'S10 4X4', 'TRACKER 4X4', 'TRACKER CONVERTIBLE 4X4',
        'VENTURE', '300M', 'CIRRUS', 'CONCORDE', 'INTREPID', 'LHS', 'NEON',
        'PT CRUISER', 'SEBRING', 'SEBRING CONVERTIBLE', 'TOWN & COUNTRY',
        'TOWN & COUNTRY AWD', 'LANOS', 'LEGANZA', 'NUBIRA', 'NUBIRA WAGON',
        'CARAVAN', 'CARAVAN FFV', 'DAKOTA', 'DAKOTA 4X4', 'DURANGO 4X4',
        'DURANGO 5.9 R/T 4X4', 'GRAND CARAVAN', 'GRAND CARAVAN AWD',
        'GRAND CARAVAN FFV', 'RAM 1500', 'RAM 1500 4X4', 'RAM 1500 VAN',
        'RAM 1500 WAGON', 'RAM 2500 VAN', 'RAM 2500 VAN NGV',
        'RAM 2500 WAGON', 'VIPER GTS', 'VIPER RT/10', '360 MODENA F1',
        '456 MGT', '456 MGTA', '550 MARANELLO', 'COUGAR', 'CROWN VICTORIA',
        'E150 CLUB WAGON', 'E150 VAN', 'E250 VAN', 'ESCORT ZX2',
        'EXPEDITION', 'EXPEDITION 4X4', 'EXPLORER', 'EXPLORER 4X4',
        'EXPLORER OHV', 'EXPLORER OHV 4X4', 'EXPLORER SOHC',
        'EXPLORER SOHC 4X4', 'F150', 'F150 4X4', 'FOCUS SEDAN',
        'FOCUS WAGON', 'GRAND MARQUIS', 'MUSTANG', 'MUSTANG #', 'RANGER',
        'RANGER 4X4', 'TAURUS', 'TAURUS #', 'TAURUS WAGON',
        'TAURUS WAGON #', 'WINDSTAR VAN', 'WINDSTAR WAGON', 'C1500 SIERRA',
        'C1500 YUKON', 'C1500 YUKON XL', 'C2500 SIERRA',
        'G15/G25 SAVANA CARGO', 'G1500/G2500 SAVANA PASSENGER', 'JIMMY',
        'JIMMY 4X4', 'K1500 SIERRA 4X4', 'K1500 YUKON 4X4', 'SAFARI CARGO',
        'SAFARI CARGO AWD', 'SAFARI PASSENGER', 'SAFARI PASSENGER AWD',
        'SONOMA', 'SONOMA 4X4', 'ACCORD', 'ACCORD DX', 'ACCORD EX/LX',
        'CIVIC COUPE Si', 'CIVIC COUPE SiR', 'CIVIC CX/DX/LX/EX', 'CR-V',
        'INSIGHT', 'ODYSSEY', 'PRELUDE', 'S2000', 'ACCENT', 'ELANTRA',
        'ELANTRA WAGON', 'SONATA 2.4L', 'SONATA 2.5L', 'TIBURON', 'G20',
        'I30', 'QX4 4X4', 'HOMBRE', 'HOMBRE 4X4', 'RODEO 4X4',
        'TROOPER 4X4', 'S-TYPE V6', 'S-TYPE V8', 'VANDEN PLAS',
        'VANDEN PLAS SUPERCHARGED', 'XJ8', 'XJR #', 'XK8',
        'XK8 CONVERTIBLE', 'XKR #', 'XKR CONVERTIBLE #', 'CHEROKEE 4X4',
        'GRAND CHEROKEE 4X4', 'TJ 4X4', 'SEPHIA', 'SPORTAGE 4X4',
        'DISCOVERY SERIES II 4X4', 'RANGE ROVER 4X4', 'ES 300', 'GS 300',
        'GS 400', 'LS 400', 'LX 470', 'RX 300', 'RX 300 4X4',
        'CONTINENTAL', 'LS', 'NAVIGATOR 4X4', 'TOWN CAR', '626', 'B3000',
        'B4000', 'B4000 4X4', 'MILLENIA', 'MILLENIA #', 'MPV',
        'MX-5 MIATA', 'PROTEGE', 'C 230 KOMPRESSOR #', 'C 280', 'C 43 AMG',
        'CLK 320', 'CLK 320 CABRIOLET', 'CLK 430', 'CLK 430 CABRIOLET',
        'E 320', 'E 320 4MATIC', 'E 320 4MATIC WAGON', 'E 320 WAGON',
        'E 430', 'E 430 4MATIC', 'E 55 AMG', 'ML 320', 'ML 430', 'S 430',
        'S 500', 'SL 500', 'SL 600', 'SLK 230 KOMPRESSOR #', 'ALTIMA',
        'FRONTIER', 'FRONTIER 4X4', 'FRONTIER V6', 'FRONTIER V6 4X4',
        'MAXIMA', 'PATHFINDER 4X4', 'QUEST', 'XTERRA', 'XTERRA V6',
        'XTERRA V6 4X4', 'ALERO', 'INTRIGUE', 'SILHOUETTE', 'PROWLER',
        'BONNEVILLE', 'BONNEVILLE #', 'FIREBIRD/FORMULA', 'FIREFLY',
        'GRAND AM', 'GRAND PRIX', 'GRAND PRIX #', 'MONTANA', 'SUNFIRE',
        '911 CARRERA', '911 CARRERA 4', 'BOXSTER', 'BOXSTER S',
        '9-3 TURBO', '9-5 TURBO', '9-5 WAGON TURBO', 'LW WAGON', 'SC',
        'SC #', 'SL', 'SL #', 'SW WAGON #', 'FORESTER AWD', 'IMPREZA AWD',
        'IMPREZA WAGON AWD', 'LEGACY AWD', 'LEGACY WAGON AWD', 'ESTEEM',
        'ESTEEM WAGON', 'GRAND VITARA 4X4', 'SWIFT', 'VITARA 4X4',
        'VITARA CONVERTIBLE 4X4', '4RUNNER 4X4', 'AVALON', 'CAMRY',
        'CAMRY SOLARA', 'CAMRY SOLARA CONVERTIBLE', 'CELICA', 'COROLLA',
        'ECHO', 'RAV4', 'RAV4 4X4', 'RAV4 SOFT TOP', 'RAV4 SOFT TOP 4X4',
        'SIENNA', 'TACOMA', 'TACOMA 4X4', 'TUNDRA', 'TUNDRA 4X4', 'CABRIO',
        'EUROVAN', 'EUROVAN CAMPER', 'GOLF', 'GOLF TDI DIESEL', 'GTI',
        'JETTA', 'JETTA TDI DIESEL', 'NEW BEETLE', 'NEW BEETLE TDI DIESEL',
        'PASSAT', 'PASSAT WAGON', 'C70 CONVERTIBLE TURBO', 'C70 TURBO',
        'S70', 'S70 AWD TURBO', 'S70 GLT TURBO', 'S70 T5 TURBO', 'S80 2.9',
        'S80 T-6', 'V70', 'V70 AWD TURBO', 'V70 GLT TURBO', 'V70 T5 TURBO',
        'V70R AWD TURBO'
       ];

@app.get('/check_model')

async def check_model():
    """
    Endpoint to check if the model is loaded successfully.
    """
    if loaded_model:
        return {"status": "Model loaded successfully"}
    else:
        return {"status": "Failed to load the model"}

# @app.get('/get_models')
# def get_models():
#     models = loaded_model



#initialize the predict endpoint
@app.post('/predict_fuel_consumption')
async def predict_fuel_consumption(
    emissions: float = Form(...),
    fuelType: str =  Form(...),
    engineSize: float = Form(...),
    model: str = Form(...)
):
    """
    Endpoint to make predictions using the pre-trained model.
    """
    # Fit the ordinalEncoder on possible fuel types (replace with your actual categories if known)
    oe_Fuel_type = OrdinalEncoder()
    oe_Fuel_type.fit([[ft] for ft in possible_fuel_types])
    encoded_fuel_type = oe_Fuel_type.transform([[fuelType]])[0][0]
    print(f"Encoded fuel type: {fuelType} -> {encoded_fuel_type}")
    
    # Fit the ordinalEncoder on possible model types (replace with your actual categories if known)
    
    # Replace with your actual model categories
    oe_model = OrdinalEncoder()
    oe_model.fit([[m] for m in possible_models])
    encoded_model = oe_model.transform([[model]])[0][0]
    print(f"Encoded model: {model} -> {encoded_model}")
    
    # Prepare the input data as a numpy array
    input_data = np.array([[emissions, encoded_fuel_type, engineSize, encoded_model]])
    
    # Make prediction using the model
    prediction = loaded_model.predict(input_data)
    
    # Return the prediction result
    return {"prediction": float(np.round(prediction[0], 3)),
            "input_data": input_data.tolist()}

#check the unicorn server is running   
if __name__ == '__main__':

    uvicorn.run(app, host='127.0.0.1', port=8002)