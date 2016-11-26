from django.shortcuts import render
from django.http import HttpResponse
#import requests
import urllib2
from .models import Greeting
from .models import Document

import json
import hashlib
from pycoin.key.BIP32Node import BIP32Node



COIN_NETWORK = "BTC" # XTN for testnet!

def sha256_checksum(file, block_size=65536):
    sha256 = hashlib.sha256()
    # with open(file,mode='r', buffering=-1) as f:
    for block in iter(lambda: file.read(block_size), b''):
        sha256.update(block)
    return sha256.hexdigest()

# Create your views here.
def index(request):
    return HttpResponse('#RegHackTo!')
    #return render(request, 'index.html')



def hashme(request):
    if request.method == 'POST':
        print "hashme: %s" %request.POST
        try:
            file_url = request.POST.get('file_url', "http://blog.theshayan.com/wp-content/uploads/2015/11/3-940x429.png")
        except Exception, e:
            print "failed to get url %s " %e
            return HttpResponse(json.dumps({"status":"failed", "reason": e.message}), content_type="application/json", status = 400)

        r = urllib2.urlopen(file_url)
        ret_json = {}
        if request.POST.get('file_url', None) is None:
            ret_json['file_url_missing'] = 'using_testimage'
            ret_json["status"] = "default"

        file_hash = sha256_checksum(r)
        ret_json["hash"] = file_hash
        ret_json["status"] = "success"
        print ret_json
        return HttpResponse(json.dumps(ret_json), content_type="application/json", status = 200)

    return HttpResponse(json.dumps({"error":"no Get request"}), content_type="application/json", status = 400)






########################## BIP32 stuff ##############################

def get_address_by_path(wallet_key, path):
    '''
    gets wallet_key = xpub or xpriv and path
    returns JSON
    xprv: {"address":"1qwerty...", "priv_key":"Kqwert...", "path":"1/2"}
    xpub: {"address":"1qwerty...", "priv_key":None, "path":"1/2"}
    '''
    da_key = BIP32Node.from_wallet_key(wallet_key)
    btc_address = da_key.subkey_for_path(path).bitcoin_address()
    btc_private = da_key.subkey_for_path(path).wif()
    return {"address":btc_address, "priv_key":btc_private, "path":path}




def gpg_entropy():
    try:
        output = subprocess.Popen(
            ["gpg", "--gen-random", "2", "64"], stdout=subprocess.PIPE).communicate()[0]
        return output
    except OSError:
        sys.stderr.write("warning: can't open gpg, can't use as entropy source\n")
    return b''


def get_entropy():
    entropy = bytearray()
    try:
        entropy.extend(gpg_entropy())
    except Exception:
        print("warning: can't use gpg as entropy source")
    try:
        entropy.extend(open("/dev/random", "rb").read(64))
    except Exception:
        print("warning: can't use /dev/random as entropy source")
    entropy = bytes(entropy)
    if len(entropy) < 64:
        raise OSError("can't find sources of entropy")
    return entropy



def create():
    max_retries = 64
    for _ in range(max_retries):
        try:
            return BIP32Node.from_master_secret(get_entropy(), netcode=COIN_NETWORK)
        except ValueError as e:
            continue
    raise e


def create_newkey(name = None):
    bip32_key = create()
    xpub = bip32_key.wallet_key(as_private=False)
    xprv = bip32_key.wallet_key(as_private=bip32_key.is_private())
    print xpub
    print xprv



#ret_key = get_address_by_path(key, path)



#
# def list(request):
#
#     documents = Document.objects.all()
#     ret_json = []
#     for document in documents:
#         ret_json.append({'name': document.docfile.name,
#                          'url': document.docfile.url,
#                          'hash': document.hash,
#                          'upload_time': document.upload_time})
#     return HttpResponse(json.dumps(ret_json), content_type="application/json")
#



# def db(request):
#
#     greeting = Greeting()
#     greeting.save()
#
#     greetings = Greeting.objects.all()
#
#     return render(request, 'db.html', {'greetings': greetings})
#