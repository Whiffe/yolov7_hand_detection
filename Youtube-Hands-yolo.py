# 这一部分的代码是将Youtube-Hands数据集转化为yolo格式数据集
# Youtube-Hands：https://mingzhenhuang.com/projects/handler.html

import os,shutil
from PIL import Image

# xywh_xcycwh 的作用是把左上角的坐标xy，转化为中心坐标x_c,y_c，
# 并且把x_c,y_c,w,h都映射到0～1之间
# 这一个函数也是将Youtube-Hands的坐标转化为yolo格式坐标
def xywh_xcycwh(xywh,img_path):
    img = Image.open(img_path)
    imgSize = img.size  #大小/尺寸
    
    x_c = ( (float(xywh[0]) + float(xywh[2])/2.) ) / float(img.width)
    y_c = ( (float(xywh[1])+float(xywh[3])/2.) ) / float(img.height)
    w = float(xywh[2]) / float(img.width)
    h = float(xywh[3]) / float(img.height)
    xcycwh = '0 '+ str(x_c) + ' ' + str(y_c) + ' ' + str(w) + ' ' + str(h)
    return xcycwh

labels_path = './dataset/labels/'
images_path = './dataset/images/'

# 删除上一次运行产生的文件和文件夹
# 并重新创建新的文件夹结构
os.system('rm -r ./dataset')
os.system('mkdir -p ./dataset/{labels,images}/{train,test}')

# 遍历当前文件夹
for root, dirs, files in os.walk(".", topdown=False):
    for name in files:
        #gt.txt 中包含图片标注信息
        if name == 'gt.txt':
            txt_path = os.path.join(root, name)
            txt_con = open(txt_path)
            for txt_line in txt_con:
                if 'train' in txt_path:
                    # video_name是视频文件夹的名字
                    video_name = root.split('/train/')[1].split('/')[0]
                    # raw_frame_name是视频文件夹中对应图片的名字
                    raw_frame_name = 'frame' + txt_line.split(',')[0].zfill(6)+'.jpg'
                    # new_frame_name是yolo格式文件夹中对应图片的名字
                    new_frame_name = video_name + '_' + txt_line.split(',')[0].zfill(6)+'.jpg'
                    # new_txt_name是yolo格式文件夹中对应txt的名字
                    new_txt_name = video_name + '_' + txt_line.split(',')[0].zfill(6)+'.txt'
                    
                    # raw_frame_path是Youtube-Hands图片路径
                    raw_frame_path = root.split('gt')[0] + 'img1/' + raw_frame_name
                    
                    # new_image_path是yolo格式文件夹中对应图片路径
                    new_image_path = images_path+'train/'+new_frame_name
                    # label_txt_path是yolo格式文件夹中对应txt路径
                    label_txt_path = labels_path+'train/'+new_txt_name
                    
                    # 将Youtube-Hands的图片复制到yolo格式下的文件夹下
                    # 在复制的时候，图片名字是会发生改变
                    shutil.copyfile(raw_frame_path,new_image_path)
                    
                    # 提取出坐标信息，然后转化为yolo格式类别和坐标
                    element_t = txt_line.split(',')
                    
                    xywh = [element_t[2],element_t[3],element_t[4],element_t[5]]
                    xcycwh = xywh_xcycwh(xywh,raw_frame_path)
                    # yolo格式类别和坐标 存入label_txt_path的txt中，用的追加内容方式
                    with open(label_txt_path,"a") as file:   # a，代表追加内容
                        file.write(xcycwh+"\n")
                if 'test' in txt_path:
                    
                    video_name = root.split('/test/')[1].split('/')[0]
                    # 采用：str(int(float(txt_line.split(',')[0]))).zfill(6) 的原因是
                    # gt.txt中的第一类出现了1.0000，这不对，应该是1，所以代码进行了修正
                    raw_frame_name = 'frame' + str(int(float(txt_line.split(',')[0]))).zfill(6)+'.jpg'
                    new_frame_name = video_name + '_' + str(int(float(txt_line.split(',')[0]))).zfill(6)+'.jpg'
                    new_txt_name = video_name + '_' + str(int(float(txt_line.split(',')[0]))).zfill(6)+'.txt'
                    raw_frame_path = root.split('gt')[0] + 'img1/' + raw_frame_name
                    
                    new_image_path = images_path+'test/'+new_frame_name
                    label_txt_path = labels_path+'test/'+new_txt_name
                    
                    shutil.copyfile(raw_frame_path,new_image_path)
                    
                    element_t = txt_line.split(',')
                    
                    xywh = [element_t[2],element_t[3],element_t[4],element_t[5]]
                    xcycwh = xywh_xcycwh(xywh,raw_frame_path)
                    with open(label_txt_path,"a") as file:   # a，代表追加内容
                        file.write(xcycwh+"\n")

            txt_con.close()
