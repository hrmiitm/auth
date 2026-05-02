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
```bash
bitun@bitcn:~/Documents/auth$ echo -n "aHJtOmg=" | base64 --decode
hrm:hbitun@bitcn:~/Documents/auth$ echo -n "hrm:h" | base64
aHJtOmg=
```  
* Always use **HTTPS** in production

## *Note: Base64 is strictly encoding, and it is NOT encryption.*
- Encoding: Translate data usig public, universally known dictionary(the Base64 Index, in case of base64 encodding).
- Encryption: Reversiable Function but require password to decrypt.
- Hashing: One Way Function, cannot be decrypted

---

# How "hrm:h" is Encoded into Base64

Base64 is essentially a translation process: it takes raw data, turns it into a stream of 1s and 0s, and then chops that stream up into new chunks to assign them readable characters.

Here is the exact step-by-step breakdown of how the string **"hrm:h"** becomes **"aHJtOmg="**.

### Step 1: Characters to ASCII
First, the computer translates each character into its standard decimal ASCII value.

| Character | ASCII Decimal |
| :---: | :---: |
| h | 104 |
| r | 114 |
| m | 109 |
| : | 58 |
| h | 104 |

### Step 2: ASCII to 8-bit Binary
Next, those decimal numbers are converted into 8-bit binary (1s and 0s). 

* h = `01101000`
* r = `01110010`
* m = `01101101`
* : = `00111010`
* h = `01101000`

If we line them all up, we get a continuous stream of 40 bits:
`0110100001110010011011010011101001101000`

### Step 3: Regroup into 6-bit Chunks
This is the core trick of Base64. Standard text uses 8 bits per character, but Base64 groups bits by **6** (since 2⁶ = 64 possible characters in its alphabet). We take our 40 bits and slice them into 6-bit chunks:

`011010` | `000111` | `001001` | `101101` | `001110` | `100110` | `1000`

**Notice the very last group:** It only has 4 bits (`1000`). Because Base64 strictly requires groups of 6, we pad the end with two zeros to complete it: `100000`.

### Step 4: 6-bit Binary to Decimal
Now, we convert those new 6-bit chunks back into regular decimal numbers.

* `011010` = **26**
* `000111` = **7**
* `001001` = **9**
* `101101` = **45**
* `001110` = **14**
* `100110` = **38**
* `100000` = **32**

### Step 5: Map to the Base64 Index
Base64 has its own alphabet index (A-Z are 0-25, a-z are 26-51, 0-9 are 52-61, `+` is 62, and `/` is 63). We map our new decimal numbers to this table:

* 26 -> **a**
* 7 -> **H**
* 9 -> **J**
* 45 -> **t**
* 14 -> **O**
* 38 -> **m**
* 32 -> **g**

So far, we have **`aHJtOmg`**.

### Step 6: Final Padding (`=`)
Base64 processes data in blocks of 3 bytes (24 bits) at a time.

* Your first three letters (`hrm`) made up exactly 3 bytes. Perfect.
* Your last two letters (`:h`) made up only 2 bytes. 

When the final block of text is missing 1 byte, Base64 adds a single equals sign (`=`) to the end of the final output as a mathematical placeholder so the system knows how to decode it later. *(If it were missing 2 bytes, it would add `==`)*.

Add the padding to our translated letters, and the final encoded result is: 

**`aHJtOmg=`**

# How "aHJtOmg=" is Decoded from Base64

Decoding Base64 reverses the encoding process. It turns the Base64 characters back into a continuous binary string, and then regroups that string into standard 8-bit characters.

Here is the exact step-by-step breakdown of how the Base64 string **"aHJtOmg="** becomes **"hrm:h"**.

### Step 1: Remove Padding & Identify Characters
First, we look at the string: `aHJtOmg=`. 
The `=` at the end is just a padding placeholder indicating that 2 extra zero-bits were added during encoding. We remove the `=` for now and focus on the actual Base64 characters: **a, H, J, t, O, m, g**.

### Step 2: Map Base64 Characters to Decimal
Using the standard Base64 index (A-Z are 0-25, a-z are 26-51, 0-9 are 52-61, `+` is 62, and `/` is 63), we find the decimal value for each character.

| Base64 Char | Decimal Value |
| :---: | :---: |
| a | 26 |
| H | 7 |
| J | 9 |
| t | 45 |
| O | 14 |
| m | 38 |
| g | 32 |

### Step 3: Decimal to 6-bit Binary
Next, we convert those decimal numbers back into 6-bit binary chunks.

* 26 -> `011010`
* 7 -> `000111`
* 9 -> `001001`
* 45 -> `101101`
* 14 -> `001110`
* 38 -> `100110`
* 32 -> `100000`

If we link them all together, we get a 42-bit continuous stream:
`011010000111001001101101001110100110100000`

### Step 4: Discard Padding Bits
Because we had one `=` sign at the end of our original string, we know the very last 2 bits are just artificial padding. 
We drop the last two `0`s from the end of the string, leaving us with our original **40 bits**:

`0110100001110010011011010011101001101000`

### Step 5: Regroup into 8-bit Bytes
Standard computer text uses 8 bits per character (ASCII). We take our 40-bit string and slice it into 8-bit blocks:

`01101000` | `01110010` | `01101101` | `00111010` | `01101000`

### Step 6: 8-bit Binary to ASCII Decimal
Now we convert those 8-bit binary chunks back into standard decimal numbers.

* `01101000` = **104**
* `01110010` = **114**
* `01101101` = **109**
* `00111010` = **58**
* `01101000` = **104**

### Step 7: Map Decimal to ASCII Text
Finally, we translate those ASCII decimal numbers back into standard text characters.

* 104 -> **h**
* 114 -> **r**
* 109 -> **m**
* 58 -> **:**
* 104 -> **h**

The decoded string is exactly what we started with: **`hrm:h`**
