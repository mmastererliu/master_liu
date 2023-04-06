from xml.dom.minidom import parse
import os
import cv2
import re
import sys

# Read arguments
# argument = sys.argv[1:]
# if len(argument) < 2 or len(argument) > 3:
#     print("Example: python colabeler2yolo.py ./pic ./outputs ./outputs_yolo")
#     sys.exit(1)
# elif len(argument) == 2:
#     if not argument[0].endswith('/'):
#         argument[0] += '/'
#     if not argument[1].endswith('/'):
#         argument[1] += '/'
#     pic_dir = argument[0]
#     xml_dir = argument[1]
#     txt_des = "./outputs_yolo/"
# elif len(argument) == 3:
#     if not argument[0].endswith('/'):
#         argument[0] += '/'
#     if not argument[1].endswith('/'):
#         argument[1] += '/'
#     if not argument[2].endswith('/'):
#         argument[2] += '/'
pic_dir = 'G:/b_zhan/yolov5-master/yolo/imx/images/train/'
xml_dir = 'G:/b_zhan/yolov5-master/yolo/imx/images/xml/'
txt_des = 'G:/b_zhan/yolov5-master/yolo/imx/labels/train/'
#
# index = {'aeroplane':0,'bicycle':1,'bird':2,'boat':3,'bottle':4,'bus':5,'car':6,'cat':7,'chair':8,
#         'cow':9,'diningtable':10,'dog':11,'horse':12,'motorbike':13,'person':14,'pottedplant':15,'sheep':16,
#         'sofa':17,'train':18, 'tvmonitor':19}
index = { "plate": 0}


class bbox():
    type = ''
    mid_x = 0
    mid_y = 0
    dis_x = 0
    dis_y = 0


# get bbox info from xml
def get(dir):
    DOMTree = parse(dir)
    collection = DOMTree.documentElement

    result = []
    w = int(collection.getElementsByTagName('width')[0].childNodes[0].data)
    h = int(collection.getElementsByTagName('height')[0].childNodes[0].data)

    items = collection.getElementsByTagName('item')
    # 精灵标注助手标的图片 将’object‘改为item
    for i in items:
        b = bbox()
        b.type = i.getElementsByTagName('name')[0].childNodes[0].data

        lu_1 = int(i.getElementsByTagName('bndbox')[0].getElementsByTagName('xmin')[0].childNodes[0].data)
        lu_2 = int(i.getElementsByTagName('bndbox')[0].getElementsByTagName('ymin')[0].childNodes[0].data)
        rb_1 = int(i.getElementsByTagName('bndbox')[0].getElementsByTagName('xmax')[0].childNodes[0].data)
        rb_2 = int(i.getElementsByTagName('bndbox')[0].getElementsByTagName('ymax')[0].childNodes[0].data)

        # 0 中心点（归一化宽） 中心点（归一化长） 框宽度（归一化） 框长度（归一化）
        b.mid_x = (rb_1 + lu_1) / 2 / w
        b.mid_y = (rb_2 + lu_2) / 2 / h
        b.dis_x = (rb_1 - lu_1) / w
        b.dis_y = (rb_2 - lu_2) / h

        result.append(b)
    return result


# detect and create destination folder
if not os.path.exists(txt_des):
    os.makedirs(txt_des)

# xml2yolo conversion
filelists = os.listdir(pic_dir)
for n_0 in filelists:
    # print(n_0)
    if (len(n_0.split('.')) <= 1):
        continue
    n_0 = n_0.split('.jpg')[0] + '.xml'
    if os.path.exists(xml_dir + n_0):
        try:
            res = ''
            r = get(xml_dir + n_0)
            tar_num = len(get(xml_dir + n_0))
            print(n_0 + ', 目标数量：' + str(tar_num))

            # 防止有多余的其他字符或空格
            for k in range(tar_num):
                t = re.sub('[\W_]+', '', r[k].type)
                res += str(index[t]) + ' ' + str(r[k].mid_x) + ' ' + str(r[k].mid_y) + ' ' + str(
                    r[k].dis_x) + ' ' + str(r[k].dis_y) + '\n'

            f = open(txt_des + n_0.split('.xml')[0] + '.txt', 'w')
            f.write(res)
            f.close()
        except:
            print('WARNING : Existing wrong labels')
