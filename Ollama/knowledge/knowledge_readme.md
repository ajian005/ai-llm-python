# RAG私有化知识库
### 前提
- 部署好 Open WebUI + Ollama + 开源大模型(DeepSeek|Gamma)
- 知识库素材 如:WM_IoT_SDK  https://github.com/winnermicro/wm_iot_sdk

### 进入知识库的数据预处理
- 直接将 word Excel数据导入是无法正常使用的，原因是需要进行切片后才可以使用的；word文件其实是一个压缩包，代码也不行
- 这里将数据手动切片为几个文件 (实际情况可以采用切片工具进行加工，这里知识演示)
- 手动将文件《wifi api station 联网示例代码.txt》 切片为:
  《wifi api station 联网示例代码01.txt》
  《wifi api station 联网示例代码02.txt》
  《wifi api station 联网示例代码03.txt》

- 手动上传到Open WebUI的知识库
   
