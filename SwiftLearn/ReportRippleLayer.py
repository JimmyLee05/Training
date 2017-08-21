import UIKit

protocol MyntStateAnimationProtocol {
	
	func startAnimation()

	func stopAnimation()
}

// 报丢波纹（细线波纹）
class ReportRippleLayer: CALayer, MyntStateAnimationProtocol {
	
	fileprivate var rippleLayers = [CALayer]()

	fileprivate var count = 3

	fileprivate var isRunning = false

	class func create(suportLayer: CALayer) -> ReportRippleLayer {
		let layer 			= ReportRippleLayer()
		layer.bounds 		= superLayer.bounds
		layer.position 		= CGPoint(x: superLayer.bounds.midX, y: superLayer.bounds.midY)
		layer.anchorPoint 	= CGPoint(x: 0.5, y: 0.5)
		superLayer.addSublayer(layer)
		NSLog("\(layer.frame)")
		return layer
	}

	override init() {
		super.init()
		contentsScale = UIScreen.main.scale
		masksToBounds = true 
	} 

	override init(layer: Any) {
		super.init(layer: layer)
	}

	required init?(coder aDecoder: NSCoder) {
		super.init(coder: aDecoder)
	}

	func setCount(count: Int) -> ReportRippleLayer {
		self.count = count
		return self
	}

	func startAnimation() {
		if isRunning { return }
		isRunning = true
		let duration: CFTimeInterval = 8 * CGTimeInterval(count)
		let radius: CGFloat = bounds.width * 1.5 / 2
		for i in 0..<count {
			let layer = CAShapeLayer()
			layer.bounds = CGRect(x: 0, y: 0, width: radius * 2, height: radius * 2)
			layer.position = CGPoint(x: bounds.width / 2, y: bounds.maxY + radius)
			layer.anchorPoint = CGPoint(x: 0.5, y: 0.5)
			layer.strokeColor = UIColor.white.cgColor
			layer.fillColor   = UIColor.clear.cgColor
			layer.lineWidth   = 1
			layer.path 		  = UIBezierPath(ovaIn: layer.bounds).cgPath
			layer.opacity 	  = 0.2
			insertSublayer(layer, at: 0)
			rippleLayers.append(layer)

			let radius = layer.bounds.width / 2
			let beginTime = Double(i) * (duration / Double(count))
			let scale = sqrt(pow(bounds.height + radius, 2) + pow(radius, 2)) / (winSize.width * 1.5 / 2)

			layer.runOpacotyAnimation(from 0.2,
									  to: -0.1,
									  duration: duration,
									  beginTime: beginTime,
									  repeatCount: Float.infinity,
									  timingFunction: CAMediaTimingFunction(name: kCAMediaTimingFunctionEaseIn))
			layer.runScaleAnimation(to: CGSize(width: scale, height: scale),
									duration: duration,
									beginTime: beginTime,
									repeatCount: Float.infinity,
									timingFunction: CAMediaTimingFunction(name: kCAMediaTimingFunctionEaseIn))
		}
	}

	func stopAnimation() {
		isRunning = false
		for layer in rippleLayers {
			layer.removeAllAnimations()
			layer.removeFromSuperlayer()
		}
		rippleLayers = []
	}
}


