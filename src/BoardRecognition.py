import math
import cv2
import numpy as np
import scipy.spatial as spatial
import scipy.cluster as cluster
from collections import defaultdict



class BoardRecognition:
    def __init__(self):
        pass


    def load_image(self, filename):
        return cv2.imread(filename)

    def prepare_image(self, image):
        img_bw = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        img_blur = cv2.GaussianBlur(img_bw, (5,5), 0)
        return img_blur

    def get_points(self, image, min_line_length = 200, max_line_gap = 50):
        image_edges = cv2.Canny(image, 200, 225)
        lines = cv2.HoughLines(image_edges, 1, np.pi / 180, 125, min_line_length, max_line_gap)
        lines = np.reshape(lines, (-1, 2))
        horizontal_lines, vertical_lines = list(), list()
        for rho, theta in lines:
            if theta < np.pi / 4 or theta > np.pi - np.pi / 4:
                vertical_lines.append([rho, theta])
            else:
                horizontal_lines.append([rho, theta])

        intersection_points = list()
        for r_hor, th_hor in horizontal_lines:
            for r_ver, th_ver in vertical_lines:
                a = np.array([[np.cos(th_hor), np.sin(th_hor)], [np.cos(th_ver), np.sin(th_ver)]])
                b = np.array([r_hor, r_ver])
                intersection_point = np.linalg.solve(a, b)
                intersection_points.append(intersection_point)
        print(f"intersection: {len(intersection_points)}")
        dists = spatial.distance.pdist(intersection_points)
        single_linkage = cluster.hierarchy.single(dists)
        flat_clusters = cluster.hierarchy.fcluster(single_linkage, 15, 'distance')
        cluster_dict = defaultdict(list)
        for i in range(len(flat_clusters)):
            cluster_dict[flat_clusters[i]].append(intersection_points[i])
        cluster_values = cluster_dict.values()
        clusters = map(lambda arr: (np.mean(np.array(arr)[:, 0]), np.mean(np.array(arr)[:, 1])), cluster_values)
        clusters = sorted(list(clusters), key=lambda k: [k[1], k[0]])
        print(f"clusters: {len(clusters)}")
        return clusters

    def draw_points(self, image, points):
        image_copy = np.copy(image)
        for idx, point in enumerate(points):
            x,y = point
            x,y = int(x), int(y) 
            # cv2.line(image_copy, (x,y), (x,y), (0,255,0), 10)
            cv2.putText(image_copy,f"{idx}",(x,y),cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
        cv2.imshow("points", image_copy)
if __name__ == "__main__":
    br1 = BoardRecognition()
    image = br1.load_image("bb.png")
    points = br1.get_points(image)
    br1.draw_points(image, points)

    cv2.waitKey(0)
    cv2.destroyAllWindows()


