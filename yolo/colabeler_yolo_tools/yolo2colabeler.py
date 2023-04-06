import os
import sys
import cv2

# argument = sys.argv[1:]
# print(len(argument))
# if len(argument) < 2 or len(argument) > 3:
#     print("Example: python yolo2colabeler.py ./pic ./outputs_yolo ./outputs_xml")
#     sys.exit(1)
# elif len(argument) == 2:
#     if not argument[0].endswith('/'):
#         argument[0] += '/'
#     if not argument[1].endswith('/'):
#         argument[1] += '/'
#     pic_dir = argument[0]
#     txt_dir = argument[1]
#     xml_des = "./output_xml/"
# elif len(argument) == 3:
#     if not argument[0].endswith('/'):
#         argument[0] += '/'
#     if not argument[1].endswith('/'):
#         argument[1] += '/'
#     if not argument[2].endswith('/'):

#         argument[2] += +6'/'
#     pic_dir = argument[0]
#     txt_dir = argument[1]zobg
#     xml_des = argument[2]
pic_dir ='G:/GC_biaotu/yolov5/runs/detect/imx/images/'
txt_dir ='G:/GC_biaotu/yolov5/runs/detect/imx/labels/'
xml_des = 'G:/GC_biaotu/yolov5/jpg/outputs/'
index={0:"HeavyVehicle", 1:"MidsizeVehicle", 2:"CompactVehicle", 3:"Car",4: "NoneVehicle", 5:"Pedestrian", 6:"LargeBus",7:"LightBus"}
class obj():
    type = ""
    xmin = 0
    ymin = 0
    xmax = 0
    ymax = 0

# detect and create xml folder
if not os.path.exists(xml_des):
    os.makedirs(xml_des)


pic_filelists = os.listdir(pic_dir)
txt_filelists = os.listdir(txt_dir)
for file in txt_filelists:
    # get width and height
    try:
        print(pic_dir + file.split('.txt')[0] + '.' + pic_filelists[0].split('.')[-1])
        image = cv2.imread(pic_dir + file.split('.txt')[0] + '.' + pic_filelists[0].split('.')[-1])
        size = image.shape
        w = size[1] #宽度
        h = size[0] #高度
    except:
        print('Not corresponding!')
        sys.exit(1)
    
    # read txt
    f = open(txt_dir + file)
    lines = f.readlines()
    f.close()

    # create xml content
    result_str = "<?xml version=\"1.0\" ?><doc><path>" + os.getcwd() + "\\" + pic_dir.split('/')[1] + "\\" + file.split('.txt')[0] + '.' + pic_filelists[0].split('.')[-1] + "</path><outputs><object>"
    for line in lines:
        b = obj()
        line = line.split('\n')[0].split(' ')
        b.type = int(line[0])
        b.xmin = int((2*float(line[1])*w-float(line[3])*w)/2)
        b.xmax = int((float(line[3])*w+2*float(line[1])*w)/2)
        b.ymin = int((2*float(line[2])*h-float(line[4])*h)/2)
        b.ymax = int((float(line[4])*h+2*float(line[2])*h)/2)
        result_str += "<item><name>" + index[b.type] + "</name>" + "<bndbox>" + "<xmin>" + str(b.xmin) + "</xmin>" + "<ymin>"+ str(b.ymin) +"</ymin>" + "<xmax>"+ str(b.xmax) +"</xmax>" + "<ymax>"+ str(b.ymax) +"</ymax></bndbox></item>"
    result_str += "</object></outputs><time_labeled>1618224361277</time_labeled><labeled>true</labeled><size><width>"+ str(w) +"</width><height>"+ str(h) + "</height><depth>3</depth></size></doc>"
    
    # write xml
    f = open(xml_des + file.split('.txt')[0] + '.xml', 'w')
    f.write(result_str)
    f.close()
