import pandas as pd
import psycopg2

INPUT_FILE = "input.xlsx"
OUTPUT_FILE = "output.xlsx"

DB_CONFIG = {
    "host": "localhost",
    "port": 7777,
    "dbname": "pladias",
    "user": "pladias",
    "password": "pladias"
}

SQL_QUERY_1 = """
SELECT id FROM atlas.records r
JOIN atlas.records_herbariums h ON (h.records_id = r.id)
WHERE
h.herbariums_id = 169 -- Roztoky
AND r.original_id = %s;
"""

SQL_QUERY_2 = """
SELECT r.id FROM atlas.records r
JOIN atlas.records_herbariums h ON (h.records_id = r.id)
JOIN taxons_clear t ON (t.id = r.taxon_id)
JOIN atlas.records_authors rel_aut ON (rel_aut.records_id = r.id)
JOIN atlas.authors a ON (a.id = rel_aut.authors_id)
WHERE
h.herbariums_id = 169 -- Roztoky
AND t.name_lat = %s
AND (
    a.name || ' ' || a.surname = %s
    OR
    r.datum = %s
    );
"""

def safe_trim(value):
    """Převede NaN/None na prázdný řetězec a ořízne mezery."""
    if pd.isna(value):
        return ""
    return str(value).strip()

def main():
    print("📘 Načítám Excel...")
    df = pd.read_excel(INPUT_FILE)

    col1_name = df.columns[0]
    col2_name = df.columns[1]
    col3_name = df.columns[2]
    col4_name = df.columns[3]
    col5_name = df.columns[4]
    col6_name = df.columns[5]

    print("🔌 Připojuji se k databázi...")
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    results_1 = []
    results_2 = []

    print("🚀 Spouštím SQL dotazy pro každý řádek...")
    for index, row in df.iterrows():
        original_id = safe_trim(row[col1_name])
        taxon = safe_trim(row[col2_name])
        collector = safe_trim(row[col3_name])
#         date = safe_trim(row[col4_name])
        date = pd.to_datetime(safe_trim(row[col4_name]), format="%d.%m.%Y", errors='coerce').date()
        country = safe_trim(row[col5_name])
        locality = safe_trim(row[col6_name])

        # Pokud jsou oba sloupce prázdné, přeskočíme
        if not original_id and not val2:
            results_1.append(None)
            results_2.append(None)
            continue
        if country != 'ČR':
            results_1.append(None)
            results_2.append(None)
            continue
         # pokud mají orig id, uvedeme ho
        if original_id:
            cur.execute(SQL_QUERY_1, (original_id,))
            res1 = cur.fetchone()
            results_1.append(res1[0] if res1 else None)
        else:
            results_1.append(None)

        # druhý dotaz
        if taxon and pd.notna(date):
            cur.execute(SQL_QUERY_2, (taxon, collector, date))
            res2 = cur.fetchall()
            if res2:
                links = [f'{r[0]}' for r in res2]
                results_2.append("; ".join(links))
            else:
                results_2.append(None)
        else:
            results_2.append(None)

    df["plná shoda original_id"] = results_1
    df["kandidáti dle dat"] = results_2

    print("💾 Ukládám výsledek do", OUTPUT_FILE)
    df.to_excel(OUTPUT_FILE, index=False)

    cur.close()
    conn.close()
    print("✅ Hotovo!")


if __name__ == "__main__":
    main()
