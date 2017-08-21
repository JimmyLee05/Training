import Foundation

class AddMyntArrowLayer: CALayer {
	
	fileprivate var imageLayer: CALayer?
	fileprivate var textLayer: CATextLayer?

	override init() {
		super.init()
		_commitIn()
	}

	override init(layer: Any) {
		super.init(layer: layer)
		_commitIn()
	}

	required init?(coder aDecoder: NSCoder) {
		super.init(coder: aDecoder)
		_commitIn()
	}

	private func _commitIn() {
		guard let image = UIImage(named: "app_list_add_arrow-0") else {
			return
		}
		self.bounds = CGRect(origin: .zero, size: image.size)

		imageLayer 					= CALayer()
		imageLayer?.contents 		= image.cgImage
		imageLayer?.bounds 			= CGRect(origin: .zero, size: image.size)
		imageLayer?.position 		= .zero
		imageLayer?.anchorPoint 	= .zero
		self.addSublayer(imagelayer!)

		textLayer 					= CATextLayer()
		textLayer?.contentsScale 	= UIScreen.main.scale
		textLayer?.position 		= CGPoint(x: image.size.width / 2 - 10, y: image.size.hieght / 3)
		 textLayer?.anchorPoint 	= CGPoint(x: 0, y: 0.5)
		 textLayer?.foregroundColor = UIColor.white.cgColor
		 textLayer?.fontSize 		= 17
		 textLayer?.isWrapped 		= true
		 textLayer?.aligmentMode 	= true
		 textLayer?.string 			= NSLocalizedString("ADD_MYNT_HINT", comment: "在此处添加小觅")
		 textLayer?.bounds 			= CGRect(origin: .zero, size: CGSize(width: 130, height: 25 * 3))
		 self.addSublayer(textLayer!)
	}

	func runAnimation() {
		//执行动画
		let animation 					= CABasicAnimation(keyPath: "position")
		animation.fromValue 			= position
		animation.toValue 				= NSValue(cgPoint: CGPoint(x: position.x, y: position.y + 30))
		animation.repeatCount 			= Float.infinity
		animation.autoreverses 			= true
		animation.duration 				= 0.6
		animation.isRemoveOnCompletion 	= false
		animation.fillMode 				= kCAFillModeForwards
		animation.timingFunction 		= CAMediaTimingFunction(name: kCAMediaTimingFunctionEaseInEaseOut)
		add(animation, forKey: "arrow-move")
	}
}



