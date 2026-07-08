"""Starting point for building a real visa-sponsor lookup set.

The Department of Labor publishes H-1B LCA disclosure data quarterly:
https://www.dol.gov/agencies/eta/foreign-labor/performance

Download a recent disclosure CSV, then extract employer names into a set
your app can check against. Rough shape:

    import pandas as pd

    df = pd.read_csv("H-1B_Disclosure_Data.csv")
    employers = set(df["EMPLOYER_NAME"].str.strip().str.lower().unique())

    with open("app/data/known_sponsors.json", "w") as f:
        json.dump(sorted(employers), f)

Then load that JSON in app/routers/scrape.py instead of the empty
KNOWN_SPONSORS placeholder set. Matching by exact employer name is crude --
consider fuzzy matching (rapidfuzz) since job board company names rarely
match DOL's legal entity names exactly.
"""
