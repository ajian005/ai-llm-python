#模型下载
from modelscope import snapshot_download

model_dir = snapshot_download('Ceceliachenen/paraphrase-multilingual-MiniLM-L12-v2',
                              cache_dir='/Users/lijianquan/workspace/ai/modelscope')
