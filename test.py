#test.py

import senko

GITHUB_URL = "https://github.com/gitkh2891/EV-IOT/"
OTA = senko.Senko(url=GITHUB_URL, files=["test.py"])

print("hello world 123")