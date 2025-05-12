import requests

url = "wss://melbet-uz-1.com/games-frame/sockets/crash"

querystring = {
    "whence": "55",
    "fcountry": "192",
    "ref": "8",
    "gr": "1521",
    "appGuid": "games-web-app-unknown",
    "lng": "uz",
    "access_token": "eyJhbGciOiJFUzI1NiIsImtpZCI6IjEiLCJ0eXAiOiJKV1QifQ.eyJzdWIiOiI1MC84NTYxMzM4ODciLCJwaWQiOiI4IiwianRpIjoiMC8yYzU0ZTRmMDFkOGNkZjZlYTFlOTkxOTdkNjA3ODlmMTAzY2JjOTYzNGJjZGM5ZGM4YWEzZDk1NjM5ODVlZTE3IiwiYXBwIjoiTkEiLCJpbm5lciI6InRydWUiLCJuYmYiOjE3NDY4MjA5OTgsImV4cCI6MTc0NjgzNTM5OCwiaWF0IjoxNzQ2ODIwOTk4fQ.2iG0SO-Gm0nQXpNScXyyI6reG3DVdNMV4LpsSTRCSDffFRl1-PiMU8UN6GDZ1fRnasT-28kM0Dre70O_eJ0Z7g"
}

headers = {
    "host": "melbet-uz-1.com",
    "connection": "Upgrade",
    "pragma": "no-cache",
    "cache-control": "no-cache",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0",
    "upgrade": "websocket",
    "origin": "https://melbet-uz-1.com",
    "sec-websocket-version": "13",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "en-US,en;q=0.9",
    "cookie": "platform_type=desktop; lng=uz; cookies_agree_type=3; tzo=5; is12h=0; auid=LiC3gGgeXWCzmpEBAznOAg==; che_g=bab392ec-fca5-df0e-5d63-6b103203ef6d; sh.session.id=e465ff2d-efcc-4f0a-b5e0-f15aa44e0c63; sh.message_sound_active=1; application_locale=uz; PAY_SESSION=5df2be672238a6982188d0aab614ce31; _gcl_au=1.1.355112690.1746820462; _gid=GA1.2.1128368004.1746820463; _hjSessionUser_5352645=eyJpZCI6ImUxMTZkYjA4LWZjOTctNTc0OC05OGNkLTgwMjk4ZTI4NmY5YSIsImNyZWF0ZWQiOjE3NDY4MjA0NjM3MTUsImV4aXN0aW5nIjpmYWxzZX0=; _fbp=fb.1.1746820463740.121695555208657554; x-banner-api=; _ga=GA1.2.1035960047.1746820462; ua=856133887; uhash=c788a6d570683526bc8d964abeab2365; cur=UZS; user_token=eyJhbGciOiJFUzI1NiIsImtpZCI6IjEiLCJ0eXAiOiJKV1QifQ.eyJzdWIiOiI1MC84NTYxMzM4ODciLCJwaWQiOiI4IiwianRpIjoiMC8yYzU0ZTRmMDFkOGNkZjZlYTFlOTkxOTdkNjA3ODlmMTAzY2JjOTYzNGJjZGM5ZGM4YWEzZDk1NjM5ODVlZTE3IiwiYXBwIjoiTkEiLCJpbm5lciI6InRydWUiLCJuYmYiOjE3NDY4MjA5OTgsImV4cCI6MTc0NjgzNTM5OCwiaWF0IjoxNzQ2ODIwOTk4fQ.2iG0SO-Gm0nQXpNScXyyI6reG3DVdNMV4LpsSTRCSDffFRl1-PiMU8UN6GDZ1fRnasT-28kM0Dre70O_eJ0Z7g; SESSION=e271fe5abaf9d582952645a142bf741f; window_width=759; _ga_435XWQE678=GS2.1.s1746820461$o1$g1$t1746821278$j20$l0$h0; _ga_8SZ536WC7F=GS2.1.s1746820463$o1$g1$t1746821278$j3$l1$h1628566287",
    "sec-websocket-key": "h8ueLYZScFBp5GXSjwqjhQ==",
    "sec-websocket-extensions": "permessage-deflate; client_max_window_bits"
}

response = requests.get(url, headers=headers, params=querystring)

print(response.text)