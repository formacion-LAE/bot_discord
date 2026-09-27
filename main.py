import discord
from discord.ext import commands
import requests
import os
import random

TOKEN = os.getenv("TOKEN")  # ← Railway lo leerá de Variables

intents = discord.Intents.default()
intents.message_content = True


bot = commands.Bot(command_prefix='!', intents=intents)

# ID del canal donde quieres que el bot envíe el mensaje
CANAL_EVENTOS_ID = 1287516263760924754  # ← pon aquí el ID real

# Aeropuertos españoles
AEROPUERTOS_ESP = [
    {"nombre": "A Coruña", "icao": "LECO"},
    {"nombre": "Alicante-Elche", "icao": "LEAL"},
    {"nombre": "Almería", "icao": "LEAM"},
    {"nombre": "Asturias", "icao": "LEAS"},
    {"nombre": "Badajoz", "icao": "LEBZ"},
    {"nombre": "Barcelona-El Prat", "icao": "LEBL"},
    {"nombre": "Bilbao", "icao": "LEBB"},
    {"nombre": "Burgos", "icao": "LEBG"},
    {"nombre": "Córdoba", "icao": "LEBA"},
    {"nombre": "Cuatro Vientos (Madrid)", "icao": "LECU"},
    {"nombre": "Fuerteventura", "icao": "GCFV"},
    {"nombre": "Girona-Costa Brava", "icao": "LEGE"},
    {"nombre": "Gran Canaria", "icao": "GCLP"},
    {"nombre": "Granada-Jaén", "icao": "LEGR"},
    {"nombre": "Huesca-Pirineos", "icao": "LEHC"},
    {"nombre": "Ibiza", "icao": "LEIB"},
    {"nombre": "Jerez", "icao": "LEJR"},
    {"nombre": "La Gomera", "icao": "GCGM"},
    {"nombre": "La Palma", "icao": "GCLA"},
    {"nombre": "Lanzarote", "icao": "GCRR"},
    {"nombre": "León", "icao": "LELN"},
    {"nombre": "Logroño-Agoncillo", "icao": "LELO"},
    {"nombre": "Madrid-Barajas Adolfo Suárez", "icao": "LEMD"},
    {"nombre": "Málaga-Costa del Sol", "icao": "LEMG"},
    {"nombre": "Melilla", "icao": "GEML"},
    {"nombre": "Menorca", "icao": "LEMH"},
    {"nombre": "Murcia-San Javier", "icao": "LELC"},
    {"nombre": "Palma de Mallorca", "icao": "LEPA"},
    {"nombre": "Pamplona", "icao": "LEPP"},
    {"nombre": "Reus", "icao": "LERS"},
    {"nombre": "Sabadell", "icao": "LELL"},
    {"nombre": "Salamanca-Matacán", "icao": "LESA"},
    {"nombre": "San Sebastián", "icao": "LESO"},
    {"nombre": "Santander-Seve Ballesteros", "icao": "LEXJ"},
    {"nombre": "Santiago de Compostela", "icao": "LEST"},
    {"nombre": "Sevilla", "icao": "LEZL"},
    {"nombre": "Tenerife Norte", "icao": "GCXO"},
    {"nombre": "Tenerife Sur", "icao": "GCTS"},
    {"nombre": "Valencia", "icao": "LEVC"},
    {"nombre": "Valladolid", "icao": "LEVD"},
    {"nombre": "Vigo", "icao": "LEVX"},
    {"nombre": "Vitoria", "icao": "LEVT"},
    {"nombre": "Zaragoza", "icao": "LEZG"}
]

@bot.command()
async def vuelo_españa(ctx):
    # Elegir dos aeropuertos distintos
    origen, destino = random.sample(AEROPUERTOS_ESP, 2)

    mensaje = (
        f"🛫 ¡Hola, <@&{1278475063707963503}>! Os propongo una ruta muy amigable por si no tenéis idea de qué volar 😉:\n\n"
        f"**{origen['nombre']} ({origen['icao']}) → {destino['nombre']} ({destino['icao']})**\n\n"
        f"Es un vuelo precioso dentro de España, perfecto para disfrutar del paisaje. **¡A despegar!**"
    )

    # Enviar al canal específico
    canal_eventos = bot.get_channel(CANAL_EVENTOS_ID)
    if canal_eventos:
        await canal_eventos.send(mensaje)
    else:
        await ctx.send("No pude encontrar el canal de eventos. ¿Está bien el ID?")

    # Responder también en el canal donde se ejecutó el comando
    await ctx.send("Ruta enviada al canal de eventos ✈️")

@bot.command()
async def evento_programado(ctx):
    origen, destino = random.sample(AEROPUERTOS_ESP, 2)

    nombre_evento = f"Vuelo grupal: {origen['icao']} → {destino['icao']}"
    descripcion_evento = (
        f"🛫 ¡Hola pilotos! Os propongo un vuelo grupal muy amigable:\n\n"
        f"**{origen['nombre']} ({origen['icao']}) → {destino['nombre']} ({destino['icao']})**\n\n"
        f"Será un vuelo precioso dentro de España. ¡Os esperamos!"
    )

    from datetime import datetime, timedelta, UTC
    inicio = datetime.now(UTC) + timedelta(days=2)
    fin = inicio + timedelta(hours=2)

    try:
        evento = await ctx.guild.create_scheduled_event(
            name=nombre_evento,
            description=descripcion_evento,
            start_time=inicio,
            end_time=fin,
            entity_type=discord.EntityType.external,
            location=f"{origen['icao']} → {destino['icao']}",
            privacy_level=discord.PrivacyLevel.guild_only
        )

        await ctx.send(f"Evento creado correctamente ✈️\nNombre: **{nombre_evento}**\nFecha: {inicio}")

    except Exception as e:
        await ctx.send(f"Hubo un error creando el evento: {e}")

@bot.command()
async def aip(ctx, pais: str):
    pais = pais.upper()

    aips = {
        "ES": "https://aip.enaire.es/AIP/AIP-es.html",
        "FR": "https://www.sia.aviation-civile.gouv.fr",
        "DE": "https://aip.dfs.de/basicAIP/",
        "UK": "https://www.nats.aero/ais",
        "IT": "https://www.enav.it/en/our-services/ais",
        "PT": "https://ais.nav.pt/wp-content/uploads/AIS_Files/eAIP_Current/eAIP_Online/eAIP/html/index.html",
        "NL": "https://eaip.lvnl.nl/web/eaip/default.html",
        "BE": "https://ops.skeyes.be/html/belgocontrol_static/eaip/eAIP_Main/html/index-en-GB.html",
        "CH": "https://www.skyguide.ch/en/services/ais",
        "AT": "https://eaip.austrocontrol.at",
        "NO": "https://www.avinor.no/en/ais",
        "SE": "https://www.lfv.se/en/ais",
        "FI": "https://ais.fi",
        "GR": "https://www.hcaa.gr/en/flight-information/ais",
        "TR": "https://www.dhmi.gov.tr/Sayfalar/aipturkey.aspx"
    }

    if pais not in aips:
        await ctx.send("País no soportado. Usa ES, FR, DE, UK, IT, PT, NL, BE, CH, AT, NO, SE, FI, GR o TR.")
        return

    await ctx.send(f"📘 **AIP de {pais}:**\n{aips[pais]}")

@bot.command()
@commands.has_role("Staff")  # Nombre EXACTO del rol
async def clear(ctx, cantidad: int):
    if cantidad < 1:
        await ctx.send("Debes indicar un número válido de mensajes a borrar.")
        return

    await ctx.channel.purge(limit=cantidad + 1)
    await ctx.send(f"🧹 Se han borrado {cantidad} mensajes.", delete_after=5)


@bot.command()
async def metar(ctx, icao: str):
    import xml.etree.ElementTree as ET

    icao = icao.upper()
    url = f"https://aviationweather.gov/api/data/metar?ids={icao}&format=xml"

    try:
        response = requests.get(url)
        xml_data = response.text

        # Parsear XML
        root = ET.fromstring(xml_data)

        metar = root.find(".//raw_text")

        if metar is not None:
            metar_texto = metar.text
            await ctx.send(f"📡 METAR de **{icao}**:\n```\n{metar_texto}\n```")
        else:
            await ctx.send(f"No pude obtener el METAR de {icao}. Puede que NOAA no tenga datos ahora mismo.")

    except Exception as e:
        await ctx.send(f"Hubo un error obteniendo el METAR: {e}")


@bot.event
async def on_ready():
    print(f"Bot conectado como {bot.user}")
bot.run(TOKEN)
