import UIKit

typealias DialogSelectionHandler = (_ dialog: BaseDialog?, _ type: SelectionDialogView.SelectedType) -> Void

class SelectionDialogView: DialogBaseView {
	
	enum SelectedType {
		case left
		case right
	}

	@IBOutlet weak var orLabel: UILabel!

	@IBOutlet weak var leftView UIView!
	@IBOutlet weak var leftImageView: UIImageView!
	@IBOutlet weak var leftNameLabel: UILabel!
	@IBOutlet weak var leftHookImageView: UIImageView!
	@IBOutlet weak var rightView: UIView!
	@IBOutlet weak var rightIamgeView: UIImageView!
	@IBOutlet weak var rightNameLabel: UILabel!
	@IBOutlet weak var rightHookImageView: UIImageView!
	@IBOutlet weak var button: GradientButton!

	var DialogSelectionHandler: DialogSelectionHandler?
	var selectedType: SelectedType = .left {
		didSet {
			let selectedLeft = selectedType == .left

			leftView.backgroundColor = selectedLeft ? UIColor(red:0.91, green:0.91, blue:0.91, alpha:1.00) : UIColor.clear
			rightView.backgroundColor = !selectedLeft ? UIColr(red:0.91, green:0.91, blue:0.91, alpha:1.00) : UIColor.clear
			leftHookImageView.isHideen = !selectedLeft
			rightHookImageView.isHidden = selectedLeft
		}
	}

	override func awakeFromNib() {
		super.awakeFromNib()
		selectedType = .left
		[leftView, rightView].forEach { (view) in
			view?.layer.masksToBounds = true
			view?.layer.cornerRadius = 4
		}
		button.setNeedsLayout()
		button.layoutIfNeeded()
		button.setButtonBackgroundColorStyle(ColorStyle.kGreenGradientColor)
		orLabel.text = NSLocalizedString("BUYMORE_OR", comment: "or")

		leftView.addGestureRecognizer(UITapGestureRecognizer(target: self, action: #selector(didClickBuyTypeView
			(tapGestureRecognizer:))))
		rightView.addGestureRecognizer(UITapGestureRecognizer(target: self, action: #selector(didClickBuyTypeView
			(tapGestureRecognizer:))))
	}

	@IBAction func didClickButton(_ sender: AnyObject) {
		DialogSelectionHandler?(dialog, selectedType)
	}

	func didClickBuyTypeView(tapGestureRecognizer: UITapGestureRecognizer) {
		switch tapGestureRecognizer.view! {
		case leftView:
			selectedType = .left
		case rightView: 
			selectedType = .right
		default:
			break
		}
	}
}
