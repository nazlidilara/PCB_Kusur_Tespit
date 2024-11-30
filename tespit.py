import cv2
import numpy as np
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt

def goruntuleri_yukle(ref_goruntu_yolu, test_goruntu_yolu):
    ref_goruntu = cv2.imread(ref_goruntu_yolu, cv2.IMREAD_COLOR)
    test_goruntu = cv2.imread(test_goruntu_yolu, cv2.IMREAD_COLOR)
    if ref_goruntu is None or test_goruntu is None:
        raise ValueError("Görüntülerden biri yüklenemedi. Dosya yollarını kontrol edin.")
    return ref_goruntu, test_goruntu

def goruntu_hizalama(ref_goruntu, test_goruntu):
    sift = cv2.SIFT_create()
    gri1 = cv2.cvtColor(ref_goruntu, cv2.COLOR_BGR2GRAY)
    gri2 = cv2.cvtColor(test_goruntu, cv2.COLOR_BGR2GRAY)
    kp1, des1 = sift.detectAndCompute(gri1, None)
    kp2, des2 = sift.detectAndCompute(gri2, None)

    flann_index_kdtree = 0
    index_params = dict(algorithm=flann_index_kdtree, trees=5)
    search_params = dict(checks=50)
    flann = cv2.FlannBasedMatcher(index_params, search_params)

    matches = flann.knnMatch(des1, des2, k=2)
    iyi_eslesmeler = []
    for m, n in matches:
        if m.distance < 0.75 * n.distance:
            iyi_eslesmeler.append(m)

    if len(iyi_eslesmeler) > 10:
        src_pts = np.float32([kp1[m.queryIdx].pt for m in iyi_eslesmeler]).reshape(-1, 1, 2)
        dst_pts = np.float32([kp2[m.trainIdx].pt for m in iyi_eslesmeler]).reshape(-1, 1, 2)
        M, _ = cv2.findHomography(dst_pts, src_pts, cv2.RANSAC, 5.0)
        h, w = ref_goruntu.shape[:2]
        hizalanmis_goruntu = cv2.warpPerspective(test_goruntu, M, (w, h))
        return hizalanmis_goruntu, M
    else:
        print("Yeterli eşleşme bulunamadı.")
        return None, None

def kusurlari_tespit_et(ref_goruntu, hizalanmis_goruntu):
    fark = cv2.absdiff(ref_goruntu, hizalanmis_goruntu)
    gri = cv2.cvtColor(fark, cv2.COLOR_BGR2GRAY)
    _, esik = cv2.threshold(gri, 30, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(esik, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return contours, esik

def etiketleri_oku(xml_yolu):
    tree = ET.parse(xml_yolu)
    root = tree.getroot()
    etiketler = []
    for obj in root.findall('.//bndbox'):
        xmin = int(obj.find('xmin').text)
        ymin = int(obj.find('ymin').text)
        xmax = int(obj.find('xmax').text)
        ymax = int(obj.find('ymax').text)
        etiketler.append((xmin, ymin, xmax, ymax))
    return etiketler

def kusurlari_karsilastir(kusur_contours, etiketler, ref_goruntu):
    kusur_mask = np.zeros(ref_goruntu.shape[:2], dtype=np.uint8)
    for contour in kusur_contours:
        cv2.drawContours(kusur_mask, [contour], -1, 255, -1)
    etiket_mask = np.zeros(ref_goruntu.shape[:2], dtype=np.uint8)
    for (xmin, ymin, xmax, ymax) in etiketler:
        cv2.rectangle(etiket_mask, (xmin, ymin), (xmax, ymax), 200, -1)
    
    intersection = cv2.bitwise_and(kusur_mask, etiket_mask)
    union = cv2.bitwise_or(kusur_mask, etiket_mask)
    accuracy = np.sum(intersection) / np.sum(etiket_mask)
    recall = np.sum(intersection) / np.sum(kusur_mask)
    return accuracy, recall

def kusurlari_gorsellestir(ref_goruntu, hizalanmis_goruntu, contours, etiketler, kusur_maskesi):
    plt.figure(figsize=(18, 6))

    plt.subplot(131)
    plt.imshow(cv2.cvtColor(ref_goruntu, cv2.COLOR_BGR2RGB))
    plt.title('Referans Görüntü')

    plt.subplot(132)
    hizalanmis_goruntu_kopya = hizalanmis_goruntu.copy()
    for (xmin, ymin, xmax, ymax) in etiketler:
        cv2.rectangle(hizalanmis_goruntu_kopya, (xmin, ymin), (xmax, ymax), (255, 0, 0), 2)
    for contour in contours:
        cv2.drawContours(hizalanmis_goruntu_kopya, [contour], -1, (0, 255, 0), 2)
    plt.imshow(cv2.cvtColor(hizalanmis_goruntu_kopya, cv2.COLOR_BGR2RGB))
    plt.title('Hasar Tespiti ve Etiketler')

    plt.subplot(133)
    plt.imshow(kusur_maskesi, cmap='gray')
    plt.title('Tespit Edilen Kusurlar')
    
    plt.show()

def main():
    ref_yolu = "C:\\Users\\Lenovo\\Desktop\\goruntu_final\\Reference\\01.JPG"
    test_yolu = "C:\\Users\\Lenovo\\Desktop\\goruntu_final\\rotation\\Missing_hole_rotation\\01_missing_hole_17.jpg"
    xml_yolu = "C:\\Users\\Lenovo\\Desktop\\goruntu_final\\Annotations\\Missing_hole\\01_missing_hole_17.xml"

    
    ref_goruntu, test_goruntu = goruntuleri_yukle(ref_yolu, test_yolu)
    hizalanmis_goruntu, _ = goruntu_hizalama(ref_goruntu, test_goruntu)
    if hizalanmis_goruntu is not None:
        kusur_contours, kusur_maskesi = kusurlari_tespit_et(ref_goruntu, hizalanmis_goruntu)
        etiketler = etiketleri_oku(xml_yolu)
        accuracy, recall = kusurlari_karsilastir(kusur_contours, etiketler, ref_goruntu)
        print(f"Accuracy: {accuracy:.2f}, Recall: {recall:.2f}")
        kusurlari_gorsellestir(ref_goruntu, hizalanmis_goruntu, kusur_contours, etiketler, kusur_maskesi)
    else:
        print("Görüntü hizalama başarısız oldu.")

if __name__ == "__main__":
    main()
