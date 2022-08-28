# pip install translate-api
import translators as ts

if __name__ == '__main__':
    print(ts.google("Salut tout le monde !", from_language="FR", to_language="EN"))
