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

### FIXES
- Better docs (with more comprehensive examples)
