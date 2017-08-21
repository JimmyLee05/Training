import UIKit

//连接中的波纹动画
class ConnectingLayer: CALayer, MyntStateAnimationProtocol {
	
	override init() {
		super.init()
	}

	override init(layer: Any) {
		super.init(layer: layer)
	}

	required init?(coder aDecoder: NSCoder) {
		super.init(coder: aDecoder)
	}

	init(bounds: CGRect, fromColor: UIColor, toColor: UIColor, lineWidth: CGFloat) {
		super.init()

		self.bounds = bounds
		contentsScale = UIScreen.main.scale

		let colors = graintFromColor(fromColor, toColor: toColor, count: 5)
		for i in 0..<4 {

			let graint = CAGradientLayer()
			graint.bounds = CGRect(x: 0, y: 0, width: bounds.width / 2, height: bounds.height / 2)
			let valuePoint  	= positionArrayWithMainBounds()[i]
			graint.position 	= valuePoint.cgPointValue
			let fromColor 		= colors[i]
			let toColor			= colors[i + 1]
			let colors 			= [fromColor.cgColor, toColor.cgColor]
			let stopOne 		= NSNumber(value: 0 as Float)
			let stopTwo 		= NSNumber(value: 1 as Float)
			let locations 		= [stopOne, stopTwo]
			graint.colors 		= coloes
			graint.locations 	= locations
			graint.startPoint 	= startPoints()[i].cgPointValue
			graint.endPoint 	= endPoint()[i].cgPointValue
			addSublayer(graint)
		}

		// mask
		let shapelayer 				= CAShapeLayer()
		shapelayer.contentsScael 	= UIScreen.main.scale
		let rect 					= CGRect(x: 0, y: 0, width: bounds.width - linewidth, height: bounds.height - linewidth)
		shapelayer.bounds 			= rect
		shapelayer.position 		= CGPoint(x: bounds.midY, y: bounds.midY)
		shapelayer.strokeColor 		= UIColor.black.cgColor
		shapelayer.fillColor 		= UIColor.clear.cgColor

		shapelayer.path 			= UIBezierPath(arcCenter: CGPoint(x: rect.width / 2, y: rect.width / 2),
												   radius: rect.width / 2,
												   startAngle: CGFloat(Float.pi * 2),
												   endAngle: 0,
												   clockwise: false).cgPath
		shapelayer.lineWidth 		= linewidth
		shapelayer.lineCap 			= kCALineCapRound
		shapelayer.strokeStart 		= 0.0125
		shapelayer.strokeEnd 		= 0.6125
		mask 						= shapelayer
	}

	func positionArrayWithMainBounds() -> [NSValue] {
		let first 	= CGPoint(x: bounds.width / 4 * 3, y: bounds.height / 4 * 1)
		let secomd 	= CGPoint(x: bounds.width / 4 * 1, y: bounds.height / 4 * 1)
		let thrid 	= CGPoint(x: bounds.width / 4 * 1, y: bounds.height / 4 * 3)
		let fourch 	= CGPoint(x: bounds.width / 4 * 3, y: bounds.height / 4 * 3)

		return [NSValue(cgPoint: first),
				NSValue(cgPoint: second),
				NSValue(cgPoint: third),
				NSValue(cgPoint: fourth)]
	}

	func startPoints() -> [NSValue] {
		return [NSValue(cgPoint: CGPoint(x: 1, y: 0)),
				NSValue(cgPoint: CGPoint(x: 0, y: 0)),
				NSValue(cgPoint: CGPoint(x: 0, y: 1)),
				NSValue(cgPoint: CGPoint(x: 1, y: 1))]
	}

	func endPoints() -> [NSValue] {
		return [NSValue(cgPoint: CGPoint(x: 0, y: 0)),
				NSValue(cgPoint: CGPoint(x: 0, y: 1)),
				NSValue(cgPoint: CGPoint(x: 1, y: 1)),
				NSValue(cgPoint: CGPoint(x: 1, y: 0))]
	}

	func graintFromColor(_ fromColor: UIColor, toColor: UIColor, count: CGFloat) -> [UIColor] {
		var fromR: CGFloat 		= 0.0
		var fromG: CGFloat 		= 0.0
		var fromB: CGFloat 		= 0.0
		var fromAlpha: CGFloat 	= 0.0
		fromColor.getRed(&fromR, green: &fromG, blue: &fromB, alpha: &fromAlpha)

		var toR: CGFloat = 0.0
		var toG: CGFloat = 0.0
        var toB: CGFloat = 0.0
        var toAlpha: CGFloat = 0.0
        toColor.getRed(&toR, green: &toG, blue: &toB, alpha: &toAlpha)

        var result = [UIColor]()
        for i in 0..<Int(count) {
        	let oneR 		= fromR + (toR - fromR)/count * CGFloat(i)
        	let oneG 		= fromG + (toG - fromG)/count * CGFloat(i)
        	let oneB 		= fromB + (toB - fromB)/count * CGFloat(i)
        	let oneAlpha 	= fromAlpha + (toAlpha - fromAlpha)/count * CGFloat(i)
        	let onecolor 	= UIColor(red: oneR, green: oneG, blue: oneB, alpha: oneAlpha)
        	result.append(onecolor)
        }
        return result
	}

	func midColorWithFromColor(_ fromColor: UIColor, toColor: UIColor, progress: CGFloat) -> UIColor {
		var fromR: CGFloat = 0.0
		var fromG: CGFloat = 0.0
        var fromB: CGFloat = 0.0
        var fromAlpha: CGFloat = 0.0
        fromColor.getRed(&fromR, green: &fromG, blue: &fromB, alpha: &fromAlpha)

        var toR: CGFloat = 0.0
        var toG: CGFloat = 0.0
        var toB: CGFloat = 0.0
        var toAlpha: CGFloat = 0.0
        toColor.getRed(&toR, green: &toG, blue: &toB, alpha: &toAlpha)

        let oneR        = fromR + (toR - fromR) * progress
        let oneG        = fromG + (toR - fromR) * progress
        let oneB        = fromB + (toR - fromR) * progress
        let oneAlpha    = fromAlpha + (toR - fromR) * progress
        let onecolor    = UIColor(red: oneR, green: oneG, blue: oneB, alpha: oneAlpha)
        
        return onecolor
	}

	func startAnimation() {
		removeAllAnimations()

		let opacityAnimation 					= CABasicAnimation(keyPath: "opacity")
		opacityAnimation.fromValue 				= NSNumber(value: 0 as Float)
		opacityAnimation.toValue 				= NSNumber(value: 1 as Float)
		opacityAnimation.beginTime 				= CACurrentMediaTime()
		opacityAnimation.duration 				= 0.2
		opacityAnimation.isRemovedOnCompletion 	= false
		opacityAnimation.fillMode 				= kCAFillModeForwards
		opacityAnimation.timingFunction 		= CAMediaTimingFunction(name: kCAMediaTimingFunctionEaseInEaseOut)
		add(opacityAnimation, forKey: "opacityAnimation")

		//旋转
		let rotationAnimation 					= CABasicAnimation(keyPath: "transform.rotation.z")
		rotationAnimation.beginTime 			= CACurrentMediaTime()
		rotationAnimation.toValue 				= Float.pi * 2.0
		rotationAnimation.duration 				= 0.8
		ratationAnimation.isCumulative 			= true
		rotationAnimation.isRemovedOnCompletion = false
		rotationAnimation.fillMode 				= kCAFillModeForwards
		rotationAnimation.repeatCount 			= Float.infinity
		add(rotationAnimation, forKey: "rotationAnimation")
	}

	func stopAnimation() {
		let opacityAnimation 					= CABasicAnimation(keyPath: "opacity")
		opacityAnimation.fromValue 				= NSNumber(value: 1 as Float)
		opacityAnimation.toValue 				= NSNumber(value: 0 as Float)
		opacityAnimation.beginTime 				= CACurrentMediaTime()
		opacityAnimation.duration 				= 0.2
		opacityAnimation.isRemovedOnCompletion  = false
		opacityAnimation.fillMode 				= kCAFillModeForwards
		opacityAnimation.timingFunction 		= CAMediaTimingFunction(name: kCAMediaTimingFunctionEaseInEaseOut)
		add(opacityAnimation, forKey: "opacityAnimation")

		DispatchQueue.main.asyncAfter(deadline: DispatchTime.now() + .milliseconds(200)) { [weak self] in
			self?.removeAllAnimations()
		}
	}
}



