import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

import config
import livepix
import database as db

# Configuração de logs para ver erros no CMD
logging.basicConfig(level=logging.INFO)

# Inicialização do Bot
bot = Bot(token=config.TOKEN_TELEGRAM)
dp = Dispatcher()

# --- MENU PRINCIPAL (BOTÕES DE BAIXO) ---
menu_principal = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text=f"💎 Entrar no grupo VIP — R$ {config.PRECO_VIP}")],
    [KeyboardButton(text=f"🎬 Pedir vídeo personalizado — R$ {config.PRECO_VIDEO}")]
], resize_keyboard=True)

# --- COMANDO /START ---
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    texto_boas_vendas = (
        "👋 Olá, aqui é o Pedro Pugliese!\n\n"
        "Você pode entrar no meu grupo VIP ou pedir um vídeo personalizado. "
        "Escolha uma das opções abaixo ⬇️"
    )
    await message.answer(texto_boas_vendas, reply_markup=menu_principal)

# --- OPÇÃO: GRUPO VIP ---
@dp.message(F.text.contains("VIP"))
async def comprar_vip(message: types.Message):
    await message.answer("⏳ Gerando seu link de pagamento exclusivo...")
    
    # Chama a API do LivePix para gerar o link com valor travado
    link = await livepix.gerar_link_livepix(config.PRECO_VIP)
    
    if link:
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Pagar R$ 24,99 no Pix 💳", url=link)]
        ])
        texto_vip = (
            "💎 **Meu Grupo VIP**\n\n"
            f"Clique no botão abaixo para pagar R$ {config.PRECO_VIP}.\n\n"
            "💰 Após realizar o pagamento, **envie o comprovante aqui**. "
            "Vou analisar e em poucos minutos você terá o acesso ✅"
        )
        await message.answer(texto_vip, reply_markup=kb)
    else:
        await message.answer("❌ Erro ao gerar link de pagamento. Tente novamente em instantes.")

# --- OPÇÃO: VÍDEO PERSONALIZADO ---
@dp.message(F.text.contains("vídeo"))
async def comprar_video(message: types.Message):
    await message.answer("⏳ Gerando seu link de pagamento exclusivo...")
    
    # Chama a API do LivePix
    link = await livepix.gerar_link_livepix(config.PRECO_VIDEO)
    
    if link:
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Pagar R$ 100,00 no Pix 💳", url=link)]
        ])
        texto_video = (
            "🎬 **Vídeo Personalizado**\n\n"
            f"Clique no botão abaixo para pagar R$ {config.PRECO_VIDEO}.\n\n"
            "💰 Após pagar, envie o comprovante e as **instruções do vídeo** aqui na legenda. "
            "Vou analisar e começar a produzir seu vídeo em breve 🎬"
        )
        await message.answer(texto_video, reply_markup=kb)
    else:
        await message.answer("❌ Erro ao gerar link de pagamento. Tente novamente.")

# --- RECEBIMENTO DE COMPROVANTE (FOTO) ---
@dp.message(F.photo)
async def receber_comprovante(message: types.Message):
    # Salva no banco de dados simples
    db.salvar_pedido(message.from_user.id, "Pendente")
    
    # Responde ao usuário
    await message.answer("✅ Recebi seu comprovante! Já estou analisando. Em breve te mando uma resposta por aqui.")
    
    # Envia para você (Admin) para aprovação manual
    legenda_admin = (
        "🚨 **Novo Comprovante Recebido!**\n\n"
        f"👤 Usuário: @{message.from_user.username or 'Sem Username'}\n"
        f"🆔 ID: `{message.from_user.id}`\n"
        f"📝 Legenda: {message.caption or 'Sem instruções'}"
    )
    await bot.send_photo(config.ADMIN_ID, message.photo[-1].file_id, caption=legenda_admin)

# --- FUNÇÃO PARA RODAR O BOT ---
async def main():
    db.init_db() # Cria o arquivo .db se não existir
    print("-------------------------------")
    print("🚀 Bot Pedro Pugliese ONLINE!")
    print("-------------------------------")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Bot desligado.")