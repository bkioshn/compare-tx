import requests
import os
import time

LCD_URL = os.getenv("LCD_URL", None)
GRAPHQL_URL = os.getenv("GRAPHQL_URL", None)


def get_lcd_transaction(tx_hash):
    while True:
        try:
            result = requests.get(f"{LCD_URL}/cosmos/tx/v1beta1/txs/{tx_hash}")
            return result.json()
        except:
            print(f"LCD error at {tx_hash}")
            time.sleep(10)
            continue

def get_graphql_transaction_by_hash(tx_hash, limit):
    query = f"""
        query {{
            lcd_tx_responses(where: {{hash: {{_eq: "{tx_hash}"}}}}, limit: {limit}) {{
                result
            }}
        }}
    """
    return requests.post(GRAPHQL_URL, json={"query": query})

def get_graphql_transactions(limit, offset):
    query = f"""
        query {{
            lcd_tx_responses(limit: {limit}, offset: {offset}) {{
                result
                hash
            }}
        }}
    """
    return requests.post(GRAPHQL_URL, json={"query": query})


def get_graphql_transactions_count():
    query = f"""
        query {{
            lcd_tx_responses_aggregate {{
                 aggregate {{
                    count
                }}
            }}
        }}
    """
    return requests.post(GRAPHQL_URL, json={"query": query})
