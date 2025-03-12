# Ollama 教程

![alt text](src/images/ollama_introduction_image.png)
Ollama 是一个开源的本地大语言模型运行框架，专为在本地机器上便捷部署和运行大型语言模型（LLM）而设计。

Ollama 支持多种操作系统，包括 macOS、Windows、Linux 以及通过 Docker 容器运行。

Ollama 提供对模型量化的支持，可以显著降低显存要求，使得在普通家用计算机上运行大型模型成为可能。

## 谁适合阅读本教程？
Ollama 适用于开发者、研究人员以及对数据隐私有较高要求的用户，它可以帮助用户在本地环境中快速部署和运行大型语言模型，同时提供灵活的定制化选项。

使用 Ollama，我们可以在在本地运行 Llama 3.3、DeepSeek-R1、Phi-4、Mistral、Gemma 2 和其他模型。

## 学习本教程前你需要了解
本教程适合有 Python 基础的开发者学习，如果不了解 Python 可以查阅 Python 3.x 基础教程。

理解 Docker 镜像和容器的区别，知道如何从 Docker Hub 拉取镜像并运行容器，docker 相关内容参见： Docker 教程。

熟悉命令行工具（如终端或命令提示符）的基本操作，例如文件和目录的创建、删除、移动，以及如何运行脚本和程序。

## 创建新的模型
我们可以使用 ollama create 命令从 Modelfile 创建模型：

实例

``` shell
ollama create model -of ./Modelfile
```


## 相关链接
Ollama 官方地址：https://ollama.com/

Github 开源地址：https://github.com/ollama/ollama

Ollama 官方文档：https://github.com/ollama/ollama/tree/main/docs