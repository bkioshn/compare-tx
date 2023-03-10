from deepdiff import DeepDiff
from query import (
    get_graphql_transaction_by_hash,
    get_graphql_transactions,
    get_graphql_transactions_count,
    get_lcd_transaction,
)

WINDOW_SIZE = 1000


def compare_all_txs():
    match_file = open("match.txt", "a")
    unmatch_file = open("unmatch.txt", "a")

    max = get_graphql_transactions_count().json()["data"]["lcd_tx_responses_aggregate"][
        "aggregate"
    ]["count"]

    unmatched_hash = []
    matched_hash = 0
    for offset in range(0, max, WINDOW_SIZE):
        tx_graphql = get_graphql_transactions(WINDOW_SIZE, offset).json()["data"][
            "lcd_tx_responses"
        ]

        if not tx_graphql:
            break

        print("Comparing a list of", len(tx_graphql), "txs")

        for j in range(0, len(tx_graphql)):
            tx_graphql_result = tx_graphql[j]["result"]
            tx_graphql_hash = tx_graphql[j]["hash"]

            print(f"Investigate data from GraphQL at hash {tx_graphql_hash}")
            print(f"Comparing hash {tx_graphql_hash} at index {offset + j} / {max}")
            print(f"Fetching data from LCD at hash {tx_graphql_hash}")

            tx_lcd_result = get_lcd_transaction(tx_graphql_hash)
            print(f"Received data from LCD at hash {tx_graphql_hash}")

            ddiff = DeepDiff(tx_graphql_result, tx_lcd_result)
            if not ddiff.to_dict():
                print("Matched")
                matched_hash += matched_hash + 1
                match_file.write(tx_graphql_hash + "\n")

            else:
                print(f"Result in hash {tx_graphql_hash} is not matched")
                unmatched_hash.append(tx_graphql_hash)
                unmatch_file.write(tx_graphql_hash + "\n")

    print(f"Done comparing")
    print(f"Matched {matched_hash} txs")
    print(f"Unmatched {len(unmatched_hash)} txs")
    print(f"Unmatched txs are {unmatched_hash}")


def compare_tx(tx_hash):
    graphql_res = get_graphql_transaction_by_hash(tx_hash, 1)

    graphql_tx_res = graphql_res.json()["data"]["lcd_tx_responses"][0]["result"]
    lcd_tx_res = get_lcd_transaction(tx_hash)

    ddiff = DeepDiff(graphql_tx_res, lcd_tx_res)

    print(tx_hash)
    print(ddiff)
