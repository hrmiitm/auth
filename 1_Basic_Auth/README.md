# Flask HTTP Basic Auth Demo

A minimal Flask app showing how HTTP Basic Authentication works.

## 🚀 Features

* Protect routes using a custom `@basic_auth` decorator
* Reads credentials via `request.authorization`
* Triggers browser login popup using `WWW-Authenticate` header

## ⚙️ How It Works

1. User accesses a protected route
2. Decorator checks for credentials
3. If missing/invalid → returns `401 Unauthorized`
4. Browser shows login popup
5. Credentials sent as: `username:password` → Base64 encoded
6. Browser stores credentials in memory `(per **realm**)`
7. Same realm → no re-login, different realm → asks again
8. Server decodes + validates (`hrm` / `h`)
9. Access granted if valid

## 🧪 Quick Start

```bash
python main.py
```

Open: [http://localhost:5000/dashboard](http://localhost:5000/dashboard)

**Login:**

* Username: `hrm`
* Password: `h`

## 🔐 Logout Behavior

* Browser caches credentials (in memory)
* No true logout in Basic Auth
* To simulate logout:

  * Force `401 Unauthorized` response
  * OR close the browser/tab

## ⚠️ Security Note

* Basic Auth = **Base64 encoding (not encryption)**
* Credentials can be easily decoded if intercepted
  * Go to Network tab --> In Request Headers --> `Authorization:Basic aHJtOmg=`
  * ```bash
bitun@bitcn:~/Documents/Jan2026/TDS/auth$ echo -n "hrm:h" | base64
aHJtOmg=
bitun@bitcn:~/Documents/Jan2026/TDS/auth$ echo -n "aHJtOmgK" | base64 --decode
hrm:h
```
* Always use **HTTPS** in production
