from django import template
import re

register = template.Library()
# 이미지를 복붙 했을 때 img 태그에서 첫장을 뽑아오는 custom template
@register.filter
def extract_first_image_url(content):
    # 정규 표현식을 사용하여 첫 번째 이미지 URL 추출
    img_urls = re.findall(r'<img.*?src="(.*?)".*?>', content)
    
    # 이미지 URL 리스트에서 첫 번째 항목을 반환
    if img_urls:
        return img_urls[0]
    else:
        return None
