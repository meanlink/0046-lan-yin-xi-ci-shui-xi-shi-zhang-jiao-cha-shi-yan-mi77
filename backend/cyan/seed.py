from cyan.demo_strips import PAIRS

def seed(connection):
    connection.execute("INSERT INTO plates VALUES('CY-032','桥影负片 B32','雁皮棉纸 LP-7',60,120,.06,'open') ON CONFLICT DO NOTHING")
    for code,short_temp,long_temp,short_density,long_density,long_fade,state in PAIRS:
        connection.execute("INSERT INTO strips(plate,code,state) VALUES('CY-032',%s,%s) ON CONFLICT DO NOTHING",(code,state))
        for side,temp,density,fade in (("short",short_temp,short_density,None),("long",long_temp,long_density,long_fade)):
            connection.execute(
                "INSERT INTO strip_readings(plate,strip,side,temp,density,fade) VALUES('CY-032',%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING",
                (code,side,temp,density,fade))
