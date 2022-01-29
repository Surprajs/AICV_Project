import math
import cv2
import numpy as np
import scipy.spatial as spatial
import scipy.cluster as cluster
from collections import defaultdict
from datetime import datetime



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
        clusters = sorted(list(clusters), key=lambda k: k[1])
        for n in range(9):
            clusters[9*n:9*(n+1)] = sorted(clusters[9*n:9*(n+1)], key=lambda k: k[0])
        print(f"clusters: {len(clusters)}")
        return clusters

    def draw_points(self, image, points):
        image_copy = np.copy(image)
        for idx, point in enumerate(points):
            x,y = point
            x,y = int(x), int(y) 
            # cv2.line(image_copy, (x,y), (x,y), (0,255,0), 10)
            print(f"x: {x}, y: {y}")
            cv2.putText(image_copy,f"{idx}",(x,y),cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
        cv2.imshow("points", image_copy)
        

    def crop_squares(self, image, points):
        if len(points) != 81:
            print("wrong number of points!")
            return
        time = datetime.now().strftime("%H%M%S")
        coords = list(filter(lambda k: (k%2 == 1 and k%9 != 8), list(range(70))))
        for idx,coord in enumerate(coords):
            top_left, bottom_right = points[coord], points[coord+10]
            top_left_x, top_left_y = [int(x) for x in top_left]
            bottom_right_x, bottom_right_y = [int(x) for x in bottom_right]
            # cv2.imshow(f"{time}-{idx}",image[top_left_y:bottom_right_y+1,top_left_x:bottom_right_x+1])
            cv2.imwrite(f"squares/{time}-{idx}.png", image[top_left_y:bottom_right_y+1,top_left_x:bottom_right_x+1])


if __name__ == "__main__":
    br1 = BoardRecognition()
<<<<<<< HEAD
    image = br1.load_image("photo-18-03-23.png")
=======
    image = br1.load_image(".\calibration\calibration_images\photo-18-05-10.png")
>>>>>>> f136d45135cf15b7b912b8084654c92b9d5e096c
    points = br1.get_points(image)
    br1.draw_points(image, points)
    br1.crop_squares(image, points)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


