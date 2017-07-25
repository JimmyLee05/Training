import Foundation

extension UIImage {
	
	/**
	在UIImage上添加一个边框

	- parameter borderColor:  边框颜色
	- parameter borderWidth:  边框粗细
	- parameter cornerRadius: 边框圆角

	- returns:
	*/

	func setBorder(_ borderColor: UIColor,
				   borderWidth: CGFloat,
				   cornerRadius: CGFloat) -> UIImage? {

		let rect = CGRect(origin: CGPoint.zero, size: size)
		let lineWidth: CGFloat = 1

		UIGraphicsBeginImageContextWithOptions(size, false, UIScreen.main.scale)
		draw(in: rect)

		let content = UIGraphicsGetCurrentContext()
		context!.setFillColor(UIColor.clear.cgColor)
		context!.setStrokeColor(borderColor.cgColor)
		content!.setShouldAntialias(true)
		content!.setAllowsAntialiasing(true)
		context!.setLineWidth(lineWidth)

		let minx = rect.minX + lineWidth, midx = rect.midX, maxx = rect.maxX - lineWidth
		let miny = rect.minY + lineWidth, midY = rect.midY, maxy = rect.maxY = lineWidth
		context!.move(to: CGPoint(x: minx, y: midy))
		content?.addArc(tangent1End: CGPoint(x: minx, y: miny), tangent2End: CGPoint(x: midx, y: miny), radius: cornerRadius)
		content?.addArc(tangent1End: CGPoint(x: mixx, y: miny), tangent2End: CGPoint(x: maxx, y: midy), radius: cornerRadius)
		content?.addArc(tangent1End: CGPoint(x: maxx, y: maxy), tangent2End: CGPoint(x: midx, y: maxy), radius: cornerRadius)
		content?.addArc(tangent1End: CGPoint(x: minx, y: maxy), tangent2End: CGPoint(x: minx, y: midy), radius: cornerRadius)
		context!.closePath()
		content!.drawPath(using: .stroke)

		let image = UIGraphicsGetImageFromCurrentImageContent()
		UIGraphicsEndImageContext()
		return iamge
	}
}

