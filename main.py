import discord
from discord.ext import commands
import requests
from bot_secrets import TOKEN
import random
intents = discord.Intents.default()
intents.message_content = True


bot = commands.Bot(command_prefix='/', intents=intents)

# ID del canal donde quieres que el bot envíe el mensaje
CANAL_EVENTOS_ID = 1553741712596140096  # ← pon aquí el ID real

# Aeropuertos españoles
AEROPUERTOS_ESP = [
    {"nombre": "Madrid-Barajas", "icao": "LEMD"},
    {"nombre": "Barcelona-El Prat", "icao": "LEBL"},
    {"nombre": "Gran Canaria", "icao": "GCLP"},
    {"nombre": "Tenerife Norte", "icao": "GCXO"},
    {"nombre": "Tenerife Sur", "icao": "GCTS"},
    {"nombre": "Málaga-Costa del Sol", "icao": "LEMG"},
    {"nombre": "Bilbao", "icao": "LEBB"},
    {"nombre": "Sevilla", "icao": "LEZL"},
    {"nombre": "Valencia", "icao": "LEVC"},
    {"nombre": "Alicante-Elche", "icao": "LEAL"},
]

@bot.command()
async def evento_espana(ctx):
    # Elegir dos aeropuertos distintos
    origen, destino = random.sample(AEROPUERTOS_ESP, 2)

    mensaje = (
        f"🛫 ¡Hola, pilotos! Hoy os propongo una ruta muy amigable:\n\n"
        f"**{origen['nombre']} ({origen['icao']}) → {destino['nombre']} ({destino['icao']})**\n\n"
        f"Es un vuelo precioso dentro de España, perfecto para disfrutar del paisaje. ¡A despegar!"
    )

    # Enviar al canal específico
    canal_eventos = bot.get_channel(CANAL_EVENTOS_ID)
    if canal_eventos:
        await canal_eventos.send(mensaje)
    else:
        await ctx.send("No pude encontrar el canal de eventos. ¿Está bien el ID?")

    # Responder también en el canal donde se ejecutó el comando
    await ctx.send("Ruta enviada al canal de eventos ✈️")

@bot.event
async def on_ready():
    print(f"Bot conectado como {bot.user}")
bot.run(TOKEN)
