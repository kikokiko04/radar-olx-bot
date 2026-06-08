import requests
import re
import os

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

alvos = {
    "O Meu Opel Astra G": "https://www.olx.pt/d/anuncio/opel-astra-g-1-4-16v-nico-dono-IDJr5i2.html",
    "Hyundai Coupe RD1": "https://www.olx.pt/d/anuncio/vendo-hyundai-coup-1-6-de-1997-IDJpCvq.html"
}

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
    "Accept-Language": "pt-PT,pt;q=0.9",
    "Referer": "https://www.google.com/" # Engana o site fingindo que viemos de uma pesquisa
}

def enviar_telegram(mensagem):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": TELEGRAM_CHAT_ID, "text": mensagem, "parse_mode": "Markdown"})

def monitorizar():
    relatorio = "📊 *Radar OLX (Deep Scan Mode):*\n\n"
    
    for nome, url in alvos.items():
        try:
            resposta = requests.get(url, headers=headers)
            html = resposta.text
            
            # Procurar em vários locais possíveis usando uma expressão regular mais flexível
            # O OLX por vezes coloca os dados dentro de um JSON chamado "__initialData__"
            padroes = [r'"viewCount":(\d+)', r'page_view_counter":"(\d+)"', r'view_count":(\d+)']
            
            cliq = None
            for p in padroes:
                busca = re.search(p, html)
                if busca:
                    cliq = busca.group(1)
                    break
            
            if cliq:
                relatorio += f"🟢 {nome}: {cliq} Cliques\n"
            else:
                relatorio += f"⚠️ {nome}: Dados protegidos/ocultos.\n"
                
        except Exception as e:
            print(f"Erro: {e}")

    enviar_telegram(relatorio)

if __name__ == "__main__":
    monitorizar()
