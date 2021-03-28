import pydest
import asyncio
import time

HEADERS = {"X-API-Key": '19a8efe4509a4570bee47bd9883f7d93'}
API_KEY = '19a8efe4509a4570bee47bd9883f7d93'
ROOT = 'https://www.bungie.net/Platform'
destiny = pydest.Pydest(API_KEY)

async def main():

    time_start = time.time()
    weaponlist={}
    activities = await destiny.api.get_activity_history(3,4611686018497181967,2305843009574424386,20,5,0)
    for i in activities['Response']['activities']:
        activityid = i['activityDetails']['instanceId']
        detail = await destiny.api.get_post_game_carnage_report(int(activityid))
        for j in detail['Response']['entries']:
            if j['player']['destinyUserInfo']['membershipId']=='4611686018497181967':
                if 'weapons' in j['extended']:
                    for weapon in j['extended']['weapons']:
                        Weaponid = weapon['referenceId']
                        Kills = weapon['values']['uniqueWeaponKills']['basic']['value']
                        PrecisionKills = weapon['values']['uniqueWeaponPrecisionKills']['basic']['value']
                        if Weaponid in weaponlist:
                            weaponlist[Weaponid]['Kills'] += Kills
                            weaponlist[Weaponid]['PrecisionKills'] += PrecisionKills
                        else:
                            weaponlist[Weaponid]={'Kills':Kills,'PrecisionKills':PrecisionKills}
            break
    for i in weaponlist:
        WeaponName = await destiny.decode_hash(i,'DestinyInventoryItemDefinition')
        weaponlist[i]['Name']=WeaponName['displayProperties']['name']

    time_end = time.time()
    print('totally cost',time_end-time_start)
    print(weaponlist)
    print(weaponlist)




loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()