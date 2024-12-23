import uiautomator2 as u2
import csv
import random
import time
import threading
import subprocess
import logging
import os
import requests

total_streams = 1

# from super_proxy import setup_proxy_main
from num_of_tracks import get_track_count
from install_apks import main_install_apk

# Setup logging
logging.basicConfig(
    filename='activity_log.txt',
    level=logging.INFO,
    format='%(asctime)s - %(threadName)s - %(message)s'
)

# Global configuration for the script
config = {
    'stream_limit_min': 1,     # Minimum number of streams per account
    'stream_limit_max': 1,     # Maximum number of streams per account
    'play_time_min': 60,        # Minimum play time per track in seconds
    'play_time_max': 80,       # Maximum play time per track in seconds
    'content_distribution': {   # Percentage distribution for playing content
        'track': 100,
        'album': 0,
        'artist_search': 0
    },
    'track_interaction': {      # Interaction settings
        'like_percentage': 50,  # 100% chance to like the song
        'add_to_playlist': 50   # 100% chance to add the song to playlist
    }
}
def load_inputs():
    accounts = []
    album_urls = []
    track_urls = []
    artist_songs = []

    # Load account details
    with open('accounts.csv', mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            accounts.append(row)

    # Load album URLs
    with open('albumn_urls.csv', mode='r') as file:
        reader = csv.reader(file)
        album_urls = list(reader)

    # Load track URLs
    with open('track_urls.csv', mode='r') as file:
        reader = csv.reader(file)
        track_urls = list(reader)

    # Load artist search keywords
    with open('artist_song.csv', mode='r') as file:
        reader = csv.reader(file)
        artist_songs = list(reader)

    return accounts, album_urls, track_urls, artist_songs

# Assign proxy for each account
def assign_proxy(d, username, proxyserver, proxyport):

    logging.info(f"Device ID : {d.serial} | Proxy Server : {proxyserver} | Proxy Port : {proxyport}") #| Username : {pusername} | Password : {ppassword} | Username : {username}")
    print(f"Device ID : {d.serial} | Proxy Server : {proxyserver} | Proxy Port : {proxyport}") # | Username : {pusername} | Password : {ppassword} | Username : {username}")
    # Implement proxy binding logic here using third-party proxy app (e.g., super_proxy or oxy proxy manager)
    # setup_proxy_main(proxyserver,proxyport,pusername,ppassword,d)
    subprocess.call(f"adb -s {d.serial} shell settings put global http_proxy {proxyserver}:{proxyport}")
    time.sleep(3)

# Log into Qobuz
def login_qobuz(d, username, password):
    time.sleep(5)
    with requests.Session() as session:  # Creates a session for reusing and closing connections

        subprocess.call(f"adb -s {d.serial} shell pm clear com.qobuz.music --user 0 --cache")
        time.sleep(2)
        subprocess.call(f"adb -s {d.serial} shell pm clear com.qobuz.music")
        
        # Start the Qobuz app and navigate to login using uiautomator2 on the device 'd'
        d.app_start("com.qobuz.music", "com.qobuz.android.mobile.app.screen.home.MainActivity")
        time.sleep(5)
        if d(resourceId='com.android.systemui:id/notification_stack_scroller').exists:
            print("Notification bar opened")
            subprocess.call(f'adb -s {d.serial} shell input swipe 500 1500 500 500 300')
            print("Notification bar closed")

        if d(text="EXPLORE").exists:
            d(text="No, thanks").click()
        elif d(text="Explore").exists:
            d(text="No, thanks").click()

        time.sleep(5)
        
        if d(text="Discover"):
            print("Logged in Already")
            d.app_stop("com.qobuz.music")
            # del d  # Disconnect u2 after stopping the app
            return

        logging.info(f"Device ID : {d.serial}\nLogging into Qobuz with email: {username} on device {d.serial}")
        print(f"Logging into Qobuz with email: {username} on device {d.serial}")
        time.sleep(5)
        
        if d(text='Enter your email address').exists:
            d(text='Enter your email address').click()
            d.send_keys(username)
        else:
            print("Unable to click on Enter Email")

        time.sleep(3)

        if d(text='Continue').exists:
            d(text='Continue').click()

        time.sleep(3)

        if d(text='Enter your password').exists:
            d(text='Enter your password').click()
            d.send_keys(password)

        time.sleep(5)

        if d.xpath('/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/androidx.compose.ui.platform.ComposeView/android.view.View/android.view.View/android.view.View/android.widget.ScrollView/android.view.View[1]').exists:
            d.xpath('/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/androidx.compose.ui.platform.ComposeView/android.view.View/android.view.View/android.view.View/android.widget.ScrollView/android.view.View[1]').click()
        else:
            print("Error, Unable to login")
            logging.info("Error, Unable to login")
            return
        
        time.sleep(5)

        if d(text='YES').exists:
            d(text='YES').click()
            print("Clicked on YES")
            
        time.sleep(5)

        if d(text='Allow').exists:
            d(text='Allow').click()
            print("Clicked on Allow access")
        elif d(text='ALLOW').exists:
            d(text='ALLOW').click()
            print("Clicked on ALLOW access")
        
        time.sleep(15)

        if d(text="Discover").exists:
            print("Logged in ")
            d.app_stop("com.qobuz.music")
            return True
        
# Initialize indices to track the next item for each content type
track_index = 0
album_index = 0
artist_index = 0

def select_content(d, album_urls, track_urls, artist_songs):
    global track_index, album_index, artist_index
    
    # Randomly select content type based on distribution
    content_type = random.choices(
        ['track', 'album', 'artist_search'],
        weights=[
            config['content_distribution']['track'],
            config['content_distribution']['album'],
            config['content_distribution']['artist_search']
        ],
        k=1
    )[0]
    
    # Select content based on type
    if content_type == 'track':
        # Select the next track based on track_index
        selected_content = track_urls[track_index]
        logging.info(f"Device ID : {d.serial}\nSelected track: {selected_content}")
        print(f"Selected track: {selected_content}")
        
        # Update the track index and reset if end of list is reached
        track_index = (track_index + 1) % len(track_urls)

    elif content_type == 'album':
        # Select the next album based on album_index
        selected_content = album_urls[album_index]
        logging.info(f"Device ID : {d.serial}\nSelected album: {selected_content}")
        print(f"Selected album: {selected_content}")
        
        # Update the album index and reset if end of list is reached
        album_index = (album_index + 1) % len(album_urls)

    elif content_type == 'artist_search':
        # Select the next artist based on artist_index
        selected_content = artist_songs[artist_index]
        logging.info(f"Device ID : {d.serial}\nSelected artist/song search: {selected_content}")
        print(f"Selected artist/song search: {selected_content}")
        
        # Update the artist index and reset if end of list is reached
        artist_index = (artist_index + 1) % len(artist_songs)
    return content_type, selected_content

# Play selected content for a random duration
def play_content(d, content_type, content):
    time.sleep(3)
    selected_content = content[0]
    with requests.Session() as session:
        # d = u2.connect(device.serial)
        print(d.serial)
        
        play_duration = random.randint(config['play_time_min'], config['play_time_max'])
        minutes = play_duration // 60
        seconds = play_duration % 60
        
        # Format the output to MM:SS
        duration = f"{minutes:02}:{seconds:02}"
        print(f"Play duration is : {duration}")
        # Set 100% chance for testing
        like_percentage = config['track_interaction']['like_percentage']  
        add_to_playlist_percentage = config['track_interaction']['add_to_playlist']  

        if content_type == 'track':
            time.sleep(5)
            d.shell(f"am start -a android.intent.action.VIEW -d '{selected_content}'")
            time.sleep(6)

            logging.info(f"Device ID : {d.serial}\nSelected track: {selected_content}")
            print(f"Selected track: {selected_content}")

            if d(text='Playback paused').exists:
                print("Playback paused")
                logging.info("Playback paused")
                return
            
            if d(description='Play').exists:
                d(description='Play').click()
                print("Clicked on Play")    

            time.sleep(3)

            if d(text='Playback paused').exists:
                print("Playback paused")
                logging.info("Playback paused")
                return
            
            if d.xpath('/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.FrameLayout[2]/androidx.compose.ui.platform.ComposeView/android.view.View/android.view.View/android.view.View').exists:
                d.xpath('/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.FrameLayout[2]/androidx.compose.ui.platform.ComposeView/android.view.View/android.view.View/android.view.View').click()
                print("Clicked on the Song being played")
            
            time.sleep(3)

            song_paused = False
            while not song_paused:
                if d(text=f'{duration}').exists():
                    if d(resourceId='com.qobuz.music:id/playPauseBtn').exists:
                        d(resourceId='com.qobuz.music:id/playPauseBtn').click()
                        print("Song Paused")
                        song_paused = True  # Mark the song as paused but continue with rest of the logic

            should_like = random.randint(1, 100) <= like_percentage
            should_add_to_playlist = random.randint(1, 100) <= add_to_playlist_percentage

            # Perform the like action
            if should_like:
                if d(resourceId='com.qobuz.music:id/addRemoveFavoritesImageView').exists:
                    d(resourceId='com.qobuz.music:id/addRemoveFavoritesImageView').click()
                    print("Song liked!")

            # Perform the add to playlist action
            if should_add_to_playlist:
                if d(resourceId='com.qobuz.music:id/optionsImage').exists:
                    d(resourceId='com.qobuz.music:id/optionsImage').click()
                    print("Clicked on Options")
                    if d(text='Add to playlists').exists:
                        d(text='Add to playlists').click()
                        print("Clicked on Add to Playlists")
                    time.sleep(3)
                    if d(resourceId='com.qobuz.music:id/subtitleText', instance=1).exists:
                        d(resourceId='com.qobuz.music:id/subtitleText', instance=1).click()
                        print("Clicked on the Playlist")
                        time.sleep(5)

                    print("Song added to playlist!")

            print("Stopping App")
            d.app_stop("com.qobuz.music")
            # del d  # Disconnect u2 after stopping the app
        elif content_type == 'album':
            time.sleep(5)
            d.shell(f"am start -a android.intent.action.VIEW -d '{selected_content}'")
            time.sleep(6)

            logging.info(f"Device ID : {d.serial}\nSelected album: {selected_content}")
            print(f"Selected album: {selected_content}")

            if d(text='Playback paused').exists:
                print("Playback paused")
                logging.info("Playback paused")
                return
            
            if d(description='Play').exists:
                d(description='Play').click()
                print("Clicked on Play")    
            
            time.sleep(3)
            
            if d(text='Playback paused').exists:
                print("Playback paused")
                logging.info("Playback paused")
                return
            
            if d.xpath('/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.FrameLayout[2]/androidx.compose.ui.platform.ComposeView/android.view.View/android.view.View/android.view.View').exists:
                d.xpath('/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.FrameLayout[2]/androidx.compose.ui.platform.ComposeView/android.view.View/android.view.View/android.view.View').click()
                print("Clicked on the Song being played")
            
            time.sleep(3)

            numoftracks = get_track_count(selected_content)
            print(f"Number of tracks : {numoftracks}")

            count = 0
            print(f"Skipping {numoftracks} tracks")
            while count < numoftracks:
                if d(text=f'{duration}').exists():
                    if d(resourceId='com.qobuz.music:id/skipNextBtn').exists:
                        d(resourceId='com.qobuz.music:id/skipNextBtn').click()
                        print("Song Skipped")
                        count += 1
                    else:
                        print("Skip button not found.")
            
            time.sleep(3)

            d.app_stop("com.qobuz.music")
            # del d  # Disconnect u2 after stopping the app

        elif content_type == 'artist_search':

            d.app_start("com.qobuz.music", "com.qobuz.android.mobile.app.screen.home.MainActivity")
            time.sleep(5)
            if d(resourceId='com.android.systemui:id/notification_stack_scroller').exists:
                print("Notification bar opened")
                subprocess.call(f'adb -s {d.serial} shell input swipe 500 1500 500 500 300')
                print("Notification bar closed")
            if d(text="Samsung Keyboard").exists:
                d(text="Agree").click()
                print("Clicked on Agree")
                logging.info("Clicked on Agree")
            elif d(resourceId='android:id/button1').exists:
                d(resourceId='android:id/button1').click()
                print("Clicked on Agree")
                logging.info("Clicked on Agree")
            while True:
                if d.xpath('/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.FrameLayout/androidx.compose.ui.platform.ComposeView/android.view.View/android.view.View/android.view.View/android.widget.EditText/android.view.View[3]').exists:
                    d.xpath('/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.FrameLayout/androidx.compose.ui.platform.ComposeView/android.view.View/android.view.View/android.view.View/android.widget.EditText/android.view.View[3]').click()
                    print("Removed the existing text in search")

                if d(text='Search').exists:
                    d(text='Search').click()
                    print("Clicked on Search")
                    break
                else:
                    subprocess.call(f"adb -s {d.serial} shell input keyevent 4")
                    time.sleep(3)
                    if d.xpath('/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.FrameLayout/androidx.compose.ui.platform.ComposeView/android.view.View/android.view.View/android.view.View/android.widget.EditText/android.view.View[3]').exists:
                        d.xpath('/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.FrameLayout/androidx.compose.ui.platform.ComposeView/android.view.View/android.view.View/android.view.View/android.widget.EditText/android.view.View[3]').click()
                        print("Removed the existing text in search")

            time.sleep(3)

            if d(description='Search').exists:
                d(description='Search').click()
                print("Clicked on Search")

            d.send_keys(selected_content)    

            time.sleep(3)

            if d(text='Tracks').exists:
                d(text='Tracks').click()
                print("Clicked on Tracks")

            time.sleep(2)

            if d(description='Options', instance=0).exists:
                d(description='Options', instance=0).click()
                print("Clicked on Options")

            time.sleep(6)

            if d(text='Playback paused').exists:
                print("Playback paused")
                logging.info("Playback paused")
                return
            
            if d(description='Play').exists:
                d(description='Play').click()
                print("Clicked on Play")    

            if d(text='Playback paused').exists:
                print("Playback paused")
                logging.info("Playback paused")
                return
            
            if d.xpath('/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.FrameLayout[2]/androidx.compose.ui.platform.ComposeView/android.view.View/android.view.View/android.view.View').exists:
                d.xpath('/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.FrameLayout[2]/androidx.compose.ui.platform.ComposeView/android.view.View/android.view.View/android.view.View').click()
                print("Clicked on the Song being played")

            while True:
                if d(text=f'{duration}').exists():
                    if d(resourceId='com.qobuz.music:id/playPauseBtn').exists:
                        d(resourceId='com.qobuz.music:id/playPauseBtn').click()
                        print("Song Paused")
                        break

            d.app_stop("com.qobuz.music")
            # del d

# Main bot execution function for each device
def bot_execution(d, udid,username, password, proxyserver, proxyport, album_urls, track_urls, artist_songs):
    logging.info(f"Starting bot on device: {udid}")
    print(f"Starting bot on device: {udid}")
    # d = u2.connect(udid)  # Connect to the device with specific UDID
    try:
        state=True
        assign_proxy(d, username, proxyserver, proxyport)  # Step 2: Assign proxy and bind it
        state = login_qobuz(d, username, password)   # Step 3: Login to Qobuz
        if state:
            stream_limit = random.randint(config['stream_limit_min'], config['stream_limit_max'])
            logging.info(f"Stream limit for account {username} on device {udid}: {stream_limit}")
            print(f"Stream limit for account {username} on device {udid}: {stream_limit}")

            streams = 0
            global total_streams

            while streams < stream_limit:
                content_type, selected_content = select_content(d, album_urls, track_urls, artist_songs)
                play_content(d, content_type, selected_content)
                print("Selected content = ",selected_content)
                os.system(f"title Total Streams: {total_streams}")
                logging.info(f"Total Streams: {total_streams}")
                total_streams += 1
                streams += 1
                logging.info(f"Stream {streams} completed for account {username} on device {udid}")
                print(f"Stream {streams} completed for account {username} on device {udid}")

            # logout_account(d)
            logging.info(f"Bot execution completed on device {udid}")
            print(f"Bot execution completed on device {udid}")

    finally:
        print("Closing connection")
        d.app_stop("com.qobuz.music")  # Ensure the app is stopped
        # del d

# Function to get the list of connected devices
def get_device_udids():
    result = subprocess.run(['adb', 'devices'], stdout=subprocess.PIPE)
    output = result.stdout.decode('utf-8').splitlines()

    udids = []
    for line in output[1:]:
        if line.strip() and 'device' in line:
            udid = line.split()[0]
            udids.append(udid)
    
    logging.info(f"Connected devices: {udids}")
    print(f"Connected devices: {udids}")
    return udids

# Main function to launch threads for each device
def main():
    device_udids = get_device_udids()  # Step 1: Get connected devices
    connections = {udid: u2.connect(udid) for udid in device_udids}

    if not device_udids:
        logging.info("No devices connected. Exiting.")
        print("No devices connected. Exiting.")
        return

    logging.info(f"Number of connected devices: {len(device_udids)}")
    print(f"Number of connected devices: {len(device_udids)}")

    while True:  # Infinite loop to restart the process when all accounts are processed
        accounts, album_urls, track_urls, artist_songs = load_inputs()  # Reload accounts each loop
        num_accounts = len(accounts)

        if num_accounts == 0:
            logging.info("No accounts available in accounts.csv.")
            print("No accounts available in accounts.csv.")
            return

        logging.info(f"Total accounts available: {num_accounts}")
        print(f"Total accounts available: {num_accounts}")

        # Divide the accounts into chunks based on the number of devices
        chunk_size = len(device_udids)
        
        for i in range(0, num_accounts, chunk_size):
            threads = []
            # Assign each account to a device, if available
            accounts_chunk = accounts[i:i + chunk_size]
            for j, account in enumerate(accounts_chunk):
                device_udid = device_udids[j]  # Assign account to each device in sequence
                logging.info(f"Assigning account {account['username']} to device {device_udid}")
                print(f"Assigning account {account['username']} to device {device_udid}")

                username = account['username']
                password = account['password']
                proxyserver = account['pserver']
                proxyport = account['pport']

                # Create a new thread for each device and start it
                t = threading.Thread(target=bot_execution, args=(connections[device_udid], device_udid, username, password, proxyserver, proxyport, album_urls, track_urls, artist_songs,))
                threads.append(t)
                time.sleep(2)
                t.start()

            # Wait for all threads in this batch to complete
            for t in threads:
                t.join()

            logging.info(f"Completed account execution batch {i // chunk_size + 1}")
            print(f"Completed account execution batch {i // chunk_size + 1}")

        logging.info("All accounts have been processed. Restarting from the first account.")
        print("All accounts have been processed. Restarting from the first account.")
# def main():
#     device_udids = get_device_udids()  # Get connected devices
#     accounts, album_urls, track_urls, artist_songs = load_inputs()

#     if not device_udids:
#         print("No devices connected.")
#         return

#     # Pre-establish connections for all devices
#     connections = {udid: u2.connect(udid) for udid in device_udids}

#     # Start all devices simultaneously
#     threads = []
#     for i, udid in enumerate(device_udids):
#         account = accounts[i % len(accounts)]
#         username = account['username']
#         password = account['password']
#         proxyserver = account['pserver']
#         proxyport = account['pport']

#         # Pass pre-established connection to bot_execution
#         thread = threading.Thread(target=bot_execution, args=(
#             connections[udid], udid, username, password, proxyserver, proxyport, album_urls, track_urls, artist_songs
#         ))
#         threads.append(thread)
#         thread.start()

#     # Wait for all threads to complete
#     for thread in threads:
#         thread.join()

#     # Cleanup connections
#     for d in connections.values():
#         d.app_stop("com.qobuz.music")
#         del d

#     print("All devices have been processed.")

# Entry point for the script
if __name__ == "__main__":
    main_install_apk()
    main()
