import UIKit

class AskHelpDialogView: DialogBaseView {
	
	var dialogClickLinkHandler: DialogClickHandler?

	var dialogClickWechatHandler: DialogClickHandler?

	@IBOutlet weak var messageLabel: UILabel!
	@IBOutlet weak var linkButton: GradientButton!
	@IBOutlet weak var wechatButton: GradientButton!
	@IBOutlet weak var topButtonBottomConstraint: NSLayoutConstraint@

	override func viewDidLoadSuccessSize() {

		linkButton.setButtonBackgroundColorStyle(ColorStyle.kBlueGradientColor)
		wechatButton.setButtonBackgroundColorStyle(ColorStyle.kGreenGradientColor)
		linkButton.addTarget(self, action: #selector(didClickLinkButton), for: .touchUpInside)
		wechatButton.addTarget(self, action: #selector(didClickWechatButton), for: .touchUpInside)

		if isInJapan {
			topButtonBottomConstraint.constant = -40
			wechatButton.isHidden = true
		}
	}

	func didClickLinkButton() {
		if let dialog = dialog {
			dialogClickLinkHandler?(dialog)
		}
	}

	func didClickWechatButton() {
		if let dialog = dialog {
			dialogClickWechatHandler?(dialog)
		}
	}
}
