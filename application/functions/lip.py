import cv2
import numpy as np

import brica


GAUSSIAN_KERNEL_SIZE = (5,5)


class OpticalFlow(object):
    def __init__(self):
        """ Calculating optical flow.
        Input image can be retina image or saliency map. 
        """
        self.last_gray_image = None
        self.hist_32 = np.zeros((128, 128), np.float32)
        
        self.inst = cv2.optflow.createOptFlow_DIS(
            cv2.optflow.DISOPTICAL_FLOW_PRESET_MEDIUM)
        self.inst.setUseSpatialPropagation(False)
        self.flow = None
        
    def _warp_flow(self, img, flow):
        h, w = flow.shape[:2]
        flow = -flow
        flow[:,:,0] += np.arange(w)
        flow[:,:,1] += np.arange(h)[:,np.newaxis]
        res = cv2.remap(img, flow, None, cv2.INTER_LINEAR)
        return res
        
    def process(self, image, is_saliency_map=False):
        if image is None:
            return

        if not is_saliency_map:
            # Input is retina image
            gray_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        else:
            # Input is saliency map
            gray_image = np.clip(image * 255.0, 0.0, 255.0).astype(np.uint8)
            
        if self.last_gray_image is not None:
            if self.flow is not None:
                self.flow = self.inst.calc(self.last_gray_image,
                                           gray_image,
                                           self._warp_flow(self.flow, self.flow))
            else:
                self.flow = self.inst.calc(self.last_gray_image,
                                           gray_image,
                                           None)
            # (128, 128, 2)
        self.last_gray_image = gray_image
        return self.flow


class LIP(object):
    """ Retina module.

    This LIP module calculates saliency map and optical flow from retina image.
    """
    
    def __init__(self):
        self.timing = brica.Timing(2, 1, 0)

        self.optical_flow = OpticalFlow()

        self.last_saliency_map = None
        self.last_optical_flow = None

    def __call__(self, inputs):
        if 'from_retina' not in inputs:
            raise Exception('LIP did not recieve from Retina')

        retina_image = inputs['from_retina'] # (128, 128, 3)
        saliency_map = self._get_saliency_map(retina_image) # (128, 128)

        use_saliency_flow = False

        if not use_saliency_flow:
            # Calculate optical flow with retina image
            optical_flow = self.optical_flow.process(retina_image,
                                                     is_saliency_map=False)
        else:
            # Calculate optical flow with saliency map
            optical_flow = self.optical_flow.process(saliency_map,
                                                     is_saliency_map=True)
        
        # Store saliency map for debug visualizer
        self.last_saliency_map = saliency_map
        
        self.last_optical_flow = optical_flow
        
        return dict(to_fef=(saliency_map, optical_flow))

    def _get_saliency_magnitude(self, image):
        # Calculate FFT
        dft = cv2.dft(image.astype(np.float32), flags=cv2.DFT_COMPLEX_OUTPUT)
        magnitude, angle = cv2.cartToPolar(dft[:, :, 0], dft[:, :, 1])

        log_magnitude = np.log10(magnitude.clip(min=1e-10))

        # Apply box filter
        log_magnitude_filtered = cv2.blur(log_magnitude, ksize=(3, 3))

        # Calculate residual
        magnitude_residual = np.exp(log_magnitude - log_magnitude_filtered)

        # Apply residual magnitude back to frequency domain
        dft[:, :, 0], dft[:, :, 1] = cv2.polarToCart(magnitude_residual, angle)
    
        # Calculate Inverse FFT
        image_processed = cv2.idft(dft)
        magnitude, _ = cv2.cartToPolar(image_processed[:, :, 0],
                                       image_processed[:, :, 1])
        return magnitude

    def _get_saliency_map(self, image):
        resize_shape = (64, 64) # (h,w)

        # Size argument of resize() is (w,h) while image shape is (h,w,c)
        image_resized = cv2.resize(image, resize_shape[1::-1])
        # (64,64,3)

        saliency = np.zeros_like(image_resized, dtype=np.float32)
        # (64,64,3)
    
        channel_size = image_resized.shape[2]
    
        for ch in range(channel_size):
            ch_image = image_resized[:, :, ch]
            saliency[:, :, ch] = self._get_saliency_magnitude(ch_image)

        # Calclate max over channels
        saliency = np.max(saliency, axis=2)
        # (64,64)

        saliency = cv2.GaussianBlur(saliency, GAUSSIAN_KERNEL_SIZE, sigmaX=8, sigmaY=0)

        SALIENCY_ENHANCE_COEFF = 2.0 # Strong saliency contrst
        #SALIENCY_ENHANCE_COEFF = 0.5 # Low saliency contrast, but sensible for weak saliency

        # Emphasize saliency
        saliency = (saliency ** SALIENCY_ENHANCE_COEFF)

        # Normalize to 0.0~1.0
        saliency = saliency / np.max(saliency)
    
        # Resize to original size
        saliency = cv2.resize(saliency, image.shape[1::-1])
        return saliency
