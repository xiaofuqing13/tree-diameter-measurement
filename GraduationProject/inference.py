import os
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"
from mmdet.apis import init_detector, inference_detector, show_result_pyplot, show_result_ins,show_result
import mmcv
from PIL import Image
import numpy as np
import cv2


def inference(src,mtx, dist):
    config_file = 'config/solo/solo_r50_fpn_8gpu_3x.py'
    # download the checkpoint from model zoo and put it in `checkpoints/`
    checkpoint_file = 'checkpoints/epoch_100.pth'
    # build the model from a config file and a checkpoint file
    model = init_detector(config_file, checkpoint_file, device='cuda:0')

    # test a single image
    #demo = 'static/demo.jpg'
    result = inference_detector(model, src)

    img = mmcv.imread(src)

    h, w, _ = img.shape
    black = np.zeros((h, w, 3), np.uint8)
    black.fill(0)
    img_show = black.copy()
    cur_result = result[0]
    seg_label = cur_result[0]
    seg_label = seg_label.cpu().numpy().astype(np.uint8)
    cate_label = cur_result[1]
    cate_label = cate_label.cpu().numpy()
    score = cur_result[2].cpu().numpy()
    vis_inds = score > 0.25
    seg_label = seg_label[vis_inds]

    num_mask = seg_label.shape[0]
    cate_label = cate_label[vis_inds]
    cate_score = score[vis_inds]
    sort_by_density=False
    if sort_by_density:
        mask_density = []
        for idx in range(num_mask):
            cur_mask = seg_label[idx, :, :]
            cur_mask = mmcv.imresize(cur_mask, (w, h))
            cur_mask = (cur_mask > 0.5).astype(np.int32)
            mask_density.append(cur_mask.sum())
        orders = np.argsort(mask_density)
        seg_label = seg_label[orders]
        cate_label = cate_label[orders]
        cate_score = cate_score[orders]
    np.random.seed(42)
    color_masks = [
            np.random.randint(255, 256, (1, 3), dtype=np.uint8)
            for _ in range(num_mask)
        ]
    for idx in range(num_mask):
        idx = -(idx + 1)
        cur_mask = seg_label[idx, :, :]
        cur_mask = mmcv.imresize(cur_mask, (w, h))

        cur_mask = (cur_mask > 0.5).astype(np.uint8)
        if cur_mask.sum() == 0:
            continue

        color_mask = color_masks[idx]
        cur_mask_bool = cur_mask.astype(np.bool)
        img_show[cur_mask_bool] = black[cur_mask_bool] * 0 + color_mask * 1.0
        img_pil = Image.fromarray(np.uint8(img_show))
        img_pil.save("static/mask/trunk.jpg")
    show_result_ins(img,result, model.CLASSES, score_thr=0.25, out_file="static/testimg/instance_out.jpg")
    return img_show


