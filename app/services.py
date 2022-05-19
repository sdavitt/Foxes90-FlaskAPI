import requests as r

def getF1Drivers():
    data = r.get('https://ergast.com/api/f1/current/driverStandings.json')
    if data.status_code == 200:
        data = data.json()
    else:
        return 'broken api'
    seasonNum = data['MRData']['StandingsTable']['season']
    driversList = [(f'{x["Driver"]["givenName"]} {x["Driver"]["familyName"]}', x['points']) for x in data['MRData']['StandingsTable']['StandingsLists'][0]['DriverStandings']]
    return {
        'season': seasonNum,
        'drivers': driversList
    }