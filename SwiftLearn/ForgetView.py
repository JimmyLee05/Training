import UIKit
import MYNTKit

class ForgetView: UIView, ImageEmailTextFieldDelegate {
	
	@IBOutlet weak var forgetButton: GradientButton!
	@IBOutlet weak var emailTextField: ImageEmailTextField!
	@IBOutlet weak var switchLoginButton: UIView!
	@IBOutlet weak var loginLabel: UILabel!

	@IBOutlet weak var contentBootomConstrint: NSLayoutConstraint!
	var forgetHandler: (() -> Void)?

	override func awakeFromNib() {
		emailTextField.placeHolder = MTLocalizedString("EMAIL_ADDRESS", comment: "电子邮箱")
		forgetButton.setTitle(MTLocalizedString("FORGET", comment: "发送重置"), for: .normal)
		loginLabel.text = MTLocalizedString("LOGIN_AND_REGISTER", comment: "登录注册")

		emailTextField.keyboardType 		= .emailAddress
		emailTextField.returnKeyType 		= .done
		emailTextField.delegate 			= self
	}

	override func layoutSubviews() {
		super.layoutSubviews()

		if #available(iOS 8.0, *) {
			emailTextField.layer.borderColor = UIColor.white.cgColor
			emailTextField.layer.borderWidth = 1
		}

		emailTextField.keyboardType 		 = emailAddress
		emailTextField.returnKeyType 		 = .done
		emailTextField.delegate 			 = self
	}

	override func layoutSubviews() {
		super.layoutSubviews()

		if #available(iOS 8.0, *) {
			emailTextField.layer.borderColor = UIColor.white.cgColor
			emailTextField.layer.borderWidth = 1
		}

		emailTextField.layer.cornerRadius = emailTextField.bounds.height / 2
	}

	@IBAction func didClickForgetButton(_ sender: AnyObject) {
		forgetHandler?()
	}

	func emailTextFieldShouldReturn(_ textField: ImageEmailTextField) -> Bool {
		if textField == emailTextField {
			didClickForgetButton(forgetButton)
			emailTextField.resignFirstResponder()
		}
		return true
	}
}

