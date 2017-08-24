import UIKit

class Toast: UIView {
	
	@IBOutlet weak var titleBottomConstrint: NSLayoutConstraint!

	@IBOutlet weak var contentView: UIView!

	@IBOutlet weak var titleLabel: UILabel!

	@IBOutlet weak var messageLabel: UILabel!

	override func awakeFromNib() {

		contentView.layer.cornerRadius = 5
	}

	class func show(title: String? = nil, message: String?) {
		let toast = Toast.createFromXib() as? Toast
		toast?.show(title: title, message: message)
	}

	func show(title: String? = nil, message: String?) {

		if title == nil {
			titleBottomConstrint.constant = 0
		}
		titleLabel.text = title
		messageLabel.text = message

		translatesAutoresizingMaskIntoConstraints = false
		UIApplication.shared.keyWindow?.addSubview(self)
		fillInSuperView()

		perform(#selector(dismiss), with: self, afterDelay: 1.5)
		contentView.layer.runOpacotyAnimation(from: 0, to: 0.95, duration: 0.15)
	}

	func dismiss() {
		contentView.layer.runOpacotyAnimation(from: 0.95, to: 0, duration: 0.15)
		perform(#selector(removeFromSuperview), with: self, afterDelay: 0.15)
	}
}


