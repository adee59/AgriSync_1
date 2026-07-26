import asyncio
import json
import motor.motor_asyncio
from gmqtt import Client as MQTTClient

MONGO_URI = "mongodb://admin:password123@localhost:27017/"
MQTT_HOST = "localhost"

class AgriSyncProfessional:
    def __init__(self):
        self.db_client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
        self.db = self.db_client.agrisync_records
        self.mqtt = MQTTClient("Orchestrator")
        self.state = {"soil": None, "weather": None}

    async def on_message(self, client, topic, payload, qos, properties):
        data = json.loads(payload.decode())
        if topic == "agrisync/soil":
            self.state["soil"] = data['value']
        elif topic == "agrisync/weather":
            self.state["weather"] = data['value']
        
        await self.process_logic()

    async def process_logic(self):
        soil = self.state["soil"]
        weather = self.state["weather"]

        if soil is not None and weather is not None:
            decision = "IDLE"
            reason = "Optimal moisture levels maintained."

            if soil < 30 and weather < 70:
                decision = "ACTIVATE_IRRIGATION"
                reason = "Soil moisture critical (<30%). Low rain probability."
            elif soil < 30 and weather >= 70:
                decision = "DEFER_IRRIGATION"
                reason = "Soil dry, but rain probability high (>=70%)."

            await self.db.logs.insert_one({
                "decision": decision,
                "reason": reason,
                "context": self.state.copy()
            })
            print(f"--> Logged Decision: {decision} | Reason: {reason}")

    async def run(self):
        self.mqtt.on_message = self.on_message
        await self.mqtt.connect(MQTT_HOST)
        self.mqtt.subscribe("agrisync/#")
        print("?? AgriSync Orchestrator Online. Listening for Agent telemetry...")
        while True:
            await asyncio.sleep(1)

if __name__ == "__main__":
    core = AgriSyncProfessional()
    asyncio.run(core.run())
