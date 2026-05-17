from telethon import TelegramClient, events
import requests

# ==============================
# CONFIGURACION
# ==============================
API_ID = 33556386
API_HASH = '1cb5333facf7aa801a7eea1eaf27ff29'
PHONE = '+54355620423'
GROUP_LINK = 'https://t.me/+zal9Bznkv8YwZjMx' 
NTFY_TOPIC = 'senales-ptf-2026'
# ==============================

client = TelegramClient('sesion_bot', API_ID, API_HASH)

async def main():
    await client.start(phone=PHONE)
    print("✅ Bot conectado y escuchando señales...")

    # Obtener la entidad del grupo
    group = await client.get_entity(GROUP_LINK)

    @client.on(events.NewMessage(chats=group))
    async def handler(event):
        mensaje = event.message.message
        if mensaje:
            print(f"📨 Nueva señal recibida: {mensaje}")
            enviar_notificacion(mensaje)

    await client.run_until_disconnected()

def enviar_notificacion(mensaje):
    try:
        requests.post(
            f"https://ntfy.sh/{NTFY_TOPIC}",
            data=mensaje.encode('utf-8', errors='replace'),
            headers={
                "Title": "Nueva Senal PTF",
                "Priority": "high",
                "Tags": "chart_with_upwards_trend",
                "Content-Type": "text/plain; charset=utf-8"
            }
        )
        print("✅ Notificación enviada a tu celular")
    except Exception as e:
        print(f"❌ Error enviando notificación: {e}")

with client:
    client.loop.run_until_complete(main())
