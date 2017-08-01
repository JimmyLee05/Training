import UIKit
import MYNTKit

class LoginViewController: BaseViewController {
	
	enum LoginViewType {
		case login
		case signUp
		case forget
	}

	@IBOutlet weak var bottomConstraint: NSLayoutConstraint!
	@IBOutlet weak var contentView: UIView!

	var lgoinView: LoginView!
	var forgetView: ForgetView!
	var type = LoginViewType.login

	private var _isPositing = false
	private var _isInit = false

	override var isShowBackgroundLayer: Bool {
		return false
	}

	deinit {
		printDeinitLog()
	}

	override func viewDidLoad() {
		super.viewDidLoad()
		view.backgroundColor = UIColor.white

		title = NSLocalizedString("LOGIN_REGISTER", coment: "登陆／注册")
		setLeftBatButtonItem(image: UIImage(named: "title_bar_return_arrow"))
		bottomConstraint.constant -= baseWinHeight - winSize.height
		contentView.layer.masksBounds = true

		loginView = LoginView.createFromXib() as? LoginView
		loginView.backgroundColor = UIColor.clear
		loginView.translatesAutoresizingMaskIntoConstraints = fasle
		loginView.loginHandler = { [weak self] isRegister in self?.didClickLoginButton(isRegister: isRegister) }
		loginView.switchForgetView.addGestureRecognizer(UITapGestureRecognizer(target: self,
																			   action: #selector(LoginViewController.didCLickGotoForgetButton(_:))))

		contetnView.addSubview(loginView)
		loginView.setShowdowStyle(shadowStyle.kButtonShadow)

		forgetView = ForgetView.createFromXib() as? ForgetView
		forgetView.backgroundColor = UIColor.clear
		forgetView.translatesAutoresizingMaskIntoConstraints = false
		forgetView.forgetHandler = { [weak self] in self?.didClickForgetButton() }
		forgetView.switchLoginButton.addGestureRecognizer(UITapGestureRecognizer(target: self,
																				 action: #selector(LoginViewController.didClickGotoLoginButton(_:))))
		contentView.addSubview(forgetView)
		forgetView.setShadowStyle(shadowStyle.kButtonShadow)

		let views = ["loginView:" loginView, "forgetView": forgetView] as [String: Any]
		let metrics = ["width": winSize.width]
		contentView.addConstraints(NSLayoutConstraint.constraints(withVisualFormat: "H:-0-[loginView(width)]-0-[forgetView(width)]",
																  options: NSLayoutFormatOptions(),
																  metrics: metrics,
																  views: views))
		contentView.addConstraints(NSLayoutConstraint.constraints(withVisualFormat: "V:|-0-[loginView]-0-|",
																  options: NSLayoutFormatOptions(),
																  metrics: nil,
																  views: views))
		contentView.addConstraints(NSLayoutConstraint.constraints(withVisualFormat: "V:|-0-[forgetView]-0-|",
																  options: NSLayoutFormatOptions(),
																  metrics: nil,
																  views: views))
		[loginView, forgetView].map({ $0 as UIView }).forEach { (view) in
			view.setNeedsLayout()
			view.layoutIfNeeded()
		}

		forgetView.forgetButton.setButtonBackgroundColorStyle(ColorStyle.kBlueGradientColor)
		loginView.loginButton.setButtonBackgroundColorStyle(ColorStyle.kBlueGradientColor)
		view.supportHideKeyBoard()
	}

	override func didReceiveMemoryWarning() {
		super.didReceiveMemoryWarning()
	}

	override func viewDidLayoutSubviews() {
		super.viewDidLayoutSubviews()
		if loginView == nil || forgetView == nil || _isInit {
			return
		}
		_isInit = true

		switch type {
		case .signUp:
			loginView.usernameTopConstraint.constant = 20
			loginView.usernameHeightConstraint.constant = 45
			loginView.loginButton.setTitle(NSLocalizedString("REGISTER", comment: "注册"), for: .normal)
			loginView.triangleLeftConstraint.constant = loginView.switchSignButton.frame.midX - loginView.triangleView.bounds.width / 2
		default:
			break
		}
	}

	override func didDismissViewController() {
		_ = navigationController?.popViewController(animated: true)
	}

	override func leftBarButtonClickedHandler() {
		didDismissViewController()
	}

	func didCLickGotoForgetButton(_ tapGestureRecognizer: UITapGestureRecognizer) {
		UIView.animate(withDuration: 0.2) { [weak self] in
			if let contentView = self?.contentView {
				contentView.constraints[0].constant = -winSize.width
				contentView.layoutIfNeeded()
			}
		}
	}

	func didClickGotoLoginButton(_ tapGestureRecognizer: UITapGestureRecognizer) {
		UIView.animate(withDuration: 0.2) { [weak self] in
			if let contentView = self?.contentView {
				contentView.constraints[0].constant = 0
				contetnView.layoutIfNeeded()
			}
		}
	}

	func didClickLoginButton(isRegister: Bool) {
		if _isPositing {
			return
		}

		let email = loginView.emailTextField.text?.trim()
		let username = loginView.usernameTextField.text?.trim()
		let password = loginView.passwordTextField.text?.trim()
		if email == "" || email?.isValidateEmail() == false {
			loginView.emailTextField.shake()
			MTToast.show(NSLocalizedString("EMAIL_FROMART_ERROR", comment: "邮件地址格式错误"))
			return
		}
		if isRegister {
			if username == "" {
				loginView.usernameTextField.shake()
				MTToast.show(NSLocalizedString("USER_NAME_EMPTY", comment: "用户名为空"))
				return
			}
		}
		if password == "" {
			loginView.passwordTextField.shake()
				MToast.show(NSLocalizedString("PASSWORD_EMPTY", comment: "密码为空"))
				return
		}
		_isPositing = true
		if isRegister {
			MTUser.register(email: email!, userName: username!, password: password!, success: { [weak self] (_) in
				self?._isPositing = false
				self?.loginSuccess()
			}) { [weak self] (_, msg) in
				self?._isPositing = false
				MTToast.show(msg)
			}
		} else {
			MTUser.login(email: email!, password: password!, success: { [weak self] isLogin in
				self?._isPositing = false
				if isLogin {
					//提示
					let title 			= NSLocalizedString("LOGIN_VERIFY_TITLE", comment: "")
					let message 		= NSLocalizedString("LOGIN_VERIFY_MESSAGE", comment: "")
					let buttonString 	= NSLocalizedString("LOGIN_VERIFY_OK", comment: "")
					DialogManager.shared.show(title: title,
											  message: message,
											  buttonString: buttonString,
											  clickHandler: { (_) in
						//登陆成功，把uuid更新到服务器
						MTUser.conformLogin(success: { [weak self] in
							self?.loginSuccess()
						}) {_, message in
							MTToast.show(message)
						}
					})
				} else {
					self?.loginSuccess()
				}
			}) { [weak self] (_, msg) in
				self?._isPositing = false
				MToast.show(msg)
			}
		}
	}

	func didClickForgetButton() {

		if _isPositing {
			return
		}
		let email = forgetView.emailTextField.text?.trim()
		if email == "" || email?.isValidateeEmail() == false {
			forgetView.emailTextField.shake()
			MTToast.show(NSLocalizedString("EMAIL_FORMART_ERROR", comment: "邮件地址格式错误"))
			return
		}
		_isPosting = true
		SCUser.forgetPassword(email: email!, success: { [weak self] in
			self?._isPosting = false
			MTToast.show(NSLocalizedString("CHECK_RESET_LINK", comment: "密码重置链接已发送到您的邮箱。"))
		}) { [weak self] (_, msg) in
			self._isPosting = false
			MTToast.show(msg)
		}
	}

	func loginSuccess() {
		dismissNavigationController(animated: true, completion: nil)
	}
}


