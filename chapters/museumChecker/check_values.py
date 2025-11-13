import pandas as pd
import psycopg2
import re

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
AND r.original_id IS NULL
AND t.name_lat = %s
AND (
    a.name || ' ' || a.surname = %s
    AND
    r.datum = %s
    AND
    r.locality LIKE %s
    );
"""

SQL_QUERY_3 = """
SELECT r.id FROM atlas.records r
JOIN atlas.records_herbariums h ON (h.records_id = r.id)
JOIN taxons_clear t ON (t.id = r.taxon_id)
JOIN atlas.records_authors rel_aut ON (rel_aut.records_id = r.id)
JOIN atlas.authors a ON (a.id = rel_aut.authors_id)
WHERE
h.herbariums_id = 169 -- Roztoky
AND r.original_id IS NULL
AND t.name_lat = %s
AND r.datum = %s
AND (
        a.name || ' ' || a.surname = %s
        OR
        r.locality LIKE %s
        );
"""

SQL_QUERY_4 = """
SELECT r.id FROM atlas.records r
JOIN atlas.records_herbariums h ON (h.records_id = r.id)
JOIN taxons_clear t ON (t.id = r.taxon_id)
JOIN atlas.records_authors rel_aut ON (rel_aut.records_id = r.id)
JOIN atlas.authors a ON (a.id = rel_aut.authors_id)
WHERE
h.herbariums_id = 169 -- Roztoky
AND r.original_id IS NULL
AND t.name_lat = %s
AND (r.datum = %s
        OR
        a.name || ' ' || a.surname = %s
        OR
        r.locality LIKE %s
        );
"""

SQL_QUERY_5 = """
SELECT r.id FROM atlas.records r
JOIN atlas.records_herbariums h ON (h.records_id = r.id)
JOIN taxons_clear t ON (t.id = r.taxon_id)
JOIN atlas.records_authors rel_aut ON (rel_aut.records_id = r.id)
JOIN atlas.authors a ON (a.id = rel_aut.authors_id)
WHERE
h.herbariums_id = 169 -- Roztoky
AND r.original_id IS NULL
AND t.name_lat = %s
AND r.locality LIKE %s
AND (r.datum = %s
        OR
        a.name || ' ' || a.surname = %s
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
    results_3 = []
    results_4 = []
    results_5 = []

    print("🚀 Spouštím SQL dotazy pro každý řádek...")
    for index, row in df.iterrows():
        original_id = safe_trim(row[col1_name])
        converted_id = re.sub(r"^B\s+", "ROZ_", original_id)
        taxon = safe_trim(row[col2_name])
        collector = safe_trim(row[col3_name])
#         date = safe_trim(row[col4_name])
        date = pd.to_datetime(safe_trim(row[col4_name]), format="%d.%m.%Y", errors='coerce').date()
        country = safe_trim(row[col5_name])
        locality = '%' + safe_trim(row[col6_name]) + '%'

        # Pokud jsou oba sloupce prázdné, přeskočíme
        if not original_id and not val2:
            results_1.append(None)
            results_2.append(None)
            results_3.append(None)
            results_4.append(None)
            results_5.append(None)
            continue
        if country != 'ČR':
            results_1.append(None)
            results_2.append(None)
            results_3.append(None)
            results_4.append(None)
            results_5.append(None)
            continue
         # pokud mají orig id, uvedeme ho
        if original_id:
            cur.execute(SQL_QUERY_1, (converted_id,))
            res1 = cur.fetchone()
            results_1.append(res1[0] if res1 else None)
        else:
            results_1.append(None)

        # druhý dotaz
        if taxon and pd.notna(date):
            cur.execute(SQL_QUERY_2, (taxon, collector, date, locality))
            res2 = cur.fetchall()
            if res2:
                links = [f'{r[0]}' for r in res2]
                results_2.append("; ".join(links))
            else:
                results_2.append(None)
        else:
            results_2.append(None)

        # třetí dotaz
        if taxon and pd.notna(date):
            cur.execute(SQL_QUERY_3, (taxon, date,collector,  locality))
            res3 = cur.fetchall()
            if res3:
                links = [f'{r[0]}' for r in res3]
                results_3.append("; ".join(links))
            else:
                results_3.append(None)
        else:
            results_3.append(None)

        # čtvrtý dotaz
        if taxon and pd.notna(date):
            cur.execute(SQL_QUERY_4, (taxon, date,collector,  locality))
            res4 = cur.fetchall()
            if res4:
                links = [f'{r[0]}' for r in res4]
                results_4.append("; ".join(links))
            else:
                results_4.append(None)
        else:
            results_4.append(None)

        # pátý dotaz
        if taxon and pd.notna(date):
            cur.execute(SQL_QUERY_5, (taxon, locality, date, collector))
            res5 = cur.fetchall()
            if res5:
                links = [f'{r[0]}' for r in res5]
                results_5.append("; ".join(links))
            else:
                results_5.append(None)
        else:
            results_5.append(None)

    df["shoda přímo v original_id"] = results_1
    df["collectorANDdatumANDlokalita"] = results_2
    df["datumAND[collectorORlocalita]"] = results_3
    df["datumORcollectorORlocalita"] = results_4
    df["localitaOR[datumORcollector]"] = results_5

    print("💾 Ukládám výsledek do", OUTPUT_FILE)
    df.to_excel(OUTPUT_FILE, index=False)

    cur.close()
    conn.close()
    print("✅ Hotovo!")


if __name__ == "__main__":
    main()
