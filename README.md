A simple websocket server to demonstrate websocat

To use, install the packages with `pip install -r requirements.txt` and run `uvicorn main:app --reload`.
To connect, run `websocat ws://localhost:8000 -0` while the server is up.

The ASCII animation code is from [tpoff on GitHub](https://github.com/tpoff/Python-Gif-Ascii-Animator/tree/master), and the websocat binary is from [vi on GitHub](https://github.com/vi/websocat).