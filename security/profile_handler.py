import json

import security.player_profile as player_profile

__FILE_PROFILES_PATH = r".\data\server\profiles\profiles.json"

def use_profile(user, password):
    for profile in __get_profiles():
        if(profile.user == user):
            if(profile.password == password):
                return (True, "", profile)
            else:
                return (False, "wrong password", None)
    return (False, "not found", None)

def exists(user):
    pass

def __get_profiles():
    profiles = []
    with open(__FILE_PROFILES_PATH, "a+") as file:
        file.seek(0)

        json_profiles = json.loads(file.read())["profiles"]
        for raw in json_profiles:
            profiles.append(player_profile.deserialize(raw))

    return profiles
