"""
    大模型服务平台-->百炼用户指南（模型）--> 图像生成 --> 涂鸦作画: https://help.aliyun.com/zh/model-studio/sketch-to-image

    根据手绘图加上任意文字描述，使用通义万相-涂鸦作画模型，即可轻松完成涂鸦作画。

基本介绍
    通义万相-涂鸦作画通过手绘任意内容加文字描述，即可生成精美的涂鸦绘画作品，作品中的内容在参考手绘线条的同时，兼顾创意性和趣味性。涂鸦作画支持扁平插画、油画、二次元、3D卡通和水彩5种风格，可用于创意娱乐、辅助设计、儿童教学等场景。

    如想了解功能效果或使用流程，可以在通义万相-涂鸦作画功能中进行体验。

使用场景
    创意贺卡设计：用户可以利用涂鸦作画功能，结合节日主题和个人创意，手稿创作一幅圣诞老人与驯鹿在雪地中的温馨场景，增加贺卡的个性化与情感表达，使收卡人感受到更加真挚与特别的祝福。

    儿童绘本制作：教育工作者或家长可以根据孩子的兴趣和故事内容，涂鸦作画制作富有教育意义和趣味性的插图绘本，提升儿童阅读兴趣，促进想象力和创造力的发展。

    个性化商品设计：电商平台或设计师可以利用该功能快速生成具有独特艺术风格的产品设计，如T恤、手机壳、马克杯上的涂鸦创作图案，满足消费者对个性化和定制化商品的需求。

    社交媒体内容创作：博主和内容创作者可利用涂鸦作画创作与主题内容相符的原创涂鸦插图，提高内容的视觉吸引力，帮助建立独特的个人品牌形象，吸引并保持粉丝的关注。

    室内装饰设计：室内设计师可以为客户定制个性化的墙面艺术画或装饰图案，如根据房间风格创作相应风格涂的鸦画作，实现空间的个性化定制，提升居住或办公环境的艺术氛围。

特色优势
    知识重组&可变维扩散模型：基于自研的Composer组合生成框架的AI局部绘画创作大模型，通过知识重组与可变维度扩散模型，生成符合语义描述的多样化风格的图像。

    效果业界领先：生成图像语义一致性更精准，AI绘画创作布局自然、细节丰富、画面细腻、结果逼真。作品中的内容在参考手绘线条的同时，兼顾创意性和趣味性。

    涂鸦风格多样化：支持扁平插画、油画、二次元、3D卡通和水彩五种风格。

    稳定、易用平台服务：提供在高并发、大流量下的稳定图片生成响应和99.99%的可靠性保障，可直接调用的简单训练和推理API 接口，服务简单易用，易于集成，兼容性强。

"""

from http import HTTPStatus
from urllib.parse import urlparse, unquote
from pathlib import PurePosixPath
import requests
from dashscope import ImageSynthesis

prompt = "一棵参天大树"
sketch_image_url = "https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/6609471071/p743851.jpg"
model = "wanx-sketch-to-image-lite"
task = "image2image"


# 异步调用
def async_call():
    print('----create task----')
    task_info = create_async_task()
    print('----wait task done then save image----')
    wait_async_task(task_info)


# 创建异步任务
def create_async_task():
    rsp = ImageSynthesis.async_call(model=model,
                                    prompt=prompt,
                                    n=1,
                                    style='<watercolor>',
                                    size='768*768',
                                    sketch_image_url=sketch_image_url,
                                    task=task)
    print(rsp)
    if rsp.status_code == HTTPStatus.OK:
        print(rsp.output)
    else:
        print('create_async_task Failed, status_code: %s, code: %s, message: %s' %
              (rsp.status_code, rsp.code, rsp.message))
    return rsp


# 等待异步任务结束
def wait_async_task(task):
    rsp = ImageSynthesis.wait(task)
    print(rsp)
    if rsp.status_code == HTTPStatus.OK:
        print(rsp.output.task_status)
        # save file to current directory
        for result in rsp.output.results:
            file_name = PurePosixPath(unquote(urlparse(result.url).path)).parts[-1]
            with open('./%s' % file_name, 'wb+') as f:
                f.write(requests.get(result.url).content)
    else:
        print('Failed, status_code: %s, code: %s, message: %s' %
              (rsp.status_code, rsp.code, rsp.message))


if __name__ == '__main__':
    async_call()
    