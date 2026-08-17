import base64

cypher_text = "R1xbW3pndkhFBV9BCmxTAFtZZ0AJRANBaAIBBloEAQUASA=="
plain_text = "picoCTF{"

payload = base64.b64decode(cypher_text)

result = ""

for i in range(len(plain_text)):
    key = chr(payload[i] ^ ord(plain_text[i]))
    result += key

print(result)