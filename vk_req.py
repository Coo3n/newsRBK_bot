import random
import threading
import time
from threading import *
import requests
import os
from config import vk_token


def get_latest_posts(group_name):
    url = f"https://api.vk.com/method/wall.get?domain={group_name}&count=10&access_token={vk_token}&v=5.81"
    req = requests.get(url)
    src = req.json()

    posts = src["response"]["items"]

    result = []

    for post in posts:
        try:
            if "attachments" in post:
                post = post["attachments"]
            if post[0]["type"] == "photo":
                result.append(post[0]["photo"]["sizes"][-1]["url"])

        except Exception:
            print("Oups!")

    return result


class ImageCacheController:
    groups = []

    cacheSize = []

    def __init__(self, source_groups_file):
        source_groups_ids = open(source_groups_file, 'r')
        self.groups = source_groups_ids.readlines()
        print(f"Number of tracking groups: {len(self.groups)}.")
        for group in self.groups:
            self.cacheSize.append(0)
            group = group.strip('\n')
            if not os.path.exists(rf"images_cache_controller\images_cache\{group}.txt"):
                f = open(rf"images_cache_controller\images_cache\{group}.txt", "w+")
                print(f"Cache file for {group} created!")
            else:
                print(f"Cache file for {group} already exists.")
        self._update_thread()

    def _update_thread(self):
        group_number = 0
        for group in self.groups:
            group = group.strip('\n')
            latests_posts_images = get_latest_posts(group)
            with open(rf"images_cache_controller\images_cache\{group}.txt", "w+") as file:
                for post in latests_posts_images:
                    file.writelines(post + '\n')
            print(f"Cache file for {group} updated!")
            self.cacheSize[group_number] = len(latests_posts_images)
            group_number += 1

    def start(self):
        flag = Event()
        thread = self.MyThread(flag)
        thread.run()
        # Thread(target=self._update_thread()).start()

    def get_image(self):
        print(f"{len(self.groups)} {self.cacheSize[0]} {self.cacheSize[1]}")
        random_group_number = random.randint(0, len(self.groups) - 1)
        sus = self.groups[random_group_number].strip('\n')
        print(f"{sus} ++")
        return self.get_image_from_group(random_group_number).strip('\n')

    def get_image_from_group(self, group):
        print(f"{self.cacheSize[group]}++")
        group_name = self.groups[group].strip('\n')
        f = open(rf"images_cache_controller\images_cache\{group_name}.txt", "r")
        random_image_number = random.randint(0, self.cacheSize[group]-1)
        for i in range(random_image_number-1):
            f.readline()
        image_url = f.readline()
        return image_url