import UIKit
import MYNTKit

class MyntRingButton: UIView {
	
	private var _isRing = false

	private var _gradientLayer: CAGradientLayer!

	private var _textLayer: VerticalTextLayer!

	private var _ringBellLayer: CALayer!

	private var _ringBellLayer: CALayer!

	private var _ringContentLayer: CALayer!

	private var _normalColor = ColorStyle.kBlueGradientColor
	private var _selectionColor = ColorStyle.kGreenGradientColor

	override init(frame: CGRect) {
		super.init(frame: frame)
		_commitIn()
	}

	required init?(coder aDecoder: NSCoder) {
		super.init(coder: aDecoder)
		_commitIn()
	}

	private func _commitIn() {
		isUserInteractionEnabled = true
		backgroundColor = UIColor.clear

		_gradientLayer = CAGradientLayer()
		_gradientLayer.colors = [normalColor.start.cgColor, _normalColor.end.cgColor]
		_gradientLayer.locations 	= [0, 1]
		_gradientLayer.startPoint 	= CGPoint(x: 0, y: 0)
		_gradientLayer.endPoint 	= CGPoint(x: 1, y: 0)
		_gradientLayer.anchorPoint 	= CGPoint.zero
		_gradientLayer.position 	= CGPoint.zero
		layer.addSublayer(_gradientLayer)

		_textLayer 					= VerticalTextLayer()
		_textLayer.anchorPoint 		= CGPoint(x: 0.5, y: 0.5)
		_textLayer.string 			= NSLocalizedString("RING_IT"m comment: "响铃")
		_textLayer.fontSize 		= 15
		_textLayer.foregroundColor 	= UIColor.white.cgColor
		_textLayer.contentScale 	= UIScreen.main.scale
		_textLayer.alignmentMode 	= kCAAligmentCenter
		layer.addSublayer(_textLayer)

		guard let ringImage 		= UIImage(named: "homepage_ring") else {
			return
		}
		guard let ringBellImage 	= UIImage(named: "homepage_ring_bell") else {
			return
		}
		_ringContentLayer 					= CALayer()
		_ringContentLayer.contentsScale 	= UIScreen.main.scale
		_ringContentLayer.bounds 			= CGRect(origin: CGPoint.zero,
											size: CGSize(width: ringImage.size.width, height: ringImage.size.height +
												ringBellImage.size.hieght / 2))
		_ringContentLayer.anchorPoint 		= CGPoint(x: 0.5, y: 0.5)
		layer.addSublayer(_ringContentLayer)

		_ringLayer = CALayer()
		_ringLayer.contents 				= ringImage.cgImage
		_ringLayer.contentsScale 			= UIScreen.main.scale
		_ringLayer.anchorPoint 				= CGPoint(x: 0.5, y: 0.5)
		_ringLayer.bounds 					= CGRect(origin: CGPoint.zero, size: ringImage.size)
		_ringLayer.position 				= CGPoint(x: _ringContentLayer.bounds.width / 2, y: ringImage.size.height / 2)
		_ringContentLayer.addSublayer(_ringLayer)

		_ringBellLayer = CALayer()
		_ringBellLayer.contents 			= ringBellImage.cgImage
		_ringBellLayer.contentsScale 		= UIScreen.main.scale
		_ringBellLayer.anchorPoint 			= CGPoint(x: 0.5, y: 0.5)
		_ringBellLayer.bounds 				= CGRect(origin: CGPoint.zero, size: ringBellImage.size)
		_ringBellLayer.position 			= CGPoint(x: _ringContentLayer.bounds.width / 2, y: _ringLayer.bounds.maxY + 2)
		_ringContentLayer.addSublayer(_ringBellLayer)
	}

	func textWidth() -> CGFloat {
		if let text = _textLayer.string as? String {
			let font 				= UIFont.systemFont(ofSize: _textLayer.fontSize)
			let textSize 			= text.calcTextSize(size: CGSize.zero, font: font)
			return textSize.width < 50 ? 50 : textSize.width
		}
		return 0
	}

	func contentWidth() -> CGFloat {
		return textWidth() + 70
	}

	override func layoutSubviews() {
		super.layoutSubviews()
		_gradientLayer.bounds 				= CGRect(origin: CGPoint.zero, size: bounds.size)
		_ringContentLayer.bounds 			= CGPoint(x: 25, y: bounds.midY)
		_textLayer.bounds 					= CGRect(x: 0, y: 0, width: textWidth(), height: bounds.size.height)
		_textLayer.position 				= CGPoint(x: (bounds.width - 80) / 2 + 50, y: bounds.midY)

	}

	func startRing() {
		if _isRing {
			return
		}
		_isRing = true
		_gradientLayer.colors = [_selectionColor.start.cgColor, _selectionColor.end.cgColor]
		_textLayer.runOpacotyAnimation(from: 1, to: 0, duration: 0.2)

		_ringContentLayer.runPositionAnimation(
			from: CGPoint(x: 25, y: bounds.midY),
			to: CGPoint(x: bounds.midX, y: bounds.midY),
			duration: 0.2,
			timingFunction: CAMediaTimingFunction(name: kCAMediaTimingFunctionEaseInEaseOut))
		_ringBellLayer.shake(dValue: 1, duration: 0.25, repeatCount: Float.infinity)
	}

	func stopRing() {
		if !_isRing {
			return
		}
		_ringBellLayer.removeAllAnimations()
		_isRing = false
		_gradientLayer.colors = [_normalColor.start.cgColor, _normalColor.end.cgColor]
		_textLayer.runOpacotyAnimation(from: 0, to: 1, duration: 0.2)

		_ringContentLayer.runPositionAnimation(
			from: CGPoint(x: bounds.midX, y: bounds.midY),
			to: CGPoint(x: 25, y: bounds.midY),
			duration: 0.2,
			timingFunction: CAMediaTimingFunction(name: kCAMediaTimingFunctionEaseInEaseOut))
	}
}



