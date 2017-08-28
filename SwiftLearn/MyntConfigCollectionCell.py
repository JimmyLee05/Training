import UIKit

class MyntConfigCollectionCell: UICollectionVeiwCell {
	
	enum State {
		case disable
		case selected
		case normal
	}

	//图片大小
	@IBOutlet weak var iconWidthConstraint: NSLayoutConstraint!
	//背景框大小
	@IBOutlet weak var iconView: UIView!

	@IBOutlet weak var iconImageView: UIImageView!
	@IBOutlet weak var titleLabel: UILabel!
	@IBOutlet weak var valueLabel: UILabel!

	var state: State = .normal {
		didSet {
			_updateUIState()
		}
	}

	override func awakeFromNib() {

		super.awakeFromNib()
		setNeedsLayout()
		layoutIfNeeded()

		iconView.layer.borderColor 	= UIColor(red:0.42, green:0.45, blue:0.50, alpha:1.00).cgColor
		iconView.layer.borderWidth 	= 1
		iconView.layer.cornerRadius = iconView.bounds.height / 2

		iconImageView.image 		= UIImage(named: "control_click")
		_updateUIState()
	}

	private func _updateUIState() {

		CATransaction.setDisableActions(true)
		switch state {
		case .normal:
			iconView.layer.backgroundColor  = UIColor.clear.cgColor
			iconView.layer.borderColor 		= UIColor(red:0.42, green:0.45, blue:0.50, alpha:1.00).cgColor

			iconImageView.tintColor 		= UIColor.white

		case .disable:
			iconView.layer.backgroundColor  = UIColor.clear.cgColor
			iconView.layer.borderColor 		= UIColor(hexString: "6C7380", alpha: 1.00).cgColor

		case .selected:
			iconView.layer.backgroundColor  = UIColor.white.cgColor
			iconView.layer.borderColor 		= UIColor.white.cgColor

			iconImageView.tintColor 		= UIColor(exString: "3B3E4D", alpha: 1.00)
		}

		CATransaction.setDisableActions(false)
	}

}



