import asyncio
import json
import random
from gmqtt import Client as MQTTClient

async def simulate_agents():
    client = MQTTClient("IoT_Simulator")
    await client.connect("localhost")
    print("?? Field Telemetry Simulator active...")
    
    while True:
        soil_val = random.randint(15, 45)
        weather_val = random.randint(10, 90)

        client.publish("agrisync/soil", json.dumps({"value": soil_val}))
        client.publish("agrisync/weather", json.dumps({"value": weather_val}))
        
        print(f"[Telemetry] Sent -> Soil: {soil_val}%, Rain Prob: {weather_val}%")
        await asyncio.sleep(3)

if __name__ == "__main__":
    asyncio.run(simulate_agents())
