from groq import Groq
from app.config import settings

client = Groq(api_key=settings.GROQ_API_KEY)

print("Fetching available Groq models...\n")

models = client.models.list()

for m in models.data:
    print("-", m.id)
