import os
import os.path as osp
import torch
from PIL import Image
from download_pt import download_file_from_google_drive

class Dectect_Ingrd:
    def __init__(self, pt='last'): #defalut : last.pt
        dir_path = os.path.dirname(os.path.realpath(__file__))
        last_pt_path = os.path.join(dir_path, 'ingrd_yolov5m_last.pt')
        best_pt_path = os.path.join(dir_path, 'ingrd_yolov5m_best.pt')

        if pt == 'best':    
            pt = best_pt_path
            pt_file_id = '1hKzz9biYDxk7HJozX05esTEuot7YUPse'
        else:
            pt = last_pt_path
            pt_file_id = '1faMy4fwzHAmvOkvH_-Y4AkNSCTjAjh87'
        
        if not os.path.exists(pt):
            print('download pt from google drive...')
            download_file_from_google_drive(pt_file_id, pt)
            print('download complete!')

        self.model = torch.hub.load('ultralytics/yolov5', 'custom', path=pt)

    def detect(self, input_img_path, dest_img_path='result'): #return np_result, img_result_path
        img = Image.open(input_img_path)

        self.result = self.model(img)
        self.np_result = self.result.pandas().xyxy[0].to_numpy()
        self.ingrd_list = [self.np_result[i][-1] for i in range(len(self.np_result))]

        # save img in dest_img_path/test.jpg
        self.result.save(dest_img_path)
        dest_img = osp.join(os.getcwd(),osp.join(dest_img_path, 'test.jpg')) #절대 경로

        return self.np_result, dest_img
    
    def get_result_ingrd_list(self):
        return self.ingrd_list

    def get_xyxy_ingrd(self, ingrd):
        if ingrd in self.ingrd_list:
            idx = self.ingrd_list.index(ingrd)
            return True, self.np_result[idx][:4]
        else:
            return False, "no such ingrd"

if __name__ == "__main__":
    detection = Dectect_Ingrd() #Dectect_Ingrd('best')
    np_result, img_result = detection.detect("E:/test.jpg") #for test

    # xmin / ymin / xmax / ymax / confidence / class / name
    print(np_result)
    print(img_result)
    print(detection.get_result_ingrd_list())
    
    _, xyxy = detection.get_xyxy_ingrd('paprika')
    print(xyxy)