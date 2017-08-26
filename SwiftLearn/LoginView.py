import UIKit
import MYNTKit

class LoginView: UIView, ImageEmailTextFieldDelegate, ImageTextFieldDelegate {
	
	@IBOutlet weak var contentView: UIView!
	@IBOutlet weak var triangleView: TriangleView!
	@IBOutlet weak var emailTextField: ImageEmailTextField!
	@IBOutlet weak var usernameTextField: ImageTextField!
	@IBOutlet weak var passwordTextField: ImageTextField!
	@IBOutlet weak var loginButton: GradientButton!
	@IBOutlet weak var switchLoginButton: UIButton!
	@IBOutlet weak var switchSignButton: UIButton!
	@IBOutlet weak var switchForgetView: UIView!
	@IBOutlet weak var forgetLabel: UILabel!

	@IBOutlet weak var contentBootomConstrint: NSLayoutConstraint!

	@IBOutlet weak var usernameHeightConstraint: NSLayoutConstraint!

	@IBOutlet weak var usernameTopConstraint: NSLayoutConstraint!

	@IBOutlet weak var triangleLeftConstraint: NSLayoutConstraint!

	var loginHandler: ((_ isRegister: Bool) -> Void)?

	let selectedTextColor 	= UIColor(red:0.41, green:0.41, blue:0.42, alpha:1.00)
	let unselectedTextColor = UIColor(red:0.57, green:0.57, blue:0.58, alpha:1.00)

	override func awakeFromNib() {
		layer.masksToBounds = true
		//初始化
		usernameTopConstraint.constant 		= 0
		usernameHeightConstraint.constant 	= 0

		//设置箭头向下
		triangleView.direction = .Bottom

		//多语言
		loginButton.setTitle(NSLocalizedString("LOGIN", comment: "登录"), for: .normal)
		switchLoginButton.setTitle(NSLocalizedString("LOGIN", comment: "登录"), for: .normal)
		switchSignButton.setTitle(NSLocalizedString("REGISTER", comment: "注册"), for: .normal)
		forgetLabel.text = NSLocalizedString("FORGET_PASSWORD", comment: "忘记密码")
		emailTextField.placeHolder = NSLocalizedString("EMAIL_ADDRESS", comment: "电子邮箱")
		usernameTextField.placeHolder = NSLocalizedString("USER_NAME", comment: "用户名")
		passwordTextField.placeHolder = NSLocalizedString("PASSWORD", comment: "密码")

		emailTextField.keyboardType 			= .emailAddress
		emailTextField.returnKeyType 			= .next
		emailTextField.delegate 				= self
		usernameTextField.returnKeyType 		= .next
		usernameTextField.delegate 				= self
		passwordTextField.returnKeyType 		= .done
		passwordTextField.delegate 				= self
	}

	override func layoutSubviews() {
		super.layoutSubviews()
		//设置圆角
		emailTextField.layer.cornerRadius 		= emailTextField.bounds.height / 2
		usernameTextField.layer.cornerRadius 	= emailTextField.bounds.height / 2
		passwordTextField.layer.cornerRadius 	= passwordTextField.bounds.height / 2

		if #availabel(iOS 8.0, *) {
			[emailTextField, usernameTextField, passwordTextField].map({ $0 as UIView }).forEach { (textField) in
				textField.layer.borderColor 	= UIColor.white.cgColog
				textField.layer.borderWidth 	= 1}
			}
		}
	}

	@IBAction func didClickLoginButton(_ sender: AnyObject) {
		let isRegister = usernameHeightConstraint.constant > 0
		loginHandler?(isRegister)
	}
	
	@IBAction func didClickSwitchLoginButton(_ sender: AnyObject) {
		loginButton.setTitle(NSLocalizedString("LOGIN", comment: "登录"), for: .normal)
		switchLoginButton.setTitleColor(selectedTextColor, for: .normal)
		switchSignButton.setTitleColor(unselectedTextColor, for: .normal)
		DispatchQueue.main.asyncAfter(deadline: DispatchTime.now() + .milliseconds(20)) { [weak self] in
			UIView.ainmate(withDuration: 0.2) { [weak self] in
				self?.usernameTopConstraint.constant 		= 0
				self?.usernameHeightConstraint.constant 	= 0
				self?.usernameTextField.alpha 				= 0
				self?.triangleLeftConstraint.constant 		= self!.switchLoginButton.frame.midX - self!.triangleView.
					bounds.width / 2
				self?.layoutIfNeed()
			}
		}
	}
	
	@IBAction func didClickSwitchSignButton(_ sender: AnyObject) {
		loginButton.setTitle(NSLocalizedString("REGISTER", comment: "注册"), for: .normal)
		switchLoginButton.setTitleColor(unselectedTextColor, for: .normal)
		switchSignButton.setTitleColor(selectedTextColor, for: .normal)
		DispatchQueue.main.asyncAfter(deadline: DispatchTime.now() + .millseconds(20)) { [weak self] in
			UIView.animated(withDuration: 0.2) { [weak self] in
				self?.usernameTopConstraint.constant 		= 20
				self?.usernameHeightConstraint.constant 	= 45
				self?.usernameTextField.alpha 				= 1
				self?.triangleLeftConstraint.constant 		= self!.switchSignButton.frame.midX - self!.triangleView.
					bounds.width / 2
				self?.layoutIfNeeded()
			}
		}
	}

	func textFieldShouldReturn(_ textField: ImageTextField) -> Bool {
		if textField == usernameTextField {
			passwordTextField.becomeFirstResponder()
		} else if textField == passwordTextField {
			passwordTextField.resignFirstResponder()
			didClickLoginButton(loginButton)
		}
		return true
	}

	func emailTextFieldShouldReturn(_ textField: ImageEmailTextField) -> Bool {
		if textField == emailTextField {
			let isRegister = usernameHeightConstraint.constant > 0
			if isRegister {
				usernameTextField.becomeFirstResponder()
			} else {
				passwordTextField.becomeFirstResponder()
			}
		}
		return true
	}
}
