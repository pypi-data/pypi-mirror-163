# Secure-hashing
A library used for secure password storage. Feel free to look around the source code, there is not a lot. This library also supports peppers, if you don't know what that is i suggest you look at this: https://en.wikipedia.org/wiki/Pepper_(cryptography)

Word of safety: always practice cryptography with great care.

# Requirements
bcrypt

hmac

# Usage
```python
import secure_hash as sh
sh.hash_high(plaintext)
```

# Documentation
```python
get_salt(hash)
```
Returns the salt used in the hash.

```python
hash_high(password, pepper="", rounds=None)
```
Returns a hashed password. Rounds parameter is used to specify how many rounds should be used in salt generation.

```python
verify_high(password, hash0, pepper="")
```
Returns True if the password matches the hash.

```python
hash_low(password, salt, pepper="")
```
Returns a hashed password.

```python
verify_low(password, hash0, salt, pepper="")
```
Returns True if the password matches the hash.

# Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install Secure-hashing.

```bash
pip install securehashing
```