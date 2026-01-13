### ISSUES FACED
- Running this application in Brave browser(TTS is'nt working for me)
- Implementation - has more prerequisites for understanding its full implementation

### STEPS 
- **1:** 
    first I build a multi-agent sample project that answers user query for health issue (tool 1), 
    or to process arithmetic (tool 2).

- **2:** 
    Then I learnt about web-sockets, real time API for understanding RAGENT.
    Learnt its basics.

- **3:**
    Then I used Windsurf to build a working prototype that: 
     - has a front end for receiving audio
     - uses Fastapi backend for processing it (STT)
     - and sends the received audio as output (TTS)

    **issue:**
     - Did not work with Brave, and did not read aloud the text 
    
    **solution:**
     - Prompted and then fixed that issue, AI generated adapter for the code
     where it implemented some necessary interfaces.
     - Moved to Google Chrome where it worked fine.

- **4:**
    Finally I intergrated the Agent from '1' manually into the part where 
    the STT - TTS process happens (inside src/main:on_transcript() L#71) 

- **5:**
    It runs perfectly fine but shows warning after/while processing speech:

    ```
    (venv) bitcot@bitcot-ThinkPad-E16-Gen-3:~/python/Courses & Learnings/Learnings/RAGENT/project_one (feat/ragent_implementation)$ python -m src.api.main
    Starting Voice Gateway on http://0.0.0.0:5000
    Socket.IO endpoint: ws://localhost:5000/socket.io/
    INFO:     Started server process [6771]
    INFO:     Waiting for application startup.
    INFO:     Application startup complete.
    INFO:     Uvicorn running on http://0.0.0.0:5000 (Press CTRL+C to quit)
    INFO:     127.0.0.1:38706 - "WebSocket /socket.io/?EIO=4&transport=websocket" [accepted]
    [XWKjwSf4DobkaMWCAAAB] User said: I love world.
    --------------------------------------------------
    USER MESSAGE: I love world.
    --------------------------------------------------
    --------------------------------------------------
    AI RESPONSE: That's wonderful to hear! The world is full of beauty and diversity. What do you love most about it?
    --------------------------------------------------
    Task was destroyed but it is pending!
    task: <Task pending name='Task-88' coro=<AsyncServer._send_eio_packet() running at /home/bitcot/python/Courses & Learnings/Learnings/RAGENT/project_one/venv/lib/python3.12/site-packages/socketio/async_server.py:530>>
    /usr/lib/python3.12/threading.py:1354: RuntimeWarning: coroutine 'AsyncServer._send_eio_packet' was never awaited
      def _make_invoke_excepthook():
    RuntimeWarning: Enable tracemalloc to get the object allocation traceback
    Task was destroyed but it is pending!
    task: <Task pending name='Task-87' coro=<AsyncServer.emit() done, defined at /home/bitcot/python/Courses & Learnings/Learnings/RAGENT/project_one/venv/lib/python3.12/site-packages/socketio/async_server.py:130> wait_for=<Future pending cb=[Task.task_wakeup()]>>
    Task was destroyed but it is pending!
    task: <Task pending name='Task-91' coro=<AsyncServer._send_eio_packet() running at /home/bitcot/python/Courses & Learnings/Learnings/RAGENT/project_one/venv/lib/python3.12/site-packages/socketio/async_server.py:530>>
    Task was destroyed but it is pending!
    task: <Task pending name='Task-90' coro=<AsyncServer.emit() done, defined at /home/bitcot/python/Courses & Learnings/Learnings/RAGENT/project_one/venv/lib/python3.12/site-packages/socketio/async_server.py:130> wait_for=<Future pending cb=[Task.task_wakeup()]>>
    Task was destroyed but it is pending!
    task: <Task pending name='Task-94' coro=<AsyncServer._send_eio_packet() running at /home/bitcot/python/Courses & Learnings/Learnings/RAGENT/project_one/venv/lib/python3.12/site-packages/socketio/async_server.py:530>>
    Task was destroyed but it is pending!
    task: <Task pending name='Task-93' coro=<AsyncServer.emit() done, defined at /home/bitcot/python/Courses & Learnings/Learnings/RAGENT/project_one/venv/lib/python3.12/site-packages/socketio/async_server.py:130> wait_for=<Future pending cb=[Task.task_wakeup()]>>
    Task was destroyed but it is pending!
    task: <Task pending name='Task-100' coro=<AsyncServer._send_eio_packet() running at /home/bitcot/python/Courses & Learnings/Learnings/RAGENT/project_one/venv/lib/python3.12/site-packages/socketio/async_server.py:530>>
    Task was destroyed but it is pending!
    task: <Task pending name='Task-99' coro=<AsyncServer.emit() done, defined at /home/bitcot/python/Courses & Learnings/Learnings/RAGENT/project_one/venv/lib/python3.12/site-packages/socketio/async_server.py:130> wait_for=<Future pending cb=[Task.task_wakeup()]>>
    Task was destroyed but it is pending!
    task: <Task pending name='Task-103' coro=<AsyncServer._send_eio_packet() running at /home/bitcot/python/Courses & Learnings/Learnings/RAGENT/project_one/venv/lib/python3.12/site-packages/socketio/async_server.py:530>>
    Task was destroyed but it is pending!
    task: <Task pending name='Task-102' coro=<AsyncServer.emit() done, defined at /home/bitcot/python/Courses & Learnings/Learnings/RAGENT/project_one/venv/lib/python3.12/site-packages/socketio/async_server.py:130> wait_for=<Future pending cb=[Task.task_wakeup()]>>
    Task was destroyed but it is pending!
    task: <Task pending name='Task-107' coro=<AsyncServer._send_eio_packet() running at /home/bitcot/python/Courses & Learnings/Learnings/RAGENT/project_one/venv/lib/python3.12/site-packages/socketio/async_server.py:530>>
    Task was destroyed but it is pending!
    task: <Task pending name='Task-106' coro=<AsyncServer.emit() done, defined at /home/bitcot/python/Courses & Learnings/Learnings/RAGENT/project_one/venv/lib/python3.12/site-packages/socketio/async_server.py:130> wait_for=<Future pending cb=[Task.task_wakeup()]>>
    Task was destroyed but it is pending!
    task: <Task pending name='Task-110' coro=<AsyncServer._send_eio_packet() running at /home/bitcot/python/Courses & Learnings/Learnings/RAGENT/project_one/venv/lib/python3.12/site-packages/socketio/async_server.py:530>>
    Task was destroyed but it is pending!
    task: <Task pending name='Task-109' coro=<AsyncServer.emit() done, defined at /home/bitcot/python/Courses & Learnings/Learnings/RAGENT/project_one/venv/lib/python3.12/site-packages/socketio/async_server.py:130> wait_for=<Future pending cb=[Task.task_wakeup()]>>
    Task was destroyed but it is pending!
    task: <Task pending name='Task-113' coro=<AsyncServer._send_eio_packet() running at /home/bitcot/python/Courses & Learnings/Learnings/RAGENT/project_one/venv/lib/python3.12/site-packages/socketio/async_server.py:530>>
    Task was destroyed but it is pending!
    task: <Task pending name='Task-112' coro=<AsyncServer.emit() done, defined at /home/bitcot/python/Courses & Learnings/Learnings/RAGENT/project_one/venv/lib/python3.12/site-packages/socketio/async_server.py:130> wait_for=<Future pending cb=[Task.task_wakeup()]>>
    Task was destroyed but it is pending!
    task: <Task pending name='Task-124' coro=<AsyncServer._send_eio_packet() running at /home/bitcot/python/Courses & Learnings/Learnings/RAGENT/project_one/venv/lib/python3.12/site-packages/socketio/async_server.py:530>>
    Task was destroyed but it is pending!
    task: <Task pending name='Task-123' coro=<AsyncServer.emit() done, defined at /home/bitcot/python/Courses & Learnings/Learnings/RAGENT/project_one/venv/lib/python3.12/site-packages/socketio/async_server.py:130> wait_for=<Future pending cb=[Task.task_wakeup()]>>
    Task was destroyed but it is pending!
    task: <Task pending name='Task-127' coro=<AsyncServer._send_eio_packet() running at /home/bitcot/python/Courses & Learnings/Learnings/RAGENT/project_one/venv/lib/python3.12/site-packages/socketio/async_server.py:530>>
    Task was destroyed but it is pending!
    task: <Task pending name='Task-126' coro=<AsyncServer.emit() done, defined at /home/bitcot/python/Courses & Learnings/Learnings/RAGENT/project_one/venv/lib/python3.12/site-packages/socketio/async_server.py:130> wait_for=<Future pending cb=[Task.task_wakeup()]>>
    Task was destroyed but it is pending!
    task: <Task pending name='Task-130' coro=<AsyncServer._send_eio_packet() running at /home/bitcot/python/Courses & Learnings/Learnings/RAGENT/project_one/venv/lib/python3.12/site-packages/socketio/async_server.py:530>>
    Task was destroyed but it is pending!
    task: <Task pending name='Task-129' coro=<AsyncServer.emit() done, defined at /home/bitcot/python/Courses & Learnings/Learnings/RAGENT/project_one/venv/lib/python3.12/site-packages/socketio/async_server.py:130> wait_for=<Future pending cb=[Task.task_wakeup()]>>
    Task was destroyed but it is pending!
    task: <Task pending name='Task-133' coro=<AsyncServer._send_eio_packet() running at /home/bitcot/python/Courses & Learnings/Learnings/RAGENT/project_one/venv/lib/python3.12/site-packages/socketio/async_server.py:530>>
    Task was destroyed but it is pending!
    task: <Task pending name='Task-132' coro=<AsyncServer.emit() done, defined at /home/bitcot/python/Courses & Learnings/Learnings/RAGENT/project_one/venv/lib/python3.12/site-packages/socketio/async_server.py:130> wait_for=<Future pending cb=[Task.task_wakeup()]>>
    Task was destroyed but it is pending!
    task: <Task pending name='Task-136' coro=<AsyncServer._send_eio_packet() running at /home/bitcot/python/Courses & Learnings/Learnings/RAGENT/project_one/venv/lib/python3.12/site-packages/socketio/async_server.py:530>>
    Task was destroyed but it is pending!
    task: <Task pending name='Task-135' coro=<AsyncServer.emit() done, defined at /home/bitcot/python/Courses & Learnings/Learnings/RAGENT/project_one/venv/lib/python3.12/site-packages/socketio/async_server.py:130> wait_for=<Future pending cb=[Task.task_wakeup()]>>
    Task was destroyed but it is pending!
    task: <Task pending name='Task-139' coro=<AsyncServer._send_eio_packet() running at /home/bitcot/python/Courses & Learnings/Learnings/RAGENT/project_one/venv/lib/python3.12/site-packages/socketio/async_server.py:530>>
    Task was destroyed but it is pending!
    task: <Task pending name='Task-138' coro=<AsyncServer.emit() done, defined at /home/bitcot/python/Courses & Learnings/Learnings/RAGENT/project_one/venv/lib/python3.12/site-packages/socketio/async_server.py:130> wait_for=<Future pending cb=[Task.task_wakeup()]>>
    ```bash
### FIXES
- Better docs (with more comprehensive examples)
