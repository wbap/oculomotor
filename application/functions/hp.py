import brica
import numpy as np
import cv2
import math
from oculoenv.geom import Matrix4

class HP(object):
    """ Hippocampal formation module.

    Create allocentric panel image.
    """
    
    def __init__(self):
        self.timing = brica.Timing(2, 1, 0)

        # Allocantric panel map image
        self.map_image = np.zeros((128, 128, 3), dtype=np.uint8)
        
    def __call__(self, inputs):
        if 'from_retina' not in inputs:
            raise Exception('HP did not recieve from Environment')

        # This image input from environment is a kind of cheat and not biologically
        # acculate.
        if inputs['from_retina'] is not None:
            image, angle = inputs['from_retina'] # (128, 128, 3), (2)

            # Transform input image into allocentric panel image
            transforemed_image = self._extract_transformed_image(image, angle)

            # Overlay into existing map image
            self._overlay_extracted_image(self.map_image, transforemed_image)
        
        return dict(to_pfc=self.map_image)

    def _get_perspective_mat(self, fovy, aspect_ratio, znear, zfar):
        ymax = znear * math.tan(fovy * math.pi / 360.0)
        xmax = ymax * aspect_ratio

        t  = 2.0 * znear
        t2 = 2.0 * xmax
        t3 = 2.0 * ymax
        t4 = zfar - znear
    
        m = [[t/t2,  0.0,              0.0, 0.0],
             [0.0,  t/t3,              0.0, 0.0],
             [0.0,   0.0, (-zfar-znear)/t4, -1.0],
             [0.0,   0.0,     (-t*zfar)/t4, 0.0]]
        m = np.transpose(np.array(m, dtype=np.float32))
        mat = Matrix4(m)
        return mat

    def _extract_transformed_image(self, image, angle):
        # In order to use black color as a blank mask, set lower clip value for
        # input image
        mask_threshold = 3
    
        image = np.clip(image, mask_threshold, 255)
    
        angle_h = angle[0]
        angle_v = angle[1]
    
        m0 = Matrix4()
        m1 = Matrix4()
        m0.set_rot_x(angle_v)
        m1.set_rot_y(angle_h)
        camera_mat = m1.mul(m0)
        camera_mat_inv = camera_mat.invert()

        camera_fovy = 50
        pers_mat = self._get_perspective_mat(camera_fovy, 1.0, 0.04, 100.0)

        mat = pers_mat.mul(camera_mat_inv)
    
        plane_distance = 3.0
        
        point_srcs = [[ 1.0, 1.0, -plane_distance, 1.0],
                      [-1.0, 1.0, -plane_distance, 1.0],
                      [-1.0,-1.0, -plane_distance, 1.0],
                      [ 1.0,-1.0, -plane_distance, 1.0]]

        point_src_2ds = []
        point_dst_2ds = []
    
        for point_src in point_srcs:
            ps_x = (point_src[0] * 0.5 + 0.5) * 127.0
            ps_y = (-point_src[1] * 0.5 + 0.5) * 127.0
            point_src_2ds.append([ps_x, ps_y])
        
            p = mat.transform(np.array(point_src, dtype=np.float32))
            w = p[3]
            x = p[0]/w
            y = p[1]/w
            pd_x = (x * 0.5 + 0.5) * 127.0
            pd_y = (-y * 0.5 + 0.5) * 127.0
            point_dst_2ds.append([pd_x, pd_y])

        point_src_2ds = np.float32(point_src_2ds)
        point_dst_2ds = np.float32(point_dst_2ds)

        h,w,c = image.shape

        M = cv2.getPerspectiveTransform(point_dst_2ds, point_src_2ds)
        transformed_image = cv2.warpPerspective(image, M, (h,w))
        return transformed_image

    def _overlay_extracted_image(self, base_image, ext_image):
        GRID_DIVISION = 8
        GRID_WIDTH = 128 // GRID_DIVISION
    
        for ix in range(GRID_DIVISION):
            pixel_x = GRID_WIDTH * ix
            for iy in range(GRID_DIVISION):
                pixel_y = GRID_WIDTH * iy
                base_region_image = base_image[pixel_y:pixel_y+GRID_WIDTH,
                                               pixel_x:pixel_x+GRID_WIDTH, :]
                ext_region_image = ext_image[pixel_y:pixel_y+GRID_WIDTH,
                                             pixel_x:pixel_x+GRID_WIDTH, :]
                ext_region_image_sum = np.sum(ext_region_image, axis=2)
                has_zero = np.any(ext_region_image_sum==0)
                if not has_zero:
                    base_image[pixel_y:pixel_y+GRID_WIDTH,
                               pixel_x:pixel_x+GRID_WIDTH, :] = ext_region_image // 2 + base_region_image // 2

