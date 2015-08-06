import numpy as np
import cv2

usesOpenCV3 = False

def boxPoints(ret):
	if (usesOpenCV3 == True):
		return cv2.boxPoints(ret)
	else:
		return cv2.cv.BoxPoints(ret)

class CamShift(object):
	def get_current_histogram_density(self, ret, pts):
		mask = np.zeros(self.dst.shape, np.uint8)
		cv2.fillPoly(mask, [pts], (255, 255, 255))
		mask = mask/255
		masked_dst = cv2.bitwise_and(self.dst.copy(), mask)
		denstity_mask_sum = masked_dst.sum()
		return int(denstity_mask_sum/(ret[0][0]+ret[0][1]))

	def __init__(self,c,r,w,h,initialCamImage):

		# take first frame of the video
		self.frame = initialCamImage

		# setup initial location of window
		self.track_window = (int(c),int(r),int(w),int(h))

		# set up the ROI for tracking
		self.roi = self.frame[r:r+h, c:c+w]
		self.hsv_roi =  cv2.cvtColor(self.roi, cv2.COLOR_BGR2HSV)
		self.mask = cv2.inRange(self.hsv_roi, np.array((0., 60.,32.)), np.array((180.,255.,255.)))
		self.roi_hist = cv2.calcHist([self.hsv_roi],[0],self.mask,[180],[0,180])
		cv2.normalize(self.roi_hist,self.roi_hist,0,255,cv2.NORM_MINMAX)

		# Setup the termination criteria, either 10 iteration or move by atleast 1 pt
		self.term_crit = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1)

		self.middleX = 0
		self.middleY = 0

		self.skip_commands = False
		self.initial_histogram_density = None
		self.pts = None
		self.ret = None


	def performCamShift(self, camImage):

		if camImage != None and camImage != []:
			self.hsv = cv2.cvtColor(camImage, cv2.COLOR_BGR2HSV)
			self.dst = cv2.calcBackProject([self.hsv],[0],self.roi_hist,[0,180],1)

			# apply meanshift to get the new location
			tmp_ret, tmp_track_window = cv2.CamShift(self.dst, self.track_window, self.term_crit)
			tmp_pts = boxPoints(tmp_ret)
			tmp_pts = np.int0(tmp_pts)

			# calc density
			if self.initial_histogram_density == None:
				self.initial_histogram_density = self.get_current_histogram_density(tmp_ret, tmp_pts)
			
			current_histogramm_density = self.get_current_histogram_density(tmp_ret, tmp_pts)
			current_length_width_ratio = tmp_ret[1][0]/float(tmp_ret[1][1])
			if self.initial_histogram_density*0.6 < current_histogramm_density and current_length_width_ratio>0.5 and current_length_width_ratio<2 :
				self.ret = tmp_ret
				self.track_window = tmp_track_window
				self.pts = tmp_pts
				self.border_color = (0,255,0)
			else:
				self.border_color = (255,0,0)

			if self.pts != None:
				self.img2 = camImage.copy()

				# Draw rectangle on image
				cv2.polylines(self.img2, [self.pts], True, self.border_color, 2)

				# Draw middlepunkt on image
				self.middleX = int(self.ret[0][0])
				self.middleY = int(self.ret[0][1])
				cv2.circle(self.img2,(self.middleX, self.middleY), 2, (10,255,255))
				return self.img2, self.middleX, self.middleY, min(self.ret[1][0], self.ret[1][1])
			
			else:
				return camImage, 0, 0, 0

		else:
			print 'No cam Image'
	 
	def close(self):
	 	cv2.destroyAllWindows()