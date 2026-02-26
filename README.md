## Messenger – private family chat

Lightweight Django + Channels app for **private, ephemeral 1:1 family chat**:

- Username + password only (no email, no avatars).
- No message history (nothing stored in the DB).
- WebSocket real‑time chat with online status and typing indicator.
- Per‑room client‑side encryption (browser encrypts text before sending).
- Mobile‑friendly UI with light/dark mode.

---

## Requirements

- Python 3.11 (or any Python 3.10+ that works with Django 5).
- Virtual environment (recommended).
- Python packages (from `requirements.txt`):

```text
django>=5.0,<6.0
channels>=4.0,<5.0
daphne>=4.0,<5.0
```

---

## Run locally

From the project root (where `manage.py` lives):

1. **Create and activate a virtualenv**

   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   # source venv/bin/activate  # macOS/Linux
   ```

2. **Install dependencies**

   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

3. **Apply migrations**

   ```bash
   python manage.py migrate
   ```

   The DB is only used for users and rooms (no messages are stored).

4. **Run the ASGI server (Daphne)**

   ```bash
   daphne messenger.asgi:application
   # or specify port:
   # daphne -p 8000 messenger.asgi:application
   ```

5. **Use the app**

   - Open `http://127.0.0.1:8000/`.
   - Register (first name, username, password).
   - Share the app on your home network and have family register.
   - On the Chats page, start a room by entering a username and then chat in real time.

---

## How privacy works (short)

- **No history**: messages are never written to the database; refreshing the page clears the conversation.
- **Encryption**:
  - Each room has its own random secret stored on the `Room` model.
  - The browser derives an AES‑GCM key from that secret and encrypts message text before sending.
  - The server only relays ciphertext and does not store it.
  - This is an extra privacy layer, but not full end‑to‑end encryption (the secret is available to the server and client code).

---

## Notes for deployment

- You need an ASGI‑capable environment (Daphne, Uvicorn, or host with Django Channels support).
- On platforms like PythonAnywhere, configure an **ASGI web app** pointing at `messenger.asgi:application` and install `requirements.txt` in your virtualenv.

