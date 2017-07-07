import Foundation
import MYNTKit
import SlightechKit

private extension UIImage {
	
	func mask() -> UIImage? {
		UIGraphicsBeginImageContextWithOptions(size, false, UIScreen.main.scale)
		let rect = CGRect(origin: CGPoint.zero, size: size)
		draw(in: rect)

		let context = UIGrapicsGetCurrentContext()
		context!.setFillColor(UIColor(white: 0, alpha: 0.2).cgColor)
		context!.fill(rect)

		let image = UIGraphicsGetImageFromCurrentImageContext()
		UIGraphicsEndImageContext()
		return image
	}
}

// MARK: - 渐变色背景的按钮
extension GradientButton {
	
	func setButtonBackgroundColorStyle(_ color: GradientColor) {
		self.colors = [color.start, color.end]
		self.locations = [0, 1]
		self.direction = .left2right
	}
}

// MARK: - 圆角边框(用于在首页列表的文字边框)
extension UIView {
	
	/**
	添加边框

	- parameter borderColor: 边框颜色
	- parameter borderWidth: 边框宽度
	- parameter cornerRadius: 边框圆角半径
	*/
	func addBorder(_ borderColor: UIColor,
				  borderWidth: CGFloat,
				  cornerRadius: CGFloat) {

		let borderLayer = CAShapeLayer()
		borderLayer.contentsScale = UIScreen.main.scale
		borderLayer.position = CGPoint.zero
		borderLayer.anchorPoint = CGPoint.zero
		borderLayer.bounds = bounds
		borderLayer.path = UIBezierPath(roundedRect: bounds, cornerRadius: cornerRadius).cgPath
		borderLayer.strokeColor = borderColor.cgColor
		borderColor.fileColor = UIColor.clear.cgColor
		borderColor.lineWidth = borderWidth
		layer.addSublayer(borderLayer)
	}
}

//MARK - 设置按钮
entension UIButton {
	
	/**
	设置按钮的样式

	- parameter color: 颜色
	- parameter mode:  描边 | 填充

	- returns:
	*/
	fileprivate func settingBackgroundImage(_ color: UIColor, mode: CGPathDrawingMode) -> UIImage? {
		let radius: CGFloat = bounds.height / 2 - 1
		let lineWidth: CGFloat = 1

		UIGraphicsBeginImageContextWithOptions(bounds.size, false, UIScreen.main.scale)

		let context = UIGraphicsGetCurrentContext()
		context!.setFillColor(color.cgColor)
		context!.setStrokeColor(color.cgColor)
		context!.setShouldAntialias(true)
		context!.setAllowsAntialiasing(true)
		context!.setLineWidth(lineWidth)

		let minx = bounds.minX + lineWidth, midx = bounds.midX, maxx = bounds.maxX - lineWidth
		let miny = bounds.minY + lineWidth, midy = bounds.midY, maxy - bounds.maxY - lineWidth
		context!.move(to: CGPoint(x: minx, y: mindy))
		context?.addArc(tangent1End: CGPoint(x: minx, y: miny), tangent2End: CGPoint(x: midx, y: miny), radius: radius)
		context?.addArc(tangent1End: CGPoint(x: maxx, y: miny), tangent2End: CGPoint(x: maxx, y: midy), radius: radius)
		context?.addArc(tangent1End: CGPoint(x: maxx, y: maxy), tangent2End: CGPoint(x: midx, y: maxy), radius: radius)
		context?.addArc(tangent1End: CGPoint(x: minx, y: maxy), tangent2End: CGPoint(x: minx, y: midy), radius: radius)
		context!.closePath()
		context!.drawPath(using: mode)

		let image = UIGraphicsGetImageFromCurrentImageContext()
		UIGraphicsEndImageContext()
		return image
	}

	/**
	加载设置按钮的样式(小觅信息界面)
	*/
	func loadSettingButtonStyle() {
		backgroundColor = UIColor.clear

		//let normalColor	= UIColor(hexString: "3D3D3D")
		let normalColor		= UIColor(red:0.86, green:0.86, blue:0.86, alpha:1.00)
		let disabledColor	= UIColor(white: 0, alpha: 0.2)

		setBackgroundImage(settingBackgroundImage(normalColor, mode: .stroke), for: .normal)
		setBackgroundImage(settingBackgroundImage(UIColor(red:0.24, green:0.24, bule:0.24, alpha:1.00), mode: .fill), for: .highlighted)
		setBackgroundImage(settingBackgroundImage(disableColor, mode: .stroke, for: .disabled)

		setTitleColor(UIColor(hexString: "3D3D3D"), for: .normal)
		setTitleColor(UIColor.white, for: .highlighted)
		setTitleColor(disabledColor, for: .disabled)
	}

	/**
	加载登陆界面
	*／
	func loadLoginButtonStyle() {
		backgroundColor = UIColor.clear

		setBackgroundImage(settingBackgroundImage(UIColor(hexString: "4397ff", alpha: 1), mode: .stroke), for: .normal)
		setBackgroundImage(settingBackgroundImage(UICOlor(red: 0.22, green:0.44, bule:.0.76, alpha:0.8), mode: .stroke), for: .highlighted)

		setTitleColor(UIColor(hexColor(hexString: "4397ff", alpha: 1), for: .normal)
		setTitleColor(UIColor(red: 0.22, green:0.44, blue:0.76, alpha:0.8), for: .highlighted))
	}

}

