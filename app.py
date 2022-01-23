from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from e3utils.routers import data
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.include_router(data.router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>SSE Chat</h1>
        <form action="" onsubmit="setupSse()">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
                var url = `/sse/redditSearch?search_term=bitcoin`
                var sse = new EventSource(url)
                sse.onmessage = function(event) {
                    var messages = document.getElementById('messages')
                    var content = JSON.parse(event.data).data
                    for (let i = 0; i < content.length; i++){
                        var message = document.createElement('li')
                        var item = content[i].data;
                        var contentStr = `${item.author}:: ${item.title}`
                        var childText = document.createTextNode(contentStr)
                        message.appendChild(childText)
                        messages.appendChild(message)
                        var br = document.createElement("br");
                        messages.appendChild(br)
                    }
                }
            function setupSse() {
                var input = document.getElementById("messageText")
                
            }
        </script>
    </body>
</html>
"""


@app.get("/")
async def get():
    return HTMLResponse(html)


