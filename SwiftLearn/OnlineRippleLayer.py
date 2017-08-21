import UIKit

//在线波纹(头像周边)
class OnlineRippleLayer: CALayer, MyntStateAnimationProtocol {
	
	fileprivate var rippleLayers = [CALayer]()

	class func create(targetView: UIView) -> OnlineRippleLayer {
		let layer 				= OnlineRippleLayer()
		layer.bounds 			= targetView.bounds
		layer.position 			= CGPoint(x: targetView.bounds.midX, y: targetView.bounds.midY)
		layer.anchorPoint 		= CGPoint(x: 0.5, y: 0.5)
		targetView.layer.insertSublayer(layer, below: targetView.layer)
		return layer
	}

	override init() {
		super.init()
		contentScale = UIScreen.mian.scale
	}

	override init(layer: Any) {
		super.init(layer: layer)
	}

	required init?(coder aDecoder: NSCoder) {
		super.init(coder: aDecoder)
	}

	func startAnimation() {
		for i in 0..<3 {
			let layer 				= CGShapeLayer()
			layer.bounds			= bounds
			layer.position 			= CGPoint(x: bounds.midX, y: bounds.midY)
			layer.anchorPoint 		= CGPoint(x: 0.5, y: 0.5)
			layer.fillColor 		= UIColor.white.cgColor
			layer.path 				= UIBezierPath(ovaIn: bounds).cgPath
			layer.opacity 			= 0.03
			insertSublayer(layer, at: 0)
			rippleLayers.append(layer)

			let duration: CFTimeInterval = 9
			let beginTime = Double(i) * 3

			layer.runOpacityAnimation(from: layer.opacity,
									  to: 0,
									  duration: duration,
									  beginTime: beginTime,
									  repeatCount: Float.infinity,
									  timingFounction: CAMediaTimingFunction(name: kCAMediaTimingFunctionEaseIn))
			layer.runScaleAnimation(to: CGSize(width: 2, height: 2),
									duration: duration,
									beginTime: beginTime,
									repeatCount: Float.infinity,
									timingFunction: CAMediaTimingFunction(name: kCAMediaTimingFunctionEaseIn))
		}		
	}

	func stopAnimation() {
		for layer in rippleLayers {
			layer.removeAllAnimations()
			layer.removeFromSuperlayer()
		}
		rippleLayers = []
	}
}

