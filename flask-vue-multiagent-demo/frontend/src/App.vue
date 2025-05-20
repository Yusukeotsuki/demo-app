<template>
  <v-app>
    <v-main class="d-flex align-center justify-center bg-grey-lighten-4" style="min-height: 100vh;">
      <v-card elevation="10" class="pa-6" max-width="800">
        <v-card-title class="text-h4 text-center bg-gradient-to-r from-purple-400 to-pink-600 text-transparent bg-clip-text">
          Multi-Agent Chat
        </v-card-title>
        <v-card-text>
          <div class="overflow-y-auto mb-6" style="height: 600px;">
            <div
              v-for="msg in messages"
              :key="msg.id"
              class="d-flex mb-4"
              :class="msg.from === 'user' ? 'justify-end' : 'justify-start'"
            >
              <template v-if="msg.from !== 'user'">
                <v-card class="ma-2" color="blue-lighten-4" width="70%">
                  <v-card-title class="d-flex align-center blue">
                    <v-avatar class="mr-2" size="24">
                      <img :src="`/${msg.from}.svg`" alt="Agent" />
                    </v-avatar>
                    <span class="font-weight-medium text-white">{{ msg.from }}</span>
                  </v-card-title>
                  <v-card-text class="text-body-2">
                    <div v-html="renderMarkdown(msg.text)" class="prose"></div>
                  </v-card-text>
                </v-card>
              </template>
              <template v-else>
                <v-card class="ma-2" color="green" dark width="70%">
                  <v-card-text>{{ msg.text }}</v-card-text>
                </v-card>
              </template>
            </div>
          </div>
          <div class="d-flex align-center">
            <v-text-field
              v-model="input"
              @keyup.enter="sendMessage"
              hide-details
              class="flex-grow-1 mr-2"
              placeholder="Type a message or attach Excel..."
            ></v-text-field>
            <v-btn color="amber" class="mr-2" @click="$refs.fileInput.click()">
              Attach
            </v-btn>
            <input
              type="file"
              ref="fileInput"
              accept=".xlsx,.xls"
              class="d-none"
              @change="onFileChange"
            />
            <v-btn color="blue" @click="sendMessage">Send</v-btn>
          </div>
        </v-card-text>
      </v-card>
    </v-main>
  </v-app>
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
    // Markdown → HTML
    renderMarkdown(text) {
      return marked.parse(text)
    },

    // Excelファイル選択
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

      // ユーザー発言を即プッシュ
      this.messages.push({
        id: Date.now(),
        from: 'user',
        text: text || this.selectedFile.name
      })
      this.input = ''
      this.showExcelIcon = false

     // 既存のストリームがあれば閉じる
     if (this.evtSource) {
       this.evtSource.close()
       this.evtSource = null
     }

     // 必ずクエリ文字列を付与して GET で接続
     const url = `http://localhost:5000/api/chat_stream?message=${encodeURIComponent(text)}`
     this.evtSource = new EventSource(url)

      let buffer = ''
      const msgId = Date.now() + Math.random()

      this.evtSource.onmessage = (e) => {
        const { from, chunk } = JSON.parse(e.data)
        buffer += chunk

        const idx = this.messages.findIndex(m => m.id === msgId)
        if (idx === -1) {
          this.messages.push({ id: msgId, from, text: buffer })
        } else {
          // Vue 3 no longer provides $set, so update array element directly
          this.messages[idx] = { id: msgId, from, text: buffer }
        }
      }

      // SSE の end イベントでクローズ＆参照クリア
      this.evtSource.addEventListener('end', () => {
        this.evtSource.close()
        this.evtSource = null
      })
    }
  }
}
</script>

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
