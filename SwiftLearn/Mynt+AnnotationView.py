import Foundation

extension UIView {
	
	func showNavigationView(mapMynt: MapMynt, clickHandler: @escaping (MapMynt) -> Void) {
		let width: CGFloat 	= 100
		let height: CGFloat	= 40
		let view = NavigationView(frame: CGRect(x: bounds.width / 2 - width / 2, y: -height - 5, width: width,
			height: height))
		view.clickHandler = {
			clickHandler(mapMynt)
		}
		self.addSubview(view)
	}

	func showMapMyntCollectionView(mapMynts: [MapMynt]) {
		let count = mapMynts.count
		let row   = (count - 1) / 3 + 1
		let widthCount 	= CGFloat(min(count, 3))
		let heightCount = CGFloat(min(Double(row), 2.5))
		let width = widthCount * Mynt.annotationWidth + (widthCount + 1) * 15
		let height = heightCount * Mynt.annotationWidth + (heightCount + 1) * 15

		let view = MapMyntCollectionView(frame: CGRect(x: bounds.width / 2 - width / 2, y: height / 2, width: width,
			heightL height))
		view.mapMynts = mapMynts
		self.addSubview(view)
	}
}

extension Mynt {
	
	static var annotationWidth: CGFloat { return 60 }
	static var annotationHeight: CGFloat { return 68 }

	//绘制地图的图标
	func annotationImage(count: Int = 1, showOffline: Bool = true, block: @escaping (UIImage?) -> Void) {
		let width  = Mynt.annotationWidth
		let height = Mynt.annotationHeight
		let sn = self.sn
		loadAvatar { image in
			guard let mynt = sn.mynt else { return }
			let showOfflineLayer = mynt.uiState != .online && showOffline
			let showOwnerLayer = mynt.isOwner == false
			DispatchQueue.global().async {
				UIGraphicsBeginImageContextWithOptions(CGSize(width: width, height: height), false, UIScreen.main.scale)
				let context = UIGraphicsGetCurrentContext()

				//绘制外圈圆
				var path = UIBezierPath(arcCenter: CGPoint(x: width / 2, y: width / 2), radius: width / 2,
					startAngle: 0, endAngle: 180, clockwise: true)
				context?.addPath(path.cgPath)
				context?.setFillColor(UIColor.white.cgColor)
				context?.drawPath(using: .fill)
				//绘制底部肩头
				path = UIBezierPath()
				path.move(to: CGPoint(x: 15, y: height - 15))
				path.addLine(to: CGPoint(x: 45, y: height - 15))
				path.addLine(to: CGPoint(x: width / 2, y: height))
				path.close()
				context?.addPath(path.cgPath)
				context?.setFillColor(UIColor.white.cgColor)
				context?.drawPath(using: .fill)

				//绘制图形
				image?.draw(in: CGRect(x: 2, y: 2, width: width - 4, height: width - 4))

				if showOfflineLayer {
					//绘制蒙版
					path = UIBezierPath(arcCenter: CGPoint(x: width / 2, y: width / 2), radius: width / 2 - 2,
						startAngle: 0, endAngle: 180, clockwise: true)
					context?.addPath(path.cgPath)
					context?.set
				}
			}}
	}
}



























