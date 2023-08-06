# For use within Django.
# settings.py module
# substitute values

# top of settings.py file

# The JSON file can contain any name:value pair
# and any number of them.

# Guarded Settings reads the JSON file
# named guardedsettings.json and creates
# a Python dictionary.
# Use the dictionary name to obtain the value.

from UA_GuardedSettings import guardedsettings
gs = guardedsettings.guardedsettings()


SECRET_KEY			= gs.SettingsDictionary['SecretKey']


DATABASES

'PASSWORD'	: gs.SettingsDictionary['databasePassword'],