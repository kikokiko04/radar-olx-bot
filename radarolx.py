import requests
import re
import os

# --- CONFIGURAÇÃO ---
TELEGRAM_TOKEN = "8850082349:AAE2z7yReEdnMZEEF89D4e5CqKdSeOrnDNE"
TELEGRAM_CHAT_ID = "6757240145"

alvos = {
    "O Meu Opel Astra G": "https://www.olx.pt/d/anuncio/opel-astra-g-1-4-16v-nico-dono-IDJr5i2.html",
    "Hyundai Coupe RD1": "https://www.olx.pt/d/anuncio/vendo-hyundai-coup-1-6-de-1997-IDJpCvq.html"
}

# Cabeçalhos para fingir ser um browser real
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def enviar_telegram(mensagem):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    dados = {
        "chat_id": TELEGRAM_CHAT_ID, 
        "text": mensagem, 
        "parse_mode": "Markdown",
        "disable_notification": False 
    }
    requests.post(url, data=dados)

def monitorizar():
    relatorio = "📊 *Radar OLX Cloud:*\n\n"
    
    for nome, url in alvos.items():
        try:
            # Faz o download do código fonte da página
            resposta = requests.get(url, headers=headers)
            html = resposta.text
            
            # Verifica se está ativo
            if "Este anúncio já não se encontra ativo" in html:
                enviar_telegram(f"🚨 *URGENTE*: {nome} foi vendido!")
                continue
            
            # Procura o número usando Regex no código fonte
            # O OLX esconde o número num formato JSON dentro do script da página
            busca = re.search(r'"page_view_counter":"(\d+)"', html)
            
            if busca:
                cliq = busca.group(1)
                relatorio += f"🟢 {nome}: {cliq} Cliques\n"
            else:
                relatorio += f"⚠️ {nome}: Não foi possível ler cliques.\n"
                
        except Exception as e:
            print(f"Erro ao verificar {nome}: {e}")

    enviar_telegram(relatorio)

if __name__ == "__main__":
    monitorizar()