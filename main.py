from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dummy database
pets_db = [
    {"id": 1, "name": "Jumpy", "price": 50.0, "available": True},
    {"id": 2, "name": "Flexy", "price": 30.0, "available": False},
    {"id": 3, "name": "Bejy", "price": 10.0, "available": True},
]

@app.get("/pet/{pet_name}")
async def get_pet_by_name(pet_name: str):
    for pet in pets_db:
        if pet["name"].lower() == pet_name.lower():
            return pet
    raise HTTPException(status_code=404, detail="Pet not found")

@app.post("/pet")
async def buy_pet(payload: dict):
    pet_name = payload.get("name")
    for pet in pets_db:
        if pet["name"].lower() == pet_name.lower():
            if pet["available"]:
                # Pet is available, mark it as not available and return success message
                pet["available"] = False
                return {"message": f"You have bought the pet: {pet_name}"}
            else:
                # Pet is not available
                raise HTTPException(status_code=400, detail="Pet is not available")
    # Pet not found in the database
    raise HTTPException(status_code=404, detail="Pet not found")