# SecureBoard V1

This is a clean rollback-style version of SecureBoard before the attempted upgrades.

It includes:

- Public message board
- Admin login
- Admin logs page
- JSON-based logging

It does not include:

- Admin moderation tools
- Threat score
- Better tests
- Blocked IP logic

## Run

```bash
pip install -r requirements.txt
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

Admin login:

```text
http://127.0.0.1:5000/admin
```

Default credentials:

```text
Username: codexcapital
Password: Testing123
```
