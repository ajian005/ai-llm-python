#模型下载
from modelscope import snapshot_download

# model_dir = snapshot_download('Shanghai_AI_Laboratory/internlm2-chat-1_8b',
#                              cache_dir='/Users/lijianquan/workspace/ai/modelscope')

model_dir = snapshot_download('Qwen/Qwen2.5-0.5B-Instruct',cache_dir='/Users/lijianquan/workspace/ai/modelscope')