<template>
  <div class="chat-container">
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
</template>

<script>
import { marked } from 'marked'

export default {
  data() {
    return {
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

<<<<<<< HEAD
<style>
/* カスタムスクロールバー */
.space-y-4::-webkit-scrollbar {
  width: 8px;
}
.space-y-4::-webkit-scrollbar-thumb {
  background-color: rgba(0, 0, 0, 0.2);
  border-radius: 4px;
}

/* Tailwind Prose を有効化する場合 */
@import "https://cdn.jsdelivr.net/npm/tailwindcss@^3/dist/base.min.css";
@import "https://cdn.jsdelivr.net/npm/tailwindcss@^3/dist/components.min.css";
@import "https://cdn.jsdelivr.net/npm/tailwindcss@^3/dist/utilities.min.css";
</style>
=======
<style scoped>
</style>
>>>>>>> 11169b6f4abdde79ac9f26e0186dadc485cd3c4d
