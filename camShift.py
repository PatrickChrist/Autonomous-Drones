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
		masked_dst = np.multiply(self.dst,mask)
		tmp_dst = np.array(masked_dst)
		denstity_mask_sum = masked_dst.sum()
  		density = int(denstity_mask_sum/(ret[1][0]*ret[1][1]))
		#cv2.putText(tmp_dst, "Current Density", (10, 70), font, 1, (255,255,255),2, cv2.Line_AA)
		cv2.putText(tmp_dst, "Current Density: " + str(density), (10,120), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255))
  		if self.initial_histogram_density != None:
  			cv2.putText(tmp_dst, "Original Density: " + str(self.initial_histogram_density), (10,70), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255))
		if self.initialArea != None:
			ratioCurrentToInitialArea = (ret[1][0]*ret[1][1]) / self.initialArea
			if ratioCurrentToInitialArea < 1:
				density = density *(1+ 1.5*(1-ratioCurrentToInitialArea)) #correction factor: if the square is farther away, the density usually decreases 
		cv2.imshow("masked dst",tmp_dst)


		return density

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
		self.meanHue = None
		self.isFirstTime = True
		self.initialArea = None

	def performCamShift(self, camImage):

		if camImage != None and camImage != []:
			self.hsv = cv2.cvtColor(camImage, cv2.COLOR_BGR2HSV)
			self.dst = cv2.calcBackProject([self.hsv],[0],self.roi_hist,[0,180],1)
			cv2.imshow("histo",self.dst)

			"""hsv_lower_bound = np.array([0, 50, 50],np.uint8)
			hsv_upper_bound = np.array([180, 255, 255],np.uint8)	

			maskHSV = cv2.inRange(self.hsv, hsv_lower_bound, hsv_upper_bound)
			self.dst = cv2.bitwise_and(self.dst, self.dst, mask=maskHSV)
			
            mask = np.zeros(self.dst.shape, np.uint8)
			for i in range(0,self.dst.shape[0]-1):
				for j in range(0,self.dst.shape[1]-1):
					if self.hsv[i][j][2] in range(50,200):
						mask[i][j] = 1

			self.dst = np.multiply(self.dst, mask)
			"""
			# apply meanshift to get the new location
			tmp_ret, tmp_track_window = cv2.CamShift(self.dst, self.track_window, self.term_crit)
			tmp_pts = boxPoints(tmp_ret)
			tmp_pts = np.int0(tmp_pts)

			# calc density
			if self.isFirstTime:
				self.initial_histogram_density = self.get_current_histogram_density(tmp_ret, tmp_pts)
				self.initialArea = tmp_ret[1][0]*tmp_ret[1][1]
				self.isFirstTime = False
				current_histogramm_density = self.initial_histogram_density
				current_length_width_ratio = 1
			else:
				current_histogramm_density = self.get_current_histogram_density(self.ret, self.pts)
				if tmp_ret[1][1] != 0:
					current_length_width_ratio = tmp_ret[1][0]/float(tmp_ret[1][1])
				else:
					current_length_width_ratio = 0

			if self.isFirstTime or self.ret == None:
				ratio_lastWH_and_currentWH = 1
			else:
				#ratio_lastWH_and_currentWH = 1
				if (tmp_ret[1][1] != 0 and self.ret[1][1] != 0):
					ratio_lastWH_and_currentWH = (self.ret[1][0]/self.ret[1][1])/float(tmp_ret[1][0]/tmp_ret[1][1])
			
			if self.initial_histogram_density*0.5 < current_histogramm_density and current_length_width_ratio > 0.5 and current_length_width_ratio < 2 and ratio_lastWH_and_currentWH > 0.5 and ratio_lastWH_and_currentWH < 2:
				self.ret = tmp_ret
				self.track_window = tmp_track_window
				self.pts = tmp_pts
				self.border_color = (0,255,0)
				success = True
			else:
				self.border_color = (255,0,0)
				success = False

			if self.pts != None:
				self.img2 = camImage.copy()

				# Draw rectangle on image
				cv2.polylines(self.img2, [self.pts], True, self.border_color, 2)

				# Draw middlepunkt on image
				self.middleX = int(self.ret[0][0])
				self.middleY = int(self.ret[0][1])
				cv2.circle(self.img2,(self.middleX, self.middleY), 2, (10,255,255))
				return success, self.img2, self.middleX, self.middleY, min(self.ret[1][0], self.ret[1][1])
			
			else:
				return camImage, 0, 0, 0

		else:
			print 'No cam Image'
	 
	def close(self):
	 	cv2.destroyAllWindows()