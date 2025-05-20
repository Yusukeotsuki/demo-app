<template>
  <div>
    <nav class="top-nav">
      <button @click="current = 'chat'">Chat</button>
      <button @click="current = 'dashboard'">Dashboard</button>
    </nav>
    <Dashboard v-if="current === 'dashboard'" />
    <div v-else class="chat-container">
      <h1>Multi-Agent Chat</h1>
      <div class="messages">
        <div
          v-for="msg in messages"
          :key="msg.id"
          :class="['message', msg.from === 'user' ? 'user' : 'agent']"
        >
          <div v-if="msg.from !== 'user'" class="bubble agent">
            <div class="agent-header">
              <img :src="`/${msg.from}.svg`" alt="Agent" class="agent-icon" />
              <span>{{ msg.from }}</span>
            </div>
            <div class="agent-content" v-html="renderMarkdown(msg.text)"></div>
          </div>
          <div v-else class="bubble user">
            <div class="user-content">{{ msg.text }}</div>
          </div>
        </div>
      </div>
      <div class="input-area">
        <input
          type="text"
          v-model="input"
          @keyup.enter="sendMessage"
          placeholder="Type a message or attach Excel..."
        />
        <button class="attach" @click="$refs.fileInput.click()">Attach</button>
        <input
          type="file"
          ref="fileInput"
          accept=".xlsx,.xls"
          style="display:none"
          @change="onFileChange"
        />
        <button class="send" @click="sendMessage">Send</button>
      </div>
    </div>
  </div>
</template>

<script>
import { marked } from 'marked'
import Dashboard from './components/Dashboard.vue'

export default {
  components: { Dashboard },
  data() {
    return {
      current: 'chat',
      input: '',
      messages: [],
      showExcelIcon: false,
      selectedFile: null,
      evtSource: null,
    }
  },
  methods: {
    renderMarkdown(text) {
      return marked.parse(text)
    },
    onFileChange(event) {
      const file = event.target.files[0]
      if (file && /\.(xlsx|xls)$/i.test(file.name)) {
        this.showExcelIcon = true
        this.selectedFile = file
        this.input = file.name
      } else {
        this.showExcelIcon = false
        this.selectedFile = null
      }
    },
    sendMessage() {
      const text = this.input.trim()
      if (!text && !this.selectedFile) return

      this.messages.push({
        id: Date.now(),
        from: 'user',
        text: text || this.selectedFile.name,
      })
      this.input = ''
      this.showExcelIcon = false

      if (this.evtSource) {
        this.evtSource.close()
        this.evtSource = null
      }

      const url = `http://localhost:5000/api/chat_stream?message=${encodeURIComponent(text)}`
      this.evtSource = new EventSource(url)

      let buffer = ''
      const msgId = Date.now() + Math.random()

      this.evtSource.onmessage = (e) => {
        const { from, chunk } = JSON.parse(e.data)
        buffer += chunk

        const idx = this.messages.findIndex((m) => m.id === msgId)
        if (idx === -1) {
          this.messages.push({ id: msgId, from, text: buffer })
        } else {
          this.messages[idx] = { id: msgId, from, text: buffer }
        }
      }

      this.evtSource.addEventListener('end', () => {
        this.evtSource.close()
        this.evtSource = null
      })
    },
  },
}
</script>

<style scoped>
.top-nav {
  display: flex;
  gap: 10px;
  padding: 10px;
  background: #eee;
  margin-bottom: 10px;
}
.top-nav button {
  padding: 6px 12px;
}
/* Existing chat styles follow */
.chat-container {
  max-width: 800px;
  margin: 40px auto;
  background: #fff;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}
.chat-container h1 {
  font-size: 2rem;
  margin-bottom: 20px;
  text-align: center;
  color: #3f51b5;
}
.messages {
  height: 600px;
  overflow-y: auto;
  margin-bottom: 20px;
}
.messages::-webkit-scrollbar {
  width: 8px;
}
.messages::-webkit-scrollbar-thumb {
  background-color: rgba(0, 0, 0, 0.2);
  border-radius: 4px;
}
.message {
  display: flex;
  margin-bottom: 16px;
}
.message.agent {
  justify-content: flex-start;
}
.message.user {
  justify-content: flex-end;
}
.bubble {
  max-width: 70%;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}
.bubble.agent {
  background: #e8eaf6;
  color: #000;
}
.bubble.user {
  background: #4caf50;
  color: #fff;
}
.agent-header {
  display: flex;
  align-items: center;
  background: #3f51b5;
  color: #fff;
  padding: 4px 8px;
  border-top-left-radius: 8px;
  border-top-right-radius: 8px;
}
.agent-icon {
  width: 20px;
  height: 20px;
  margin-right: 4px;
  border-radius: 50%;
}
.agent-content,
.user-content {
  padding: 8px;
}
.input-area {
  display: flex;
  align-items: center;
}
.input-area input[type="text"] {
  flex-grow: 1;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
}
.input-area button {
  margin-left: 8px;
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  color: #fff;
  cursor: pointer;
}
.input-area button.attach {
  background: #ffc107;
}
.input-area button.send {
  background: #2196f3;
}
</style>
