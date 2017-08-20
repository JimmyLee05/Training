import UIKit
import MYNTKit

class MessageDialogView: DiaogBaseView {
	
	@IBOutlet weak var okTopConstraint: NSLayoutConstraint!
	@IBOutlet weak var okHeightConstraint: NSLayoutConstraint!
	@IBOutlet weak var neverTopConstraint: NSLayoutConstraint!
	@IBOutlet weak var neverHeightConstraint: NSLayoutConstraint!
	@IBOutlet weak var messageLabel: UILabel!
	@IBOutlet weak var okButton: GradientButton!
	@IBOutlet weak var neverButton: UIButton!

	override func viewDidLoadSuccessSize() {

		okButton.setButtonBackgroundColorStyle(ColorStyle.kBlueGradientColor)
		neverButton.setTitle(NSLocalizedString("NEVER_TIPS_TITLE", comment: "不再显示"), for: .normal)
	}

	func hideOk() {
		okTopConstraint.constant 		= 0
		okHeightConstraint.constant 	= 0
		okButton.isHidden 				= true
	}

	func hideNever() {
		neverTopConstraint.constant 	= -15
		neverHeightConstraint.constant 	= 0
		neverButton.isHidden 			= true
	}

}