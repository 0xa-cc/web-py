#coding=utf8

from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
import base64

#google play
# GGPLAY_PUBLIC_KEY='MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAmmh0cyNTzc1S+zoa5JheTGzr8V8nyc6FvyDA560qNtDnAKeU751PRcyzH2JjxBKmnxOZNK1+nlwbrYF5KJ6lBbuJ24Ye3997UFodAaF6Seu36oj2zpyR1k+QzteeQCEs14T05cFbk/5x6vCm7ezEUpD6+5sZv0ZZ2m8VPBXkLD7i6UU1Pr8+aN3I339RCU0wfyRJcuDKgd+OBOpishsQBeXhhJmdojqlnsmR0SkgNavPJZbG8JzVDTwJ7raquDqbjiy2UpeS46s9jWS0Hch/7sxRKX6oiGYqW+kDBnB6phCub8TGhrQeKGWTblmh/JrG3NIknelfirE4aae269+N9QIDAQAB'
GGPLAY_PUBLIC_KEY='MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAsVgSKV+i9RSAKiFbGoj6JvrOyJqqyN6jBJpZ/NdXZP5c9jEfA4sKvoaFohR8HOb+t+oqJESp6fs+UPrVelBPm0dbI9huJe+GRbdiULWgB3dmiLARv3uXAZ1XFqJxvfJoOE+F8KVl0RaTfU1fqsmg4vRvyOHg/QvgYGo2NTNUGeIommmf09WnL+IXHWBJ/PG7VXETkI+211yx/zlMXfbNRJWClcUh5GZ5X/kXj6hXWGKsgCzIO7H4hAP/6ePWY1daCopFYYupC2LfWVKiIYo2Wh+bXuNaixbJVHqPlBd+GuAcEDEhviHojOP49GjBRybGAiiZrsroap9ahDzxGC18VwIDAQAB'
GGPLAY_VERIFY_KEY= RSA.importKey(base64.decodestring(GGPLAY_PUBLIC_KEY))

#google play验证签名数据
def ggplay_verify(message, signature):
    '''Verify that signature is the result of signing message'''
    # Get the hash of the message
    h = SHA.new(message)
    # Create a verifier
    verifier = PKCS1_v1_5.new(GGPLAY_VERIFY_KEY)
    # decode the signature
    signature = base64.decodestring(signature)
    # verify
    if verifier.verify(h, signature) == True:
        return True
    else:#签名不对时还有返回0的情况
        return False
    
if __name__ == '__main__':
   # strMsg = '{"orderId":"12999763169054705758.1336765116266576","packageName":"com.pokerxo.com","productId":"pokerxo.goldcoin.1","purchaseTime":1364802898000,"purchaseState":0,"developerPayload":"abcdefghijk","purchaseToken":"bsqmyqimmkkjmaukozbmzdld.AO-J1OwvL8XlSH8UQbC6lSiVfBzvtrGJlHw9YF_p1O3vyQVFnaLWdrjmgG1ucMhpIAy4zKJ6-aymwNBJTAydoQ3N_dHS-R99rpDOr1dasbOLOh3oWtUI7ZH76OIXMGP-SIVUkjazpZAg"}'
   # strSign = 'g1L3OaSKW7W5sf2uGkmW/n4KZZKJgSRaqkvhS2eW0dnp0vJrz3A7o523Qvezs+bOztqDUotUD4WFTkpnx5xEqCNQz81nXzGhGw8X6F4AToPY6SVShO4tIfSDHCMOj0qcWt2TQjEQxS2BwGgH0U+aJp4fzD9HvaoezPKIOZ/FfG7TBhPFUhFCPk49L6cAKHXS8vI7kwZXzXHI8NPbjrgeicMSfPJZgdLnn7IVERsxWbaQ4UM5VUg1TINOvrGZZ2htaZ3lO8a4JXjZELYKa/YzfBpcZGh0IRP8zb7AyVi1PiHlTHDcnD62+WdK6pVqRQhFjXPTWz64Jyrqn5m1rkA3Lg=='
   strMsg ='{"orderId":"12999763169054705758.1368070253305897","packageName":"com.ourgame.pokermonster","productId":"gg.lzdzpk.01","purchaseTime":1436951766965,"purchaseState":0,"developerPayload":"CBBD42D476AC08D0","purchaseToken":"dmaifgigocfcdhfhpgpjjnfh.AO-J1OyYxSnChii-Tu0cHmMNf0XwgNQItAvVwJqHcU5tHDX9jQPtrHSL7ytE_GhiOtDcCferqqTm2GU_OYNggV2bb8V5_5sfc7gD4PXzsjsPMs5v9TQApFDFLI6M1oRDX7Qv51GZi0JP"}'
   strSign = 'rJPENtC4spH3YLZUjFEGhapL1gjxwnngimsbcsgAaBcGDZFCf8vQsaenGHwY6zKakg7amJFykgNloMuczQVctScBDpkEz8dO1dvfd5Va7cKHtE+ulnDEezBGuMG1V1w+xHiHbq8ui74YRbDFDr16VL+RBSjhF45gYhUU2obuSD/EFTK7dP+PKlxoAhUAnhlSf/dxzMBJH1TQ15kgwUjsyNfX2YSjNgXk4gVCevlvfE0aTID//59NckrtrFSAFkys0LssBI+ud8m1N6Wau0U2pTDKyNVO9Gp1RlmYJQUErHb+bpuqXJG8YsNZwJ4inRfuiVfa071XjGVCSoGlpgQG6Q=='
   print(ggplay_verify(strMsg, strSign))



