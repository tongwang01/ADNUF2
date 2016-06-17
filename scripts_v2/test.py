base_url = 'http://partnerapi.funda.nl/feeds/Aanbod.svc/search/\
json/c7e56d1972654b91bdd54fa12cf9d9c8/?website=funda&\
type=%s&\
zo=%s\
&page=%d\
&pagesize=25&projectObjectenTonen=2&objectTypenTonen=true&statistiekId=140'

url = base_url %('koop', 'amsterdam', 1)
print url