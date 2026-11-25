from cyan.demo_strips import PAIRS

def seed(connection):
    connection.execute("INSERT INTO plates VALUES('CY-032','桥影负片 B32','雁皮棉纸 LP-7',60,120,.06,'open') ON CONFLICT DO NOTHING")
    for row in PAIRS:
        connection.execute("INSERT INTO strips VALUES('CY-032',%s,%s,%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING",row)
