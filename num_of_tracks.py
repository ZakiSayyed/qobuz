import requests
import re


app_id = '950096963'
user_auth_token = 'aEngp_DVQx2AkrFPPowVAPiKfrSsDnot1sgZA4GfC8eJjFk5pN0BBiyGZqtOv0cxrzp8Jd4egcqMZiofs123NA'
cookie = 'wzuid=0c5077ac19276317a97; OptanonAlertBoxClosed=2024-10-10T11:30:08.477Z; _gcl_au=1.1.932071894.1728559808; lantern=2361e47f-ceda-4041-8f69-a4180a4610f8; _fbp=fb.1.1728559808904.361507799772415876; ABTasty=uid=ee6hjxmweky49db0&fst=1728559808575&pst=-1&cst=1728559808575&ns=1&pvt=3&pvis=3&th=; _hjSessionUser_135526=eyJpZCI6IjY0N2UyMjVmLTA3OTUtNWUwNy1hNjA2LWYxOGQ0NGI3MDRiNSIsImNyZWF0ZWQiOjE3Mjg1NTk4MzI3NTUsImV4aXN0aW5nIjp0cnVlfQ==; intercom-id-cbgll1zj=51220d90-b8e3-422f-81a6-20907fc8cc11; intercom-session-cbgll1zj=; intercom-device-id-cbgll1zj=84222137-cd73-45d8-ab73-6c623e4a811a; Unbounce_Check=2024-10-18T11:52:25.379Z; _clck=k75b18%7C2%7Cfq7%7C0%7C1744; cto_bundle=CGUOdl9tUU4xalolMkZJbGVtWmlRSDByd3RObFh4TTclMkZoTmtXU1NaMTczdzglMkY3TUV1NWtndWx5b1RUM0VaMkloWXFBQyUyRmRmdUZvJTJCbk83akJTSFlTWnJ4Yk5RTXFTbDJyOFUlMkJKS1c5bDNLSUhHZHh3UTV5dFo1RDNldUNuVTBocmthVlFVbUclMkZyeTc5VXFBSWN6dDVYdnB2UXNRQlp0YnpreEloSW9IVCUyQjdlclFwWjl5cXc3YXF1OWxIUiUyRkFMQmxhTEQlMkZmJTJCb2swcURIMmdnWklQN0ZMQ2ElMkYwTXRNNDhQVjJLeEp3ZndyS3Y4RVoxNGFPSjMzQmhRQ2pGM2RySCUyQnFuMW1NUUk; qobuz-session=r78cjqlu8kn09kpkqmqoa4sfirl5v9gc; dismissed_store_launch_info_ids=store-launch-info-popinv2-1; ab.storage.deviceId.b464b6f4-ee64-4efe-91b5-5b43f8932bed=%7B%22g%22%3A%22907e09f0-2659-e870-bb76-a21af474bed2%22%2C%22c%22%3A1728559840549%2C%22l%22%3A1729542753286%7D; ab.storage.userId.b464b6f4-ee64-4efe-91b5-5b43f8932bed=%7B%22g%22%3A%222482895%22%2C%22c%22%3A1729080533913%2C%22l%22%3A1729542753286%7D; wzsid=e2dd59f4b6496716c076; _gid=GA1.2.302201060.1729544311; _hjSession_135526=eyJpZCI6IjJhMTdhMjdlLWNiZmItNDYwZi1iM2NmLTFjOWVhYzE3ODQ2NSIsImMiOjE3Mjk1NDQzMTEwMjUsInMiOjAsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjowLCJzcCI6MH0=; wzcnst=1; wzsite=CA; _ga=GA1.1.204862717.1728559808; wzvp=tag_version=2024-09-17%2018%3A00&dl_country=CA&site_from_url=CA&dl_language=en&sectionName=Front%20-%20Download%20Shop&technicalEnvironment=prod; _rdt_uuid=1728559808533.515de6b9-7bd2-45b5-a529-f706cf405407; _uetsid=8b3995008fe511ef9da5d13b5df173eb; _uetvid=01452b2086fb11efa1679f9e3bae0bf9; RT=\"z=1&dm=www.qobuz.com&si=6b29edb0-06e4-459d-9a9c-69b2aae82996&ss=m2ji0xuz&sl=2&tt=3bw&rl=1\"; _clsk=2ontm2%7C1729545504608%7C2%7C1%7Ct.clarity.ms%2Fcollect; ab.storage.sessionId.b464b6f4-ee64-4efe-91b5-5b43f8932bed=%7B%22g%22%3A%22e9cd0d02-e4a7-15a5-a254-cd5eb2e1ffe8%22%2C%22e%22%3A1729560891944%2C%22c%22%3A1729542753285%2C%22l%22%3A1729546491944%7D; OptanonConsent=isGpcEnabled=0&datestamp=Tue+Oct+22+2024+03%3A04%3A52+GMT%2B0530+(India+Standard+Time)&version=202408.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&genVendors=&consentId=96750a33-70a2-4836-b922-3bcc7cce776c&interactionCount=2&isAnonUser=1&landingPath=NotLandingPage&groups=PERSO%3A1%2CTECH%3A1%2CPERF%3A1%2CADS%3A1&AwaitingReconsent=false&intType=1&geolocation=IN%3BDL; _ga_BCS72N6MDF=GS1.1.1729546490.13.1.1729546492.58.0.1396669792; mp_7af82412ec23205c631d2e82a099e0f7_mixpanel=%7B%22distinct_id%22%3A%202482895%2C%22%24device_id%22%3A%20%226b906c68-b787-4746-8178-37a681d902d3%22%2C%22%24user_id%22%3A%202482895%2C%22%24initial_referrer%22%3A%22%22%2C%22%24initial_referring_domain%22%3A%22%22%2C%22%24last_referrer%22%3A%22%22%2C%22%24last_referring_domain%22%3A%22%22%2C%22%24referrer%22%3A%22%22%2C%22%24referring_domain%22%3A%22%22%7D; _gat_UA-800326-5=1; ab.storage.isFirstVisit.b464b6f4-ee64-4efe-91b5-5b43f8932bed=true; ABTasty=uid=ee6hjxmweky49db0&fst=1729549807123&pst=1729549807123&cst=1729549807123&ns=1&pvt=3&pvis=3&th=; _gat_UA-800326-5=1; ab.storage.isFirstVisit.b464b6f4-ee64-4efe-91b5-5b43f8932bed=true; _clsk=2ontm2%7C1729545504608%7C2%7C1%7Ct.clarity.ms%2Fcollect; _gcl_dc=GCL.10sBfRZ7q0w.0D5AY8h4Qco; _fbp=fb.1.1728559808904.361507799772415876'

def extract_album_id(album_url):
    match = re.search(r'/album/([^/]+)', album_url)
    return match.group(1) if match else None

# with open('upc.txt', 'r') as file:
#     album_urls = [line.strip() for line in file if line.strip()]


def get_track_count(album_url):

    album_id = extract_album_id(album_url)

    if album_id is None:
        print(f"Error: Unable to extract album ID from link: {album_url}")

    url = f'https://www.qobuz.com/api.json/0.2/album/get?album_id={album_id}&app_id={app_id}'
    
    headers = {
        'Authorization': f'Bearer {user_auth_token}',
        'Cookie': cookie,
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        album_data = response.json()

        # print(f"Response for Album ID {album_id}: {album_data}")

        track_count = album_data.get('tracks_count', None)
        if track_count is not None:
            print(f'Album Link: {album_url}, Track Count: {track_count}')
        else:
            print(f"Error: 'tracks_count' key not found in the response for Album ID: {album_id}.")
    else:
        print(f'Error fetching data for Album Link {album_url}: {response.status_code}, {response.text}')
    
    return track_count
    
numoftracks = get_track_count('https://open.qobuz.com/album/eh29kwu637uka')
print(f"Number of tracks : {numoftracks}")