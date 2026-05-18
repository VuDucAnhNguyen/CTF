## voice-in-the-packet
### Đề bài
I intercepted a suspicious phone call over the network. something tells me there's more to this conversation than meets the ear...

### Giải
Sau khi tải về thì được file `call.pcap`. Kiểm tra bằng wireshark thì thấy 2 gói tin đầu và cuối chứa fake flag, còn lại từ gói tin 2 đến 1001 là giao thức UDP từ ip `192.168.1.100:10000` đến `192.168.1.100:20000`
```
#fake flag
tjctf{this_is_a_fake_flag_keep_looking}
tjctf{definitely_not_the_real_flag}
```

Đề bài có nhắc đến gọi điện qua ip nên mình nghĩ đến giao thức RTP. Kiểm tra thì đúng các gói tin UDP từ 2 đến 1001 có header của RTP. Thực hiện trích xuất dữ liệu RTP này
``` python
from scapy.all import rdpcap, UDP
import audioop, wave

pkts = rdpcap("call.pcap")
packets = [p for p in pkts if p[UDP].sport == 10000]

payloads = []
for pkt in packets:
    data = bytes(pkt[UDP].payload)
    payloads.append(data[12:])  # skip RTP header

raw_ulaw = b''.join(payloads)
pcm_data = audioop.ulaw2lin(raw_ulaw, 2)

with wave.open('audio.wav', 'wb') as wf:
    wf.setnchannels(1)    # mono
    wf.setsampwidth(2)    # 16-bit
    wf.setframerate(8000) # 8kHz (VoIP G.711 standard)
    wf.writeframes(pcm_data)
```

Sau khi kiểm tra âm thanh, waveform và spectrogram của `audio.wav` không có gì mình thử LSB từ raw. Kết quả thu được trong file `LSB.bin` có chuỗi base64 là flag
``` python
from scapy.all import rdpcap, UDP
from pathlib import Path

pkts = rdpcap("call.pcap")
packets = [p for p in pkts if p[UDP].sport == 10000]

payloads = []
for pkt in packets:
    data = bytes(pkt[UDP].payload)
    payloads.append(data[12:])  # skip RTP header

bits = []
for payload in payloads:
    for i in range(0, len(payload), 2):
        bits.append(payload[i] & 1)

raw = bytearray()
for i in range(0, len(bits) - 7, 8):
    val = int(''.join(str(b) for b in bits[i:i+8]), 2)
    raw.append(val)

Path("LSB.bin").write_bytes(bytes(raw))
```
`dGpjdGZ7aDN5X3YwaXBfczczZ19pc180XzdoaW5nfQ==`

FLAG: **tjctf{h3y_v0ip_s73g_is_4_7hing}**
