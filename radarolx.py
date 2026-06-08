import requests
import re
import os

# --- AS CHAVES SÃO LIDAS A PARTIR DO AMBIENTE (GITHUB SECRETS) ---
# Se correres localmente, podes definir estas variáveis no teu sistema, 
# mas no GitHub Actions o sistema injeta-as automaticamente.
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

alvos = {
    "O Meu Opel Astra G": "https://www.olx.pt/d/anuncio/opel-astra-g-1-4-16v-nico-dono-IDJr5i2.html",
    "Hyundai Coupe RD1": "https://www.olx.pt/d/anuncio/vendo-hyundai-coup-1-6-de-1997-IDJpCvq.html"
}

# Cabeçalhos para fingir ser um browser real
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def enviar_telegram(mensagem):
    """Envia a mensagem para o teu telemóvel via bot"""
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        print("Erro: Chaves do Telegram em falta!")
        return
        
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    dados = {
        "chat_id": TELEGRAM_CHAT_ID, 
        "text": mensagem, 
        "parse_mode": "Markdown",
        "disable_notification": False 
    }
    try:
        requests.post(url, data=dados)
    except Exception as e:
        print(f"Erro ao enviar para o Telegram: {e}")

def monitorizar():
    relatorio = "📊 *Radar OLX Cloud (GitHub Actions):*\n\n"
    
    for nome, url in alvos.items():
        try:
            # Faz o pedido HTTP
            resposta = requests.get(url, headers=headers)
            html = resposta.text
            
            # Verifica se está ativo
            if "Este anúncio já não se encontra ativo" in html:
                enviar_telegram(f"🚨 *URGENTE*: {nome} foi vendido ou removido!")
                continue
            
            # Procura o número escondido no código fonte
            busca = re.search(r'"page_view_counter":"(\d+)"', html)
            
            if busca:
                cliq = busca.group(1)
                relatorio += f"🟢 {nome}: {cliq} Cliques\n"
            else:
                relatorio += f"⚠️ {nome}: Não foi possível ler cliques.\n"
                
        except Exception as e:
            print(f"Erro ao verificar {nome}: {e}")

    # Envia o relatório final
    enviar_telegram(relatorio)

if __name__ == "__main__":
    monitorizar()