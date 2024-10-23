import uiautomator2 as u2
import subprocess
import time
from datetime import datetime
import random

def log_action(action_message):
    current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_message = f"[{current_datetime}] {action_message}"
    with open('activity_logs_proxy.txt', 'a') as log_file:
        log_file.write(log_message + '\n')

def run_adb_command(command):
    time.sleep(5)
    try:
        result = subprocess.run(
            ['adb'] + command.split(),
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error executing command '{command}': {e.stderr.strip()}")
        log_action(f"Error executing command '{command}': {e.stderr.strip()}")
        return None
    
# host = "standard.vital-proxies.com"
# port = "8603"
# password = "glzhaitymdl0ydai"

def setup_proxy_main(host, port, username, password, device):

    packages = run_adb_command('shell pm list packages')
    if packages is None:
        print("Failed to retrieve package list.")
        log_action("Failed to retrieve package list.")
        return

    if 'package:com.scheler.superproxy' not in packages:
        print("SuperProxy app is not installed.")
        log_action("SuperProxy app is not installed.")
        return
    
    subprocess.call("adb shell pm clear com.scheler.superproxy --user 0 --cache")
    time.sleep(2)
    subprocess.call("adb shell pm clear com.scheler.superproxy")

    print("Adding proxy details..")

    d = u2.connect(device.serial)
    d.app_start("com.scheler.superproxy")
    log_action("SuperProxy app started.")    

    time.sleep(5)
    try:
        d(description="Add proxy").click()
        print("Clicked on Add Proxy")
        log_action("Clicked on Add Proxy")
    except Exception as e:
        print(f"Error accessing Add Proxy: {e}")
        log_action(f"Error accessing Add Proxy: {e}")

    time.sleep(5)
    try:
        d(text ="SOCKS5").click()
        print("Clicked on SOCKS5")
        log_action("Clicked on SOCKS5")
        time.sleep(3)

    except Exception as e:
        print(f"Error accessing SOCKS5: {e}")
        log_action(f"Error accessing SOCKS5: {e}")

    time.sleep(5)
    try:
        d(description ="HTTP").click()
        print("Clicked on HTTP")
        log_action("Clicked on HTTP")

    except Exception as e:
        print(f"Error accessing HTTP: {e}")
        log_action(f"Error accessing HTTP: {e}")

    subprocess.call(f"adb -s {device.serial} shell input keyevent 4")

    time.sleep(3)
    try:
        post_xpath="/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View/android.view.View/android.view.View[1]/android.view.View/android.view.View[2]/android.widget.EditText[3]"
        if d.xpath(post_xpath).exists:  # Check if the element exists
            d.xpath(post_xpath).click()  # Click the element if found     
            print("Clicked on Server")
            log_action("Clicked on Server")
            d.send_keys(host)
    except Exception as e:
        print(f"Error accessing Server: {e}")
        log_action(f"Error accessing Server: {e}")

    time.sleep(5)

    try:
        post_xpath="/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View/android.view.View/android.view.View[1]/android.view.View/android.view.View[2]/android.widget.EditText[4]"
        if d.xpath(post_xpath).exists:  # Check if the element exists
            d.xpath(post_xpath).click()  # Click the element if found     
            print("Clicked on Port")
            log_action("Clicked on Port")
            time.sleep(2)
            d.send_keys(port)
    except Exception as e:
        print(f"Error accessing Port: {e}")
        log_action(f"Error accessing Port: {e}")

    time.sleep(5)
    try:
        d(text="None").click()
        print("Clicked on Authentication")
        log_action("Clicked on Authentication")
    except Exception as e:
        print(f"Error accessing Authentication: {e}")
        log_action(f"Error accessing Authentication: {e}")

    time.sleep(5)
    try:
        d(description="Username/Password").click()
        print("Clicked on Username/Password")
        log_action("Clicked on Username/Password")
    except Exception as e:
        print(f"Error accessing Username/Password: {e}")
        log_action(f"Error accessing Username/Password: {e}")

    time.sleep(5)
    try:
        post_xpath="/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View/android.view.View/android.view.View[1]/android.view.View/android.widget.ScrollView/android.widget.EditText[6]"
        if d.xpath(post_xpath).exists:  # Check if the element exists
            d.xpath(post_xpath).click()  # Click the element if found        
            print("Clicked on Username")
            log_action("Clicked on Username")
            d.send_keys(username)
    except Exception as e:
        print(f"Error accessing Username: {e}")
        log_action(f"Error accessing Username: {e}")

    time.sleep(5)
    try:
        post_xpath="/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View/android.view.View/android.view.View[1]/android.view.View/android.widget.ScrollView/android.widget.EditText[7]"
        if d.xpath(post_xpath).exists:  # Check if the element exists
            d.xpath(post_xpath).click()  # Click the element if found    
            print("Clicked on Password")
            log_action("Clicked on Password")
            d.send_keys(password)
    except Exception as e:
        print(f"Error accessing Password: {e}")
        log_action(f"Error accessing Password: {e}")

    #Save settings
    time.sleep(5)
    try:
        post_xpath="/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View/android.view.View/android.view.View[1]/android.view.View/android.view.View[1]/android.widget.Button[2]"
        if d.xpath(post_xpath).exists:  # Check if the element exists
            d.xpath(post_xpath).click()  # Click the element if found    
            print("Clicked on Save")
            log_action("Clicked on Save")
    except Exception as e:
        print(f"Error accessing Save: {e}")
        log_action(f"Error accessing Save: {e}")


    time.sleep(5)
    try:
        d(description="Start").click()
        print("Clicked on Start")
        log_action("Clicked on Start")
    except Exception as e:
        print(f"Error accessing Start: {e}")
        log_action(f"Error accessing Start: {e}")

    time.sleep(5)


    if d(text="OK").exists:
        d(text="OK").click()
        print("Clicked on OK")
        log_action("Clicked on OK")

    return "Proxy setup successfully"
