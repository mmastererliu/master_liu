
import numpy as np
import cv2
import torch
from lprr.LPRNet  import CHARS, build_lprnet
import numpy as np

def transform( img):
    img = img.astype('float32')
    img/=255
    img = np.transpose(img, (2, 0, 1))
    return img
def de_lpr(coord,im0):
    img=im0[int(coord[1]):int(coord[3]),int(coord[0]):int(coord[2])]
    ims = []
    # cut = cv2.imread(img)
    im = cv2.resize(img, (94, 24))
    im = transform(im)
    ims.append(im)
    ims = torch.Tensor(ims)
    lprnet = build_lprnet(lpr_max_len=8, phase=True, class_num=len(CHARS), dropout_rate=0.5)
    device = torch.device("cuda:0" if True else "cpu")
    lprnet.to(device)
    lprnet.load_state_dict(torch.load(r"G:\b_zhan\yolov5-master\lprr\Final_LPRNet_model.pth"))
    prebs = lprnet(ims.to(device))  # classifier prediction
    prebs = prebs.cpu().detach().numpy()
    preb_labels = list()
    for i in range(prebs.shape[0]):
        preb = prebs[i, :, :]  # 对每张图片 [68, 18]
        preb_label = list()
        for j in range(preb.shape[1]):  # 18  返回序列中每个位置最大的概率对应的字符idx  其中'-'是67
            preb_label.append(np.argmax(preb[:, j], axis=0))
        no_repeat_blank_label = list()
        pre_c = preb_label[0]
        if pre_c != len(CHARS) - 1:  # 记录重复字符
            no_repeat_blank_label.append(pre_c)
        for c in preb_label:  # 去除重复字符和空白字符'-'
            if (pre_c == c) or (c == len(CHARS) - 1):
                if c == len(CHARS) - 1:
                    pre_c = c
                continue
            no_repeat_blank_label.append(c)
            pre_c = c
        preb_labels.append(no_repeat_blank_label)

    plat_num = np.array(preb_labels)
    # print(plat_num)
    return plat_num
def dr_plate(im0,coord,plat_num):
    x1=int(coord[0])
    x2=int(coord[1])
    plate=np.array(plat_num)
    a=""
    for i in range(0,plate.shape[1]):
        b=CHARS[plate[0][i]]
        a+=b

    cv2.putText(im0,a,(x1,x2),0,1,(255,0,0), thickness=2,
                            lineType=cv2.LINE_AA)