import re
import cpca


def parse(user_id, text, pics):
    if '姓名' not in text:
        return

    start_idx = text.find('姓名')
    text = text[start_idx:]
    end_idx = text.find('<a') 
    if end_idx != -1:
        text = text[:end_idx]

    info_dict = {}
    info_dict['id'] = user_id
    info_dict['pics'] = pics

    addr_info, contact_info = '', ''
    _segments = re.split(r'<br />', text)
    segments = [_s for _s in _segments if _s]
    for seg in segments:
        idx = seg.find('】') if seg.find('】') != -1 else seg.find(']')
        if '姓名' in seg:
            info_dict['name'] = seg[idx+1:].strip()    # 去除首尾空格
        elif '病情描述' in seg or '诊断信息' in seg:
            desc = seg[idx+1:].strip()
            if not desc and i + 1 < len(segments):
                desc = segments[i+1]
            _idx = desc.find('<')                       
            desc = desc[:_idx] if _idx != -1 else desc
            info_dict['desc'] = desc  
        elif '联系方式' in seg or '紧急联系人' in seg or '联系人' in seg:
            contact_info += seg[idx+1:]  
        elif '所在小区、社区' in seg or '所在城市' in seg or '详细地址' in seg:
            addr_info += seg[idx+1:]

    if not addr_info:
        return
    df = cpca.transform([addr_info])
    info_dict['province'] = df['省'][0]
    info_dict['city'] = df['市'][0]
    info_dict['region'] = df['区'][0] 
    info_dict['addr'] = df['地址'][0] if df['地址'][0] else addr_info

    phone = re.findall(r'\d+', contact_info)
    phone = ''.join(phone)
    if not phone:
        return
    info_dict['phone'] = phone[:11]
    contact = re.split(r'\d+', contact_info)
    if not ''.join(contact) or '&amp' in ''.join(contact).strip():
        info_dict['contact'] = info_dict['name']
    else:
        info_dict['contact'] = ' '.join(contact).strip()                   

    if '非肺炎' in desc:
        info_dict['isCoronavirus'] = False
    elif re.search(r'肺炎|发热|冠状病|感染|发烧|咳嗽|核酸', desc):
        info_dict['isCoronavirus'] = True
    else:
        info_dict['isCoronavirus'] = False

    if 'desc' in info_dict.keys():
      if '确诊' in info_dict['desc'] or '阳性' in info_dict['desc']:
            info_dict['question'] = '确诊'
      elif '疑似' in info_dict['desc']:
            info_dict['question'] = '疑似'
      elif '密切接触' in info_dict['desc']:
            info_dict['question'] = '密切接触'  
      else:  
            info_dict['question'] = '无法排除的发热者' 
    else:
      info_dict['desc'] = ''
      info_dict['question'] = '疑似'

    return info_dict
