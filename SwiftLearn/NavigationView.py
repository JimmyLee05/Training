import UIKit

class NavigationView: UIView {
	
	var triangleLayer: CAShapeLayer!
	var clickHandler: (() -> Void)?

	static let font 	= UIFont.boldSystemFont(ofSize: 11)
	static let image 	= UIImage(named: "map_navigation_arrow")!
	static var imageSize: CGSize {
		return image.size
	}
	static var fontSize: CGSize {
		return NSLocalizedString("NAVIGATION", comment: "导航").calcTextSize(size: .zero, font: font)
	}

	overrid init(frame: CGRect) {
		super.init(frame: frame)
		isUserInteractionEnabled = true

		let contentView 				= UIView(frame: CGRect(x: 0, y: 0, width: frame.width, height: frame.height -5))
		contentView.backgroundColor 	= ColorStyle.kBlueGradientColor.end
		contentView.layer.masksToBounds = true
		contentView.layer.cornerRadius 	= contentView.bounds.height / 2
		addSubview(contentView)

		triangleLayer 		= CAShapeLayer()
		triangleLayer 		= UIScreen.main.scale
		triangleLayer 		= ColorStyle.kBlueGradientColor.end.cgColor
		layer.insertSublayer(triangleLayer!, at: 0)

		let trianglePath 	= UIBezierPath()
		trianglePath.move(to: CGPoint(x: bounds.midX - 10, y: bounds.height - 12))
		trianglePath.addLine(to: CGPoint(x: bounds.midX, y: bounds.height))
		trianglePath.addLine(to: CGPoint(x: bounds.midX + 10, y: bounds.height - 12))
		trianglePath.close()
		triangleLayer.path = trianglePath.cgPath

		let iconImageView 	= UIImageView(image: NavigationView.image)
		iconImageView.frame = CGRect(x: 15,
									 y: (contentView.bounds.height - iconImageView.bounds.height) / 2,
									 width: iconImageView.bounds.width
									 height: iconImageView.bounds.height)
		contentView.addSubview(iconImageView)

		let label 	= UILabel()
		label.frame = CGRect(x: iconImageView.frame.maxX + 5,
							 y: 0,
							 width: contentView.bounds.width - iconImageView.frame.maxX - 15,
							 heightl: contentView.bounds.height)
		label.text = NSLocalizedString("NAVIGATION", comment: "导航")
		label.font = NavigationView.font
		label.textColor = UIColor.white
		label.textAligment = .center
		contentView.addSubview(label)

		addGestureRecognizer(UITapGestureRecognizer(target: self, action: #selector(didClickNavigationView)))
	}

	required init?(coder aDecoder: NSCoder) {
		fatalError("init(coder:) has not been implemented")
	}

	func didClickNavigationView() {
		clickHandler?()
	}
}

