import random
from pkcs7Pad import pkcs7Pad, pkcs7Strip
from Cryptodome import Random
from Cryptodome.Cipher import AES


class ProfileManager:
    def __init__(self, admin):
        self.aesEcb = AES.new(Random.get_random_bytes(
            AES.block_size), AES.MODE_ECB)
        self.userIdDict = {admin: 10}
        self.adminEmail = admin

    def addToUserDict(self, email):
        while True:
            r = random.randint(11, 99)
            if r not in self.userIdDict.values():
                self.userIdDict[email] = r
                break

    def profile_for(self, email):
        if email not in self.userIdDict:
            self.addToUserDict(email)

        profile = {'email': email, 'uid': self.userIdDict[email]}
        if email == self.adminEmail:
            profile['role'] = 'admin'
        else:
            profile['role'] = 'user'

        return self.encryptProfile(encodeCookie(profile))

    def encryptProfile(self, profile):
        return self.aesEcb.encrypt(pkcs7Pad(profile.encode('utf-8'), AES.block_size))

    def decryptProfile(self, encryptedProfile):
        encodedProfilewPad = self.aesEcb.decrypt(encryptedProfile)
        encodedProfile = pkcs7Strip(encodedProfilewPad, 16).decode('utf-8')
        profile = decodeCookie(encodedProfile)

        email = profile['email']
        if profile['role'] == 'admin':
            print(f'Email: {email}, ACESS GRANTED')
        else:
            print(f'Email: {email}, ACESS DENIED')


def removeMeta(s, meta):
    if type(s) == type('string'):
        for char in meta:
            s = s.replace(char, '\"' + char + '\"')
    return s


def addMeta(s, meta):
    if type(s) == type('string'):
        for char in meta:
            s = s.replace('\"' + char + '\"', char)
    return s


def metaSplit(s, char):
    resultList = []
    prev = 0
    for i in range(len(s)):
        if s[i] == char and s[i+1] != '\"':
            resultList.append(s[prev:i])
            prev = i + 1
    resultList.append(s[prev:])
    return resultList


def encodeCookie(cookie):
    result = ''
    for key, value in cookie.items():
        key = removeMeta(key, '&=')
        value = removeMeta(value, '&=')
        result += str(key) + "=" + str(value) + "&"
    return result[:-1]


def decodeCookie(encodedCookie):
    itemList = metaSplit(encodedCookie, '&')
    result = {}
    for pair in itemList:
        key, value = metaSplit(pair, '=')
        key = addMeta(key, '&=')
        value = addMeta(value, '&=')
        result[key] = value
    return result


def ecbCutPaste(manager):
    adminEmail = 'admin@admin.com'
    attackEmail = 'michael_scott@dundermifflin.com'
    assert (len(attackEmail) - len(adminEmail)) % AES.block_size == 0

    adminProfile = manager.profile_for(adminEmail)
    attackProfile = manager.profile_for(attackEmail)

    print('Before cut & paste')
    manager.decryptProfile(attackProfile)
    fakeProfile = attackProfile[:-AES.block_size] + \
        adminProfile[-AES.block_size:]
    print('After cut & paste')
    manager.decryptProfile(fakeProfile)


if __name__ == "__main__":
    manager = ProfileManager('admin@admin.com')
    ecbCutPaste(manager)
