# Ollama 相关命令


Ollama 提供了多种命令行工具（CLI）供用户与本地运行的模型进行交互。

我们可以用 ollama --help 查看包含有哪些命令：
```shell
Large language model runner

Usage:
  ollama [flags]
  ollama [command]

Available Commands:
  serve       Start ollama
  create      Create a model from a Modelfile
  show        Show information for a model
  run         Run a model
  stop        Stop a running model
  pull        Pull a model from a registry
  push        Push a model to a registry
  list        List models
  ps          List running models
  cp          Copy a model
  rm          Remove a model
  help        Help about any command

Flags:
  -h, --help      help for ollama
  -v, --version   Show version information
```
### 1、使用方法

- ollama [flags]：使用标志（flags）运行 ollama。

- ollama [command]：运行 ollama 的某个具体命令。

### 2、可用命令

- serve：启动 ollama 服务。
- create：根据一个 Modelfile 创建一个模型。
- show：显示某个模型的详细信息。
- run：运行一个模型。
- stop：停止一个正在运行的模型。
- pull：从一个模型仓库（registry）拉取一个模型。
- push：将一个模型推送到一个模型仓库。
- list：列出所有模型。
- ps：列出所有正在运行的模型。
- cp：复制一个模型。
- rm：删除一个模型。
- help：获取关于任何命令的帮助信息。
### 3、标志（Flags）

- -h, --help：显示 ollama 的帮助信息。
- -v, --version：显示版本信息。

## 1. 模型管理
### 拉取模型
从模型库中下载模型：
```
ollama pull <model-name>
```
例如：
```
ollama pull llama2
```
### 运行模型
运行已下载的模型：
```
ollama run <model-name>
```
例如：
```
ollama run llama2
```
### 列出本地模型
查看已下载的模型列表：
```
ollama list
```
### 删除模型
删除本地模型：
```
ollama rm <model-name>
```
例如：
```
ollama rm llama2
```
## 2. 自定义模型
### 创建自定义模型
基于现有模型创建自定义模型：
```
ollama create <custom-model-name> -f <Modelfile>
```
例如：
```
ollama create my-llama2 -f ./Modelfile
```
### 复制模型
复制一个已存在的模型：
```
ollama cp <source-model-name> <new-model-name>
```
例如：
```
ollama cp llama2 my-llama2-copy
```
### 推送自定义模型
将自定义模型推送到模型库：
```
ollama push <model-name>
```
例如：
```
ollama push my-llama2
```
## 3. 服务管理
### 启动 Ollama 服务
启动 Ollama 服务以在后台运行：
```
ollama serve
```
### 停止 Ollama 服务
停止正在运行的 Ollama 服务：
```
ollama stop
```
### 重启 Ollama 服务
重启 Ollama 服务：
```
ollama restart
```
## 4. 其他常用命令
### 查看帮助
查看所有可用命令：
```
ollama --help
```
### 查看版本信息
查看当前安装的 Ollama 版本：
```
ollama version
```
### 更新 Ollama
更新 Ollama 到最新版本：
```
ollama update
```
### 查看日志
查看 Ollama 的日志信息：
```
ollama logs
```
### 清理缓存
清理 Ollama 的缓存：
```
ollama clean
```
## 5. 模型信息
### 查看模型详细信息
查看指定模型的详细信息：
```
ollama show <model-name>
```
例如：
```
ollama show llama2
```
### 查看模型依赖
查看模型的依赖关系：
```
ollama deps <model-name>
```
例如：
```
ollama deps llama2
```
### 查看模型配置
查看模型的配置文件：
```
ollama config <model-name>
```
例如：
```
ollama config llama2
```
## 6. 导入与导出
### 导出模型
将模型导出为文件：
```
ollama export <model-name> <output-file>
```
例如：
```
ollama export llama2 llama2.tar
```
### 导入模型
从文件导入模型：
```
ollama import <input-file>
```
例如：
```
ollama import llama2.tar
```
## 7. 系统信息
### 查看系统信息
查看 Ollama 的系统信息：
```
ollama system
```
### 查看资源使用情况
查看模型的资源使用情况：
```
ollama resources <model-name>
```
例如：
```
ollama resources llama2
```
## 8. 模型性能
### 查看模型性能
查看模型的性能指标：
```
ollama perf <model-name>
```
例如：
```
ollama perf llama2
```
## 9. 模型历史
### 查看模型历史记录
查看模型的历史记录：
```
ollama history <model-name>
```
例如：
```
ollama history llama2
```
## 10. 模型状态
### 检查模型状态
检查指定模型的状态：
```
ollama status <model-name>
```
例如：
```
ollama status llama2
```
