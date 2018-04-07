#!/usr/bin/env python2.7

print('')
import re
import os
import sys
import time
import urllib2
from getpass import getpass
try:
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
except ImportError:
    print('maybe try installing the prerequisites first? >:|\n')
    sys.exit(1)


# Don't want to use Xvfb? Uncomment the following line:
# """

import threading
import subprocess

class Xvfb:
    def __init__(self):
        self.process = None
    def __del__(self):
        self.process.kill()
    def setup(self):
        # setup X virtual framebuffer for our browser
        with open('/dev/null', 'w') as black_hole:
            self.process = subprocess.Popen(['Xvfb', ':1', '-screen', '0', '1024x768x8'],
                                            stdin=black_hole,
                                            stdout=black_hole,
                                            stderr=black_hole)
xvfb = Xvfb()
# wanna use python3.3+? be my guest:
# python3.3+:
#threading.Thread(target=xvfb.setup, daemon=True)
# python2.7-3.2:
thread = threading.Thread(target=xvfb.setup)
thread.daemon = True
thread.start()
os.environ["DISPLAY"] = ":1.0"
time.sleep(5)

# """


class MasteranimeDL:
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_extension('./ub.crx')
        self.driver = webdriver.Chrome(chrome_options=chrome_options)
        self.blacklist = set()

    def login(self, username, password):
        self.goto('http://www.masterani.me')
        self.get_by_xpath('login', hard_fail=True).click()
        self.get_by_xpath('username', hard_fail=True).send_keys(username)
        self.get_by_xpath('password', hard_fail=True).send_keys(password)
        self.get_by_xpath('submit', hard_fail=True).click()
        # just fetch to make sure we're logged in
        self.get_by_xpath('profile', hard_fail=True)
    
    def get_everything(self):
        self.get_show_links()
        self.set_content_cookies()
        while len(self.links) > 0:
            for link in self.links:
                vid_url = self.get_video_url(link)
                if self.download(link, vid_url):
                    print('{} - completed.\n'.format(link))
                    if not self.set_as_completed(link):
                        print('!!! something went terribly wrong!')
                        print('adding instead to blacklist...')
                        self.blacklist.add(link)
                else:
                    print("adding '{}' to blacklist\n".format(link))
                    self.blacklist.add(link)
            self.get_show_links()

    def get_show_links(self):
        print('getting links...')
        self.goto('http://www.masterani.me/my-anime')
    # double load to get rid of differently-styled new section
        self.goto('http://www.masterani.me/my-anime')
        self.links = []
        xpath = '//*[@id="myanime"]/div[2]/div/div[{}]/div/a[2]'
        try:
            count = 1
            while True:
                row = self.get_by_xpath(xpath.format(count), timeout=5)
                link = row.get_attribute('href')
                if link not in self.blacklist:
                    print('USE  - {}'.format(link))
                    self.links.append(link)
                else:
                    print('SKIP - {}'.format(link))
                count += 1
        except Exception:
            pass

    def set_content_cookies(self):
        print('injecting cookies...')
        self.set_cookie({'name' : 'pref_host', 'value' : '1'})
        self.set_cookie({'name' : 'pref_mirror', 'value' : '1%3B480'})

    def set_cookie(self, cookie):
        base = {
            'domain' : 'www.masterani.me',
            'expiry' : '2000000000.000000',
            'path' : '/',
            'secure' : False,
            'httpOnly' : False
        }
        base.update(cookie)
        self.driver.add_cookie(base)

    def get_video_url(self, link):
        print("getting video url for '{}'...".format(link))
        self.goto(link)
        frame_elem = self.get_by_xpath('frame')
        # if no iframe, video is hosted by masteranime
        if frame_elem is None:
            print('no iframe - getting masteranime video element...')
            frame_elem = self.get_by_xpath('frame_masteranime')
            if frame_elem is None:
                print("that didn't work either - returning null vid_url")
                return None
        # get the src of the frame element
        frame_src = frame_elem.get_attribute('src')

        if re.match('.*mp4upload.*', frame_src):
            # if it's an actual frame, travel there
            self.goto(frame_src)
            # and get the video's source url
            vid_tag = self.get_by_xpath('video_mp4upload')
            if vid_tag:
                print('got mp4upload vid_url successfully.')
                vid_url = vid_tag.get_attribute('src')
            else:
                print('FAILED to get mp4upload vid_url.')
                vid_url = None
        elif re.match('.*masterani\.me.*', frame_src):
            print('got it.')
            # if masterani.me is in the url, locally hosted
            vid_url = frame_src
        else:
            print('WHAT??? something went very wrong here...')
            vid_url = None
        return vid_url

    # link contains output filename
    def download(self, link, url):
        print("downloading '{}'...".format(url))
        if url is None:
            print('nevermind.')
            return False
        try:
            video_handle = urllib2.urlopen(url, timeout=60)
        except urllib2.URLError, e:
            print('URLError = ' + str(e.reason))
            return False

        target = "output/" + re.sub('.*\d+-', '', link) + '.mp4'
        if re.match('.*https://www\.masterani\.me.*', target):
            print("target = '{}', aborting".format(target))
            return False
        show_dir = os.path.dirname(target)
        if not os.path.exists(show_dir):
            os.mkdir(show_dir)
        with open(target, 'wb') as output:
            while True:
                try:
                    # don't load whole file into memory
                    data = video_handle.read(8192)
                except Exception:
                    output.close()
                    os.remove(target)
                    return False
                if data:
                    output.write(data)
                else:
                    break
        return True

    def set_as_completed(self, link):
        self.goto(link)
        checkbox_elem = self.get_by_xpath('check_box')
        if checkbox_elem is None:
            return False
        checkbox_elem.click()
        time.sleep(5)
        return True

    def goto(self, link):
        self.driver.get(link)

    def close(self):
        self.driver.quit()

    def get_by_xpath(self, field, timeout=30, hard_fail=False):
        fields_dict = {
                    'login' : '//*[@id="navigation"]/div[1]/div[2]/a',
                    'username' : '/html/body/div[2]/div/div[2]/form/div[1]/div/input',
                    'password' : '/html/body/div[2]/div/div[2]/form/div[2]/div/input',
                    'submit' : '/html/body/div[2]/div/div[2]/form/div[3]/button',
                    'profile' : '//*[@id="navigation"]/div[1]/div[2]/div[1]/a[1]',
                    'frame' : '//*[@id="watch"]/div/div[1]/div/div[3]/div[2]/div/iframe',
                    'host' : '//*[@id="host-dropdown"]/div/div[1]',
                    'quality' : '//*[@id="quality-dropdown"]/div/div[3]',
                    'video_mp4upload' : '//*[@id="player"]/div[2]/video',
                    'frame_masteranime' : '//*[@id="video_html5_api"]',
                    'check_box' : '//*[@id="watch"]/div/div[2]/div/div[2]/a[1]',
                 }
        # if not in fields list,
        if field.lower() not in fields_dict:
            # perform **VERY** weak XPath conformance check (don't be dumb):
            if field[:1] != '/':
                return
            xpath = field
        else:
            xpath = fields_dict[field]

        count = 0
        while True:
            try:
                elem = self.driver.find_element_by_xpath(xpath)
                return elem
            except Exception:
                time.sleep(1)
                count += 1
            if count > timeout:
                if hard_fail:
                    print("couldn't fetch '{}' field after {}s. quitting.".format(field, timeout))
                    self.close()
                    sys.exit(1)
                return



iface = MasteranimeDL()
iface.login(str(raw_input('Email: ')), getpass())
# customization
# You /could/ hard-code your password here, but should you? NO.
#iface.login('YourEmailHere@example.com', getpass())
iface.get_everything()
iface.close()
print('\nAll done!')


