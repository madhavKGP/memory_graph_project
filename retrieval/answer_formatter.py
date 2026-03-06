def print_answers(results):

    for r in results:

        print("\nAnswer")
        print("------")

        print(
            f"{r['subject']} → {r['relation']} → {r['object']}"
        )

        print("\nEvidence")
        print("--------")

        for ev in r["evidence"]:

            print(ev["excerpt"])

        print("\nTimestamp")

        for ev in r["evidence"]:

            print(ev["timestamp"])