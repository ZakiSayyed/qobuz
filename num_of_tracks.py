import requests
import re

app_id = '950096963'
user_auth_token = 'aEngp_DVQx2AkrFPPowVAPiKfrSsDnot1sgZA4GfC8eJjFk5pN0BBiyGZqtOv0cxrzp8Jd4egcqMZiofs123NA'
cookie = 'wzuid=0c5077ac19276317a97; OptanonAlertBoxClosed=2024-10-10T11:30:08.477Z; _gcl_au=1.1.932071894.1728559808; lantern=2361e47f-ceda-4041-8f69-a4180a4610f8; _fbp=fb.1.1728559808904.361507799772415876; ABTasty=uid=ee6hjxmweky49db0&fst=1728559808575&pst=-1&cst=1728559808575&ns=1&pvt=3&pvis=3&th=; _hjSessionUser_135526=eyJpZCI6IjY0N2UyMjVmLTA3OTUtNWUwNy1hNjA2LWYxOGQ0NGI3MDRiNSIsImNyZWF0ZWQiOjE3Mjg1NTk4MzI3NTUsImV4aXN0aW5nIjp0cnVlfQ==; intercom-id-cbgll1zj=51220d90-b8e3-422f-81a6-20907fc8cc11; intercom-session-cbgll1zj=; intercom-device-id-cbgll1zj=84222137-cd73-45d8-ab73-6c623e4a811a; Unbounce_Check=2024-10-18T11:52:25.379Z; _clck=k75b18%7C2%7Cfq7%7C0%7C1744; cto_bundle=CGUOdl9tUU4xalolMkZJbGVtWmlRSDByd3RObFh4TTclMkZoTmtXU1NaMTczdzglMkY3TUV1NWtndWx5b1RUM0VaMkloWXFBQyUyRmRmdUZvJTJCbk83akJTSFlTWnJ4Yk5RTXFTbDJyOFUlMkJKS1c5bDNLSUhHZHh3UTV5dFo1RDNldUNuVTBocmthVlFVbUclMkZyeTc5VXFBSWN6dDVYdnB2UXNRQlp0YnpreEloSW9IVCUyQjdlclFwWjl5cXc3YXF1OWxIUiUyRkFMQmxhTEQlMkZmJTJCb2swcURIMmdnWklQN0ZMQ2ElMkYwTXRNNDhQVjJLeEp3ZndyS3Y4RVoxNGFPSjMzQmhRQ2pGM2RySCUyQnFuMW1NUUk; _rdt_uuid=1728559808533.515de6b9-7bd2-45b5-a529-f706cf405407; _uetvid=01452b2086fb11efa1679f9e3bae0bf9; RT="z=1&dm=www.qobuz.com&si=6b29edb0-06e4-459d-9a9c-69b2aae82996&ss=m2jlj26v&sl=2&tt=30b&rl=1&obo=1&ld=nff&r=2plpzicz&ul=nfg&hd=nfg"; qobuz-session=b173bfe69a72fa6fc5b75dd333e7437f; _ga=GA1.1.204862717.1728559808; ab.storage.deviceId.b464b6f4-ee64-4efe-91b5-5b43f8932bed=%7B%22g%22%3A%22907e09f0-2659-e870-bb76-a21af474bed2%22%2C%22c%22%3A1728559840549%2C%22l%22%3A1729780928263%7D; ab.storage.userId.b464b6f4-ee64-4efe-91b5-5b43f8932bed=%7B%22g%22%3A%222482895%22%2C%22c%22%3A1729080533913%2C%22l%22%3A1729780928263%7D; _ga_BCS72N6MDF=GS1.1.1729780928.15.1.1729781230.59.0.2141146912; OptanonConsent=isGpcEnabled=0&datestamp=Thu+Oct+24+2024+20%3A17%3A10+GMT%2B0530+(India+Standard+Time)&version=202408.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&genVendors=&consentId=96750a33-70a2-4836-b922-3bcc7cce776c&interactionCount=2&isAnonUser=1&landingPath=NotLandingPage&groups=PERSO%3A1%2CTECH%3A1%2CPERF%3A1%2CADS%3A1&AwaitingReconsent=false&intType=1&geolocation=IN%3BDL; ab.storage.sessionId.b464b6f4-ee64-4efe-91b5-5b43f8932bed=%7B%22g%22%3A%2263fd2670-eb8e-21c3-6e20-35ccae5d6857%22%2C%22e%22%3A1729795630732%2C%22c%22%3A1729780928262%2C%22l%22%3A1729781230732%7D; mp_7af82412ec23205c631d2e82a099e0f7_mixpanel=%7B%22distinct_id%22%3A%202482895%2C%22%24device_id%22%3A%20%2219276320310992-0c9dd67d10621b-26001051-1fa400-19276320310992%22%2C%22__mps%22%3A%20%7B%7D%2C%22__mpso%22%3A%20%7B%7D%2C%22__mpus%22%3A%20%7B%7D%2C%22__mpa%22%3A%20%7B%7D%2C%22__mpu%22%3A%20%7B%7D%2C%22__mpr%22%3A%20%5B%5D%2C%22__mpap%22%3A%20%5B%5D%2C%22%24user_id%22%3A%202482895%2C%22%24initial_referrer%22%3A%20%22https%3A%2F%2Fwww.qobuz.com%2F%22%2C%22%24initial_referring_domain%22%3A%20%22www.qobuz.com%22%2C%22tech_env%22%3A%20%22PROD%22%2C%22app_major_version%22%3A%201%2C%22app_full_version%22%3A%20%221.2.0%22%2C%22app_category%22%3A%20%22Qobuz%20Player%22%2C%22app_name%22%3A%20%22Qobuz%20Web%20Player%22%2C%22user_age%22%3A%2063%2C%22user_gender%22%3A%20%22male%22%2C%22user_current_subscription_offer%22%3A%20%22studio%22%2C%22user_current_subscription_periodicity%22%3A%20%22annual%22%2C%22user_current_subscription_start_date%22%3A%20%22%22%2C%22debug_id_client%22%3A%202482895%2C%22%24search_engine%22%3A%20%22google%22%7D'

def extract_album_id(album_url):
    match = re.search(r'/album/([^/]+)', album_url)
    return match.group(1) if match else None

def get_track_count(album_url):
    album_id = extract_album_id(album_url)

    if album_id is None:
        print(f"Error: Unable to extract album ID from link: {album_url}")
        return 3

    url = f'https://www.qobuz.com/api.json/0.2/album/get?album_id={album_id}&app_id={app_id}'
    
    headers = {
        'Authorization': f'Bearer {user_auth_token}',
        'Cookie': cookie,
    }

    with requests.Session() as session:
        response = session.get(url, headers=headers)
        
        if response.status_code == 200:
            album_data = response.json()
            track_count = album_data.get('tracks_count', None)

            if track_count is not None:
                print(f'Album Link: {album_url}, Track Count: {track_count}')
                return track_count
            else:
                print(f"Error: 'tracks_count' key not found in the response for Album ID: {album_id}.")
                return 3
        else:
            print(f'Error fetching data for Album Link {album_url}: {response.status_code}, {response.text}')
            return 3

# num_of_tracks = get_track_count('https://open.qobuz.com/album/eh29kwu637uka')
# print(f"Number of tracks : {num_of_tracks}")
