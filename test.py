from utils.data import Data 

data = Data()

#print(data.get_counties())

county = 'ELGEYO MARAKWET'
cs = data.get_constituencies(county)
for c in cs:
    #print(c.name)
    ws = data.get_wards(county, c.id)
    for w in ws:
        #print(w.name)
        ps = data.get_polling_stations(county, w.id)
        for p in ps:
            print(p.name)