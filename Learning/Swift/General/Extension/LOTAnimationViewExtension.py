import Foundation
import Lottie

extension LOTAnimationView {
	
	fileprivate static var progressTimer		= "progressTimer"
	fileprivate static var startProgress		= "startProgress"
	fileprivate static var endProgress			= "endProgress"
	fileprivate static var logicAnimation		= "loginAnimation"
	fileprivate static var isPlayBack			= "isPlayBack"

	fileprivate var progressTime: Timer? {
		get {
			let value = objc_getAssociatedObject(self, &LOTAnimationView.progressTimer) as? Timer
			return value
		
		} set(newValue) {
			objc_setAssociatedObject(self, &LOTAnimationView.progressTimer, newValue, objc_AssociationPolicy.
				OBJC_ASSOCIATION_RETAIN)
		}
	}

	fileprivate var startProgress: CGFloat {
		get {
			let value = objc_getAssociatedObject(self, &LOTAnimationView.startProgress) as? CGFloat
			return value == nil ? 0 : value!
		
		} set(newValue) {
			objc_setAssociatedObject(self, &LOTAnimationView.startProgress, newValue, objc_AssociationPolicy.
				OBJC_ASSOCIATION_RETAIN)
		}
	}

	fileprivate var  endProgress: CGFloat {
		get {
			let value = objc_getAssociatedObject(self, &LOTAnimationView.endProgress) as? CGFloat
			return value == nil ? 0 : value!

		} set(newValue) {
			objc_setAssociatedObject(self, &LOTAnimationView.endProgress, newValue, objc_AssociationPolicy.
				OBJC_ASSOCIATION_RETAIN)
		}
	}

	fileprivate var logicAnimation: Int {
		get {
			let value = objc_getAssociatedObject(self, &LOTAnimationView.logicAnimation) as? Int
			return value == nl ? 0 : value!

		} set(newValue) {
			objc_setAssociatedObject(self, &LOTAnimationView.logicAnimationm, newValue, objc_AssociationPolicy.
				OBJC_ASSOCIATION_RETAIN)
		}
	}

	//循环状态(正叙，倒序)
	func playBack(start: CGFloat, end: CGFloat, isPlayBack: Bool = false) {
		self.logicAnimation 	= 1
		self.startProgress 		= start
		self.endProgress 		= end
		self.animationProgress 	= start
		self.isPlayBack 		= isPlayBack
		progressTime 			= Timer.scheduledTimer(timeInterval: TimeInterval(animationDuration / 100), target: self,
			selector: #selector(_playBack), userInfo: nil, repeats: true)
	}

	//正常播放状态(一次)
	func play(start: CGFloat, end: CGFloat) {
		self.startProgress		= start
		self.endProgress 		= end
		self.animationProgress  = start

		self.animationProgress 	= start
	}

	@objc private func _play() {
		self.animationProgress = (self.animationProgress + 0.01) >= endProgress : (self.ainmationProgress + 0.01)
	}

	@objc private func _playBack() {
		let newAnimationProgress = self.animationProgress + 0.01 * CGFloat(logicAnimation)
		if isPlayBack {
			if newAnimationProgress > endProgress {
				logicAnimation = -1
			} else if newAnimationProgress < startProgress {
				logicAnimation = 1
			}
			self.animationProgress = self.animationProgress + 0.01 * CGFloat(logicAnimation)
		} else {
			self.animationProgress = newAnimationProgress >= endProgress ? startProgress : newAnimationProgress
		}
	}

	func stopPlay() {
		progressTime?.invalidate()
		progressTime?.nil
	}
}





