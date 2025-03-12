# Ollama API 交互
Ollama 提供了基于 HTTP 的 API，允许开发者通过编程方式与模型进行交互。

本文将详细介绍 Ollama API 的详细使用方法，包括请求格式、响应格式以及示例代码。

# 1. 启动 Ollama 服务
在使用 API 之前，需要确保 Ollama 服务正在运行。可以通过以下命令启动服务：
```
ollama serve
```
默认情况下，服务会运行在 http://localhost:11434。

# 2. API 端点
Ollama 提供了以下主要 API 端点：

## 生成文本（Generate Text）
- 端点：POST /api/generate

- 功能：向模型发送提示词（prompt），并获取生成的文本。

- 请求格式：
```
{
  "model": "<model-name>",  // 模型名称
  "prompt": "<input-text>", // 输入的提示词
  "stream": false,          // 是否启用流式响应（默认 false）
  "options": {              // 可选参数
    "temperature": 0.7,     // 温度参数
    "max_tokens": 100       // 最大 token 数
  }
}
```

响应格式：
```
{
  "response": "<generated-text>", // 生成的文本
  "done": true                    // 是否完成
}
```

## 聊天（Chat）
- 端点：POST /api/chat

- 功能：支持多轮对话，模型会记住上下文。

请求格式：
```
{
  "model": "<model-name>",  // 模型名称
  "messages": [             // 消息列表
    {
      "role": "user",       // 用户角色
      "content": "<input-text>" // 用户输入
    }
  ],
  "stream": false,          // 是否启用流式响应
  "options": {              // 可选参数
    "temperature": 0.7,
    "max_tokens": 100
  }
}
```
响应格式：
```
{
  "message": {
    "role": "assistant",    // 助手角色
    "content": "<generated-text>" // 生成的文本
  },
  "done": true
}
```
## 列出本地模型（List Models）
- 端点：GET /api/tags

- 功能：列出本地已下载的模型。

- 响应格式：
```
{
  "models": [
    {
      "name": "<model-name>", // 模型名称
      "size": "<model-size>", // 模型大小
      "modified_at": "<timestamp>" // 修改时间
    }
  ]
}
```
## 拉取模型（Pull Model）
- 端点：POST /api/pull

- 功能：从模型库中拉取模型。

- 请求格式：
```
{
  "name": "<model-name>" // 模型名称
}
```
响应格式：
```
{
  "status": "downloading", // 下载状态
  "digest": "<model-digest>" // 模型摘要
}
```
# 3. 使用示例
## 生成文本
使用 curl 发送请求：

实例
```
curl http://localhost:11434/api/generate -d '{
  "model": "deepseek-coder",
  "prompt": "你好，你能帮我写一段代码吗？",
  "stream": false
}'
```
## 多轮对话
使用 curl 发送请求：

实例
```
curl http://localhost:11434/api/chat -d '{
  "model": "deepseek-coder",
  "messages": [
    {
      "role": "user",
      "content": "你好，你能帮我写一段 Python 代码吗？"
    }
  ],
  "stream": false
}'
```
## 列出本地模型
使用 curl 发送请求：

curl http://localhost:11434/api/tags

## 拉取模型
使用 curl 发送请求：

实例
```
curl http://localhost:11434/api/pull -d '{
  "name": "deepseek-coder"
}'
```
# 4. 流式响应
Ollama 支持流式响应（streaming response），适用于实时生成文本的场景。

## 启用流式响应
在请求中设置 "stream": true，API 会逐行返回生成的文本。

实例
```
curl http://localhost:11434/api/generate -d '{
  "model": "deepseek-coder",
  "prompt": "你好，你能帮我写一段代码吗？",
  "stream": true
}'
```
响应格式
每行返回一个 JSON 对象：

实例
```
{
  "response": "<partial-text>", // 部分生成的文本
  "done": false                 // 是否完成
}
```
# 5. 编程语言示例
## Python 使用 requests 库与 Ollama API 交互：

实例
```python
import requests

# 生成文本
response = requests.post(
    "http://localhost:11434/api/generate",
    json={
        "model": "deepseek-coder",
        "prompt": "你好，你能帮我写一段代码吗？",
        "stream": False
    }
)
print(response.json())
```
## 多轮对话:

实例
```
response = requests.post(
    "http://localhost:11434/api/chat",
    json={
        "model": "deepseek-coder",
        "messages": [
            {
                "role": "user",
                "content": "你好，你能帮我写一段 Python 代码吗？"
            }
        ],
        "stream": False
    }
)
print(response.json())
```

## JavaScript 使用 fetch API 与 Ollama 交互：

实例
```javascript
// 生成文本
fetch("http://localhost:11434/api/generate", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    model: "deepseek-coder",
    prompt: "你好，你能帮我写一段代码吗？",
    stream: false
  })
})
  .then(response => response.json())
  .then(data => console.log(data));
```
### 多轮对话:

实例
```javascript
fetch("http://localhost:11434/api/chat", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    model: "deepseek-coder",
    messages: [
      {
        role: "user",
        content: "你好，你能帮我写一段 Python 代码吗？"
      }
    ],
    stream: false
  })
})
  .then(response => response.json())
  .then(data => console.log(data));
```