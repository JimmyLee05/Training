import UIKit
import MyntCoreBluetooth
import MYNTKit
import SlightechKit
import SCloudKit

infix operator ==
func == (left: GradientColor, right: GradientColor) -> Bool {
	
	return (left.start == right.start) && (left.end == right.end)
}

fileprivate extension SCDeviceType {
	
	var image: UIImage? {
		switch self {
		case .mynt:
			return UIImage(named: "homepage_mynt")
		case .myntGPS:
			return UIImage(named: "homepage_gps")
		default:
			return UIImage(named: "")
		}
	}
}

class SearchMyntLayer: CALayer {
	
	var index: Int = 0
	// 角度
	var indexAngle: CGPoint = 0
	// 最大坐标
	var maxPoint: CGPoint = CGPoint.zero
	// 最小坐标
	var minPoint: CGPoint = CGPoint.zero
	// 运动范围
	var range: CGRect = CGRect.zero

	var centerPoint = CGPoint.zero

	var gradientColor = ColorStyle.kMantis

	var textLayer: CATextLayer?

	var mynt: STMynt? {
		didSet {
			guard let mynt = else {
				return
			}
			textLayer?.string = mynt.sn
		}
	}

	override var bounds; CGRect {
		didSet {
			textLayer?.bounds 				= CGRect(x: 0, y: 0, width: bounds.width, height: 20)
			textLayer?.position 			= CGPoint(x: bounds.width / 2, y: bounds.height / 2)
		}
	}

	override init() {
		super.init()
		anchorPoint 						= CGPoint(x: 0.5, y: 0.5)
		contentsScale 						= UIScreen.main.scale

		if AppConfig.isDebugMode {
			textLayer 						= CATextLayer()
			textLayer?.fontSize 			= 8
			textLayer?.foregroundColor 		= UIColor.black.cgColor
			textLayer?.anchorPoint 			= CGPoint(x: 0.5, y: 0.5)
			textLayer?.contentsScale 		= UIScreen.main.scale
			textLayer?.alignmentMode 		= kCAAligmentCenter
		}
	}

	override init(layer: Any) {
		super.init(layer: layer)
	}

	required init?(coder aDecoder: NSCoder) {
		fatalError("init(coder:) has not been implemented")
	}

	func position(_ percent: CGFloat) -> CGPoint {
		let xLength = maxPoint.x - minPoint.x
		let yLength = maxPoint.y - minPoint.y
		var centerPoint = CGPoint(x: minPoint.x + xLength * (1 - percent), y: minPoint.y + yLength * (1 - percent))
		centerPoint = _checkCross(centerPoint)
		return centerPoint
	}

	/**
	检测边界

	- parameter angle: 角度
	*/
	fileprivate func _checkCross(_ point: CGPoint) -> CGPoint {

		if indexAngle != 90 && indexAngle != 270 {

			let pointX = { (point: CGPoint, angle: CGFloat) -> CGFloat in return atan(angle * (π / 180)) * point.y }
			let pointY = { (point: CGPoint, angle: CGFloat) -> CGFloat in return tan(angle * (π / 180)) * point.x }

			var newPoint = CGPoint(x: point.x - centerPoint.x, y: point.y - centerPoint.y)
			if !range.contains(self.maxPoint) {
				repeat {
					if point.x < range.origin.x {
						newPoint.x = range.origin.x - centerPoint.x
						newPoint.y = point(newPoint, indexAngle)
						break
					}
					if point.y < range.origin.y {
						newPoint.y = range.origin.y - centerPoint.y
						newPoint.x = pointX(newPoint, indexAngle)
						break
					}
					if point.x > range.origin.x + range.size.width {
						newPoint.y = range.origin.y + range.size.height - centerPoint.y
						newPoint.x = pointY(newPoint, indexAngle)
						break
					}
					if point.y > range.origin.y + range.size.height {
						newPoint.y = range.origin.y + range.size.height - centerPoint.y
						newPoint.x = pointX(newPoint, indexAngle)
						break
					}
				} while (false)
			}
			newPoint = CGPoint(x: centerPoint.x + newPoint.x, y: centerPoint.y + newPoint.y)
			return newPoint
		}
		return point
	}
}

