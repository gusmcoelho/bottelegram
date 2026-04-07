import httpx
import config

async def gerar_link_livepix(valor):
    url_auth = "https://oauth.livepix.gg/oauth2/token"
    url_charge = "https://api.livepix.gg/v2/payments"
    
    async with httpx.AsyncClient() as client:
        # 1. Autenticação (OAuth2)
        auth_data = {
            "grant_type": "client_credentials",
            "client_id": config.LIVEPIX_CLIENT_ID,
            "client_secret": config.LIVEPIX_CLIENT_SECRET,
            "scope": config.LIVEPIX_SCOPE
        }
        
        auth_res = await client.post(url_auth, data=auth_data)
        if auth_res.status_code != 200:
            print(f"❌ Erro na Autenticação: {auth_res.text}")
            return None
            
        token = auth_res.json().get('access_token')
        
        # 2. Criar a cobrança (Agora com redirectUrl obrigatório)
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "amount": int(valor * 100), # Centavos
            "currency": "BRL",
            "redirectUrl": "https://t.me/pedropugliesebot" # URL para onde o cliente volta após pagar
        }
        
        charge_res = await client.post(url_charge, json=payload, headers=headers)
        
        if charge_res.status_code == 201:
            # O link correto está em data -> redirectUrl
            return charge_res.json()['data']['redirectUrl']
        else:
            print(f"❌ Erro na API LivePix: {charge_res.text}")
            return None