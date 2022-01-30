import math
import cv2
import numpy as np
import scipy.spatial as spatial
import scipy.cluster as cluster
from collections import defaultdict
from datetime import datetime
import tensorflow as tf



class BoardRecognition:
    def __init__(self, path_to_model):
        self.model = tf.keras.models.load_model(path_to_model)


    def load_image(self, filename):
        return cv2.imread(filename)

    def prepare_image(self, image):
        img_bw = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        img_blur = cv2.GaussianBlur(img_bw, (5,5), 0)
        return img_blur

    def get_points(self, image, min_line_length = 500, max_line_gap = 10):
        cv2.imwrite("image.png", image)
        # image = self.prepare_image(image)
        image_edges = cv2.Canny(image, 200, 225)
        # cv2.imshow("canny", image_edges)
        lines = cv2.HoughLines(image_edges, 1, np.pi / 180, 200, min_line_length, max_line_gap)
        lines = np.reshape(lines, (-1, 2))
        horizontal_lines, vertical_lines = list(), list()
        for rho, theta in lines:
            if theta < np.pi / 5 or theta > np.pi - np.pi / 5:
                vertical_lines.append([rho, theta])
            elif 70*np.pi/180 < theta < 110*np.pi/180:
                horizontal_lines.append([rho, theta])

        intersection_points = list()
        for r_hor, th_hor in horizontal_lines:
            for r_ver, th_ver in vertical_lines:
                a = np.array([[np.cos(th_hor), np.sin(th_hor)], [np.cos(th_ver), np.sin(th_ver)]])
                b = np.array([r_hor, r_ver])
                intersection_point = np.linalg.solve(a, b)
                intersection_points.append(intersection_point)
        # print(f"intersection: {len(intersection_points)}")
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
        # print(f"clusters: {len(clusters)}")
        return clusters

    def draw_points(self, image, points, name):
        image_copy = np.copy(image)
        for idx, point in enumerate(points):
            x,y = point
            x,y = int(x), int(y) 
            cv2.line(image_copy, (x,y), (x,y), (0,255,0), 10)
            # print(f"x: {x}, y: {y}")
            # cv2.putText(image_copy,f"{idx}",(x,y),cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
        cv2.imwrite(name, image_copy)
        

    def crop_squares(self, image, points, name="board", save=False):
        if len(points) != 81:
            print("wrong number of points!")
            return
        coords = list(filter(lambda k: (k%2 == 1 and k%9 != 8), list(range(70))))
        squares = list()
        for idx,coord in enumerate(coords):
            top_left, bottom_right = points[coord], points[coord+10]
            top_left_x, top_left_y = [int(x) for x in top_left]
            bottom_right_x, bottom_right_y = [int(x) for x in bottom_right]
            square = image[top_left_y:bottom_right_y+1,top_left_x:bottom_right_x+1]
            if save:
                cv2.imwrite(f"squares/{name}-{idx}.png", square)
            squares.append(square)
            # cv2.imshow(f"{idx}", square)
            # cv2.waitKey(100)
        return squares

    def create_fen(self, squares):
        fen = ""
        empty_counter = 0
        translation = ["b", "B", "empty", "w", "W"]
        squares = np.reshape(squares, (8,4))
        print(squares.shape)

        for row in range(8):
            for col in range(4):
                square = squares[row][col]
                square = cv2.resize(square, (224,224))
                square = np.array(square)/255.0
                square = square[np.newaxis, ...]
                predicted = self.model.predict(square)[0]
                idx = predicted.argmax()
                if translation[idx] == "empty":
                        empty_counter += 1
                else:
                    if empty_counter > 0:
                        fen+= str(empty_counter)
                    fen += translation[idx]
                    empty_counter = 0
            if empty_counter > 0:
                fen+= str(empty_counter)
            if row != 7:
                fen += "/"
            empty_counter = 0
        return fen


if __name__ == "__main__":
    br1 = BoardRecognition("new_new_model")
    # image = br1.load_image("photo-171516.png")
    image = br1.load_image("board-22.png")
    points = br1.get_points(image)
    # br1.draw_points(image, points, "points")
    squares = br1.crop_squares(image, points)
    fen = br1.create_fen(squares)
    print(fen)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


