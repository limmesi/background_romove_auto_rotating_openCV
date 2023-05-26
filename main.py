import numpy as np
import cv2
import os


def read_images(root, files_names):
    return [{"image": cv2.imread(root + name),
             "name": name}
            for name in files_names]


def back_remove(image):
    gray_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray_img = cv2.GaussianBlur(gray_img, (5, 5), 0)

    threshold = cv2.threshold(gray_img, 250, 255, cv2.THRESH_BINARY_INV)[1]
    threshold = cv2.erode(threshold, np.ones((5, 5)), iterations=1)

    cut_image = cv2.bitwise_and(image, image, mask=threshold)

    h, w = cut_image.shape[:2]
    delta_w = 1500 - w
    delta_h = 1500 - h
    top, bottom = delta_h // 2, delta_h - (delta_h // 2)
    left, right = delta_w // 2, delta_w - (delta_w // 2)
    cut_image = cv2.copyMakeBorder(cut_image, top, bottom, left, right, cv2.BORDER_CONSTANT, value=0)
    cut_thresh = cv2.copyMakeBorder(threshold, top, bottom, left, right, cv2.BORDER_CONSTANT, value=0)

    return cut_image, cut_thresh


def rotate_image(image, mask):
    h, w = image.shape[:2]
    lines = cv2.HoughLinesP(mask, 1, np.pi/180, threshold=100, minLineLength=100, maxLineGap=10)
    x1, y1, x2, y2 = lines[0][0]
    angle = np.arctan2(y2-y1, x2-x1) * (-180) / np.pi + 90
    rotation_matrix = cv2.getRotationMatrix2D((w/2, h/2), -angle, 1)
    img_rotated = cv2.warpAffine(image, rotation_matrix, (w, h))

    gray = cv2.cvtColor(img_rotated, cv2.COLOR_BGR2GRAY)
    moments = cv2.moments(gray)
    cY = int(moments["m01"] / moments["m00"])
    cY = int(moments["m01"] / moments["m00"])
    centerY = cY / h
    centerY = cY / h
    if centerY > 0.5:
        img_rotated = cv2.rotate(img_rotated, cv2.ROTATE_180)

    img_resized = cv2.resize(img_rotated, (600, 600))

    return img_resized


if __name__ == "__main__":
    root_dir = 'komb/'
    files = os.listdir(root_dir)
    images = read_images(root_dir, files)

    for img in images:
        bg_removes, thresh = back_remove(img['image'])
        rotated = rotate_image(bg_removes, thresh)
        cv2.imshow(img['name'], rotated)
        cv2.waitKey(0)
