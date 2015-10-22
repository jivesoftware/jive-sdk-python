import jive_sdk


# 
#clientSecret
#e4b60fc5c947566c8efe76f3efcd89297d609c6a943dd60713786b272142e4a9
#jiveSignatureURL
#https://market.apps.jivesoftware.com/appsmarket/services/rest/jive/instance/validation/8ce5c231-fab8-46b1-b8b2-fc65deccbb5d
#timestamp
#2015-10-20T05:51:30.568+0000
#clientId
#mwagsufbcqzcqlgnmuzbag04kq41qspa.i
#tenantId
#b22e3911-28ef-480c-ae3b-ca791ba86952
#jiveUrl
#https://sandbox.jiveon.com
authorization = "JiveEXTN algorithm=HmacSHA256&client_id=mwagsufbcqzcqlgnmuzbag04kq41qspa.i&jive_url=https%3A%2F%2Fsandbox.jiveon.com&tenant_id=b22e3911-28ef-480c-ae3b-ca791ba86952&timestamp=1445320336251&signature=5Tl8lzbV10LJd1zxkcS2OlqkdfkDsl62OC5rlmZuHaM%3D"
clientId = "mwagsufbcqzcqlgnmuzbag04kq41qspa.i"
clientSecret = "i8ioi18b4rn8mh95nkblzpj03hdrf2rz.s"

if jive_sdk.is_valid_authorization(authorization, clientId, clientSecret):
    print("Success")

