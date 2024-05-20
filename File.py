ib = Fore.RED + r"""

   ____        _      _      _    _ _   _ _ _ _         
  / __ \      (_)    | |    | |  | | | (_) (_) |        
 | |  | |_   _ _  ___| | __ | |  | | |_ _| |_| |_ _   _ 
 | |  | | | | | |/ __| |/ / | |  | | __| | | | __| | | |
 | |__| | |_| | | (__|   <  | |__| | |_| | | | |_| |_| |
  \___\_\\__,_|_|\___|_|\_\  \____/ \__|_|_|_|\__|\__, |
                                                   __/ |
                                                  |___/ 
""" + Style.RESET_ALL
if __name__ == "__main__":
    print(Fore.RED + ib + Style.RESET_ALL)

ppl = f"""
**PayPal Mail:** {paypal_email}
**Link:** {paypal_link}
- Friends & Family Only
- Balance Only
- No Notes
- Send in Euros (€)
 - Follow these terms of service in order to recieve your product.
 - Please provide me with a screenshot of the transaction summary once done.
"""

@bot.command()
async def pp(ctx) -> None:
    await ctx.message.delete()
    await ctx.send(f"{ppl}")

@bot.command()
async def ltc(ctx) -> None:
    await ctx.message.delete()
    await ctx.send(f"{ltc_address}")

@bot.command()
async def purge(ctx, amount: int = 1) -> None:
    await ctx.message.delete()
    deleted_count = 0
    async for message in ctx.channel.history():
        if message.author == bot.user:
            await message.delete()
            deleted_count += 1
        if deleted_count >= amount:
            break

@bot.command()
async def getbal(ctx, ltc_address: str = ltc_address) -> None:
    await ctx.message.delete()
    response = requests.get(f'https://api.blockcypher.com/v1/ltc/main/addrs/{ltc_address}/balance')
    data = response.json()

    balance_ltc = data.get('balance', 0) / 1e8  # Convert from satoshis to LTC
    unconfirmed_balance_ltc = data.get('unconfirmed_balance', 0) / 1e8
    total_received_ltc = data.get('total_received', 0) / 1e8
    total_sent_ltc = data.get('total_sent', 0) / 1e8

    # Get the current LTC to EUR exchange rate
    response = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=litecoin&vs_currencies=eur')
    ltc_to_eur_rate = response.json().get('litecoin', {}).get('eur', 0)

    balance_eur = round(balance_ltc * ltc_to_eur_rate, 2)
    unconfirmed_balance_eur = round(unconfirmed_balance_ltc * ltc_to_eur_rate, 2)
    total_received_eur = round(total_received_ltc * ltc_to_eur_rate, 2)
    total_sent_eur = round(total_sent_ltc * ltc_to_eur_rate, 2)

    await ctx.send(f'**Information for:** {ltc_address}\n'
                   f'**Balance:** {balance_ltc} LTC ({balance_eur} EUR)\n'
                   f'**Unconfirmed Balance:** {unconfirmed_balance_ltc} LTC ({unconfirmed_balance_eur} EUR)\n'
                   f'**Total Sent:** {total_sent_ltc} LTC ({total_sent_eur} EUR)\n'
                   f'**Total Received:** {total_received_ltc} LTC ({total_received_eur} EUR)')

bot.run(token, reconnect=True)
