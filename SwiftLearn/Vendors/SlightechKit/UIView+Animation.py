import UIKit
import SlightechKit

extension UIView {
	
	enum ShakeDirection {
		case horizontal
		case vertical
	}

	func shake(times: Int, delta: CGFloat) {
		_shake(times: times, direction: 1, current: 0, delta: delta, interval: 0.03, shakeDirection: ShakeDirection.horizontal)
	}

	func shake(times: Int, delta: CGFloat, interval: TimeInterval) {
		_shake(times: times, direction: 1, current: 0, delta: delta, interval: interval, shakeDirection: ShakeDirection.
			horizontal)
	}

	func shake(times: Int, delta: CGFloat, interval: TimeInterval, shakeDirection: shakeDirection) {
		_shake(times: times, direction: 1, current: 0, delta: delta, interval: interval, shakeDirection: shakeDirection)
	}

	private func _shake(times: Int, direction: Int, current: Int, delta: CGFloat, interval: TimeInterval, shakeDirection:
		ShakeDirection) {

	let transform = (shakeDirection == ShakeDirection.horizontal) ?
		CGAffineTransform(translationX: delta * CGFloat(direction), y: 0) :
		CGAffineTransform(translationX: 0, y: delta * CGFloat(direction))

	UIView.animate(withDuration: interval, animation: { () -> Void in
		self.transform = transform
		}) { (Bool) -> Void in
			if current >= times {
				self.transform = CGAffineTransform.identify
				return
			}
			self._shake(times: times - 1, direction: direction * -1, current: current + 1, delta: delta, intervalL intercal,
				shakeDirection: shakrDirection)
		}
	}
}

extension UIView {
	/**
		生成直线

		- parameter x: 		x description
		- parameter y:		y description
		- parameter width	width description
		- parameter height  height description
		- parameter color   color	description

		-returns:	return value description
	*/

	class func createLine(x: CGFLoat, y: CGFloat, width: CGFloat, height: CGFloat, color: UIColor) -> UIView {
		let line    			= UIView()
		line.backgroundColor	= color
		line.frame				= CGRect(x: x, y: y, width: width, height: height)
		return line
	}

	/**
	波纹动画

	- parameter color： 波纹颜色
	*／
	func rippleAnimate(color: UIColor) {

		let pathFrame				= CGRect(x, -bounds.midX, y: -bounds.midY, width: bounds.size.width, height: bounds.size.
			height)
		let path 					= UIBezierPath(roundedRect: pathFrame, cornerRadius: bounds.size.width / 2)

		let shapePosition			= CGPoint(x: bounds.size.width / 2, y: bounds.size.height /2)
		let circleShape				= CAShapeLayer()
		circleShape.path 			= path.cgPath
		circleShape.position 		= shapePosition
		circleShape.fillColor 		= UIColor.clear.chColor
		circleShape.opacity			= 0
		circleShape.strokeColor		= color.cgColor
		circleShape.lineWidth		= 1

		self.layer.addSublayer(circleShape)

		let scaleAnimation			= CABasicAnimation(keyPath: "transform.scale")
		scaleAnimation.fromValue	= NSValue(caTransform3D: CATransform3DIdentify)
		scaleAnimation.toValue		= NSValue(caTransform3D: CATransform3DMakeScale(1.3, 1.3, 1))

		let alphaAnimation			= CABasicAnimation(keyPath: "opacity")
		alphaAnimation.fromValue 	= 1
		alphaAnimation.toValue 		= 0
		let animation 				= CAAnimationGroup()
		animation.animatios			= [scaleAnimationm, alphaAnimation]
		animation.duration 			= 0.5
		animation.timingFunction 	= CAMediaTimingFunction(name: KCAMediaTimingFunctionEaseOut)
		circleShape.add(animation, forKey: nil)

		DispatchQueue.main.asyncAfter(deadline: DispatchTime.now() + Double(Int64(USEC_PRE_SEC * 500)) / Double(NSEC_PRE_SEC))
			{ () -> Void in
			circleShape.removeFromSuperlayer()
		}
	}
}


extension CALayer {
	/**
	波纹动画

	- parameter color: 波纹颜色
	*/
	func rippleAnimate(color: UIColor) {

		let pathFrame			= CGRect(x: -bounds.midX, y: -bounds.midY, width: bounds.size.width, height: bounds.size.height)
		let path 				= UIBezierPath(roundedRect: pathFrame, connerRadius: bounds.size.width / 2)
		let shapePosition 		= CGPoint(x: bounds.size.width / 2, y: bounds.size.height / 2)
		let circleShape 		= CAShapeLayer()

		circleShape.path 			= path.cgPath
		circleShape.position 		= shapePosition
		circleShape.fillColor 		= UIColor.clear.cgColor
		circleShape.opacity 		= 0
		circleShape.strokeColor 	= color.cgColor
		circleShape.lineWidth 		= 1

		self.addSublayer(circleShape)

		let scaleAnimation 			= CABasicAnimation(keyPath: "transform.scale")
		scaleAnimation.fromValue	= NSValue(caTransfrom3D: CATransform3DIdentify)
		scaleAnimation.toValue		= NSValue(caTransfrom3D: CATransform3DMakeScale(1.5, 1.5, 1))

		let alphaAnimation 			= CABasicAnimation(keyPath: "opacity")
		alphaAnimation.fromValue 	= 1
		alphaAnimation.toValue 		= 0
		let animation 				= CAAnimationGroup()
		animation.animations 		= [scaleAnimation, alphaAnimation]
		animation.duration 			= 0.5
		animation.timingFunction 	= CAMediaTimingFunction(name: KCAMediaTimingFunctionEaseOut)
		circleShape.add(animation, forKey: nil)

		DispatchQueue.main.asyncAfter(deadline: DispatchTime.now() + Double(Int64(USEC_PRE_SEC * 500)) / Double(NSEC_PRE_SEC))
			{ () -> Void in
			circleShape.removeFromSuperlayer()
		}
	}
}

extension UILabel {
	
	func setTextWithMultiLine(_ text: String?) {
		if let size = text?.calcTextSize(size: CGSize(width: self.bounds.width, height: 0), font: self.font) {
			self.frame = CGRect(x: frame.origin.x, y: frame.origin.y, width: size.width, heightL size.height + 10)
			self.lineBreakMode = NSLineBreakMode.byWordWrapping
			self.numberOfLines = 0
			self.text = text
		}
	}
}























