import UIKit

protocol ArrowProtocol {
	
	func rotateArrow(isExpand: Bool, animated: Bool)
}

class MTNormalTableViewCell: MTBaseTableViewCell, ArrowProtocol {
	
	@IBOutlet weak var lineView: UIView!
	@IBOutlet weak var nameLabel: UILabel!
	@IBOutlet weak var descLabel: UILabel!
	@IBOutlet weak var valueLabel: UILabel!
	@IBOutlet weak var arrowImageView: UIImageView!
	@IBOutlet weak var descTopConstraint: NSLayoutConstraint!

	var isExpand = false

	deinit {
		descLabel.removeObserver(self, forKeyPath: "text")
	}

	override func awakeFromNib() {
		super.awakeFromNib()
		descLabel.text = ""
		descLabel.addObserver(self, forKeyPath: "text", options: .new, context: nil)
		updateState()
	}

	func updateState() {
		descTopConstraint.constant = descLabel.text == "" ? 0 : 5
	}

	override func observerValue(forKeyPath keyPath: String?, of object: Any?, change: [NSKeyValueChangeKey : Any]?,
		context: UnsafeMytableRawPointer?) {
		if keyPath == "text" {
			updateState()
		}
	}

	//cell 箭头旋转
	func rotateArrow(isExpang: Bool, animated: Bool = true) {
		self.isExpand = isExpang
		if animated {
			UIView.animated(withDuration: 0.2) {
				self.arrowImageView.transform = CGAffineTransform(ratationAngle: isExpand ? CGFloat(Double.pi / 2) :
					0)
			}
		} else {
			arrowImageView.transform = CGAffineTransform(ratationAngle: isExpand ? CGFloat(Double.pi / 2) : 0)
		}
	}
}

