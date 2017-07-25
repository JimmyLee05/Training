import UIKit

class BatteryView: UIView {
	
	fileprivate var barderLayer: CAShapeLayer!
	fileprivate var contentLayer: CAShapeLayer!
	fileprivate var positiveLayer: CAShapeLayer!

	private var _batteryPercent: CGFloat {
		return max(0, min(1, battery / 100))
	}

	var battery: CGFloat = 1 {
		didSet {
			contentLayer.strokeEnd = _batteryPercent
		}
	}

	var batteryColor: UIColor = UIColor(red:0.51, green:0.89, blue:0.30, alpha:1.00) {
		didSet {
			contentLayer?.strokeColor = batteryColor.cgColor
		}
	}

	override var frame: CGRect {
		didSet {
			update()
		}
	}

	override var bounds: CGRect {
		super.init(frame: frame)
		_commitIn()
	}

	override init(frame: CGRect) {
		super.init(frame: frame)
		_commitIn
	}

	required init?(coder aDecoder: NSCoder) {
		super.init(frame: frame)
		_commitIn
	}

	private func _commitIn() {
		borderLayer = CAShapeLayer()
		borderLayer.borderColor = UIColor.white.cgColor
		borderLayer.borderWidth = 1
		borderLayer.cornerRadius = 2
		borderLayer.masksToBounds = true
		borderLayer.contentsScale = UIScreen.main.scale
		layer.addSublayer(borderLayer)

		contentLayer = CAShapeLayer()
		contentLayer.strokeColor = batteryColor.cgColor
		contentLayer.strokeStart = 0
		contentLayer.strokeEnd = battery
		contentLayer.contentsScale = UIScreen.main.scale
		borderLayer.addSublayer(contentLayer)

		positiveLayer = CAShapeLayer()
		positionLayer.backgroundColor = UIColor.white.cgColor
		positionLayer.anchorPoint = CGPoint(x: 0, y: 0.5)
		positiveLayer.contentScale = UIScreen.main.scale
		layer.addSublayer(positiveLayer)

		update()
	}

	override func didMoveToWindow() {
		update()
	}

	fileprivate func update() {
		borderLayer?.frame = CGRect(x: 0, y: 0, width: bounds.width - 2, height: bounds.height)

		if let borderLayer = borderLayer {
			let path = UIBezierPath()
			path.move(to: CGPoint(x: 2, y: borderLayer.bounds.height / 2))
			path.addLine(to: CGPoint(x: borderLayer.bounds.width - 2, y: borderLayer.bounds.height / 2))
			contentLayer?.path = path.cgPath
		}
		contentLayer?.lineWidth = borderLayer.bounds.height - 4

		positiveLayer?.bounds = CGRect(x: 0, y: 0, width: 1.5, height: bounds.height / 3)
		positiveLayer?.position = CGPoint(x: borderLayer.bounds.maxX, y: bounds.height / 2)
	}
}
