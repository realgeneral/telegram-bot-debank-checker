from app.utils.utils import edit_session_headers, send_request


class Checker:

    @staticmethod
    async def chain_balance(node_process, session, address, chain, ticker, min_amount):
        coins = []

        payload = {
            'user_addr': address,
            'chain': chain
        }
        await edit_session_headers(node_process, session, payload, 'GET', '/token/balance_list')

        resp = await send_request(
            node_process,
            session=session,
            method='GET',
            url=f'https://api.debank.com/token/balance_list?user_addr={address}&chain={chain}',
        )

        if resp == -1:
            return -1

        for coin in resp.json()['data']:
            if (ticker == None or coin['optimized_symbol'] == ticker):
                coin_in_usd = '?' if (coin["price"] is None) else coin["amount"] * coin["price"]
                if (type(coin_in_usd) is str or (type(coin_in_usd) is float and coin_in_usd > min_amount)):
                    coins.append({
                        'amount': coin['amount'],
                        'name': coin['name'],
                        'ticker': coin['optimized_symbol'],
                        'price': coin['price'],
                        'logo_url': coin['logo_url']
                    })

        return coins

    @staticmethod
    async def get_used_chains(node_process, session, address):
        payload = {
            'id': address,
        }

        await edit_session_headers(node_process, session, payload, 'GET', '/user/used_chains')

        resp = await send_request(
            node_process,
            session=session,
            method='GET',
            url=f'https://api.debank.com/user/used_chains?id={address}',
        )

        if resp == -1:
            return -1

        chains = resp.json()['data']['chains']

        return chains

    @staticmethod
    async def get_usd_balance(node_process, session, wallets):
        payload = {
            'user_addr': wallets,
        }
        await edit_session_headers(node_process, session, payload, 'GET', '/asset/net_curve_24h')

        resp = await send_request(
            node_process,
            session=session,
            method='GET',
            url=f'https://api.debank.com/asset/net_curve_24h?user_addr={wallets}',
        )

        if resp == -1:
            return -1

        usd_value = resp.json()['data']['usd_value_list'][-1][1]
        return usd_value
