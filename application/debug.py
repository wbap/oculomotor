import ptvsd
from server import app

if __name__ == '__main__':
    print("waiting....")
    ptvsd.enable_attach("my_secret", address=('0.0.0.0', 3000))
    ptvsd.wait_for_attach()

    app.run(host='0.0.0.0', port=80)
