#import cx_Oracle

def read(input, con):
    cur = con.cursor()
    query = 'select * from melanoma.muestras where id_muestra=%d' % (input)
    #print (query)
    cur.execute(query)
    result=cur.fetchone()
    data = result[6].read().decode("utf-8") 
    #print (data)
    cur.close()
    #print (data)
    return data
