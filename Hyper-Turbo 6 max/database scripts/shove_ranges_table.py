import sqlite3

conn = sqlite3.connect('handranges.db')
print "Opened database successfully";

conn.execute("DROP TABLE IF EXISTS hypercall")

# Create table as per requirement

sql = """CREATE TABLE hypercall (
        openpos VARCHAR(40),
        blinds INT,
        ante INT,
        players INT,
        pos VARCHAR(40),
        range FLOAT,
        UNIQUE(openpos, blinds, ante, players, pos))"""

conn.execute(sql)


# disconnect from server
conn.close()

