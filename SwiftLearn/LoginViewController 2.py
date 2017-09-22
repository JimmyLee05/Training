import UIKit
import MYNTKit

class LoginViewController: BaseViewController {
	
	enum LoginViewType {
		case login
		case singUp
		case forget
	}

	@IBOutlet weak var bottomConstraint: NSLayoutConstraint!
	@IBOutlet weak var contentView: UIView!

	var loginView: LoginView!
	var forgetView: ForgetView!
	var type = LoginViewType.login

	override var isShowBackgroundLayer: Bool {
		return false
	}

	override func viewDidLoad() {
		super.viewDidLoad()
		view.backgroundColor = UIColor.white

		title = MTLocalizedString("LOGIN_REGISTER", comment: "登陆／注册")
		setLeftBarButtonItem(image: Resource.Image.Navigation.back)
		bottomConstraint.constant -= baseWinHeight - winSize.height
		contentView.layer.masksToBounds = true

		loginView = LoginView.createFromXib() as? LoginView
		loginView.backgroundColor = UIColor.clear
		loginView.translatesAutoresizingMaskIntoConstraints = false
		loginView.loginHandler = { [weak self] isRegister in self?.didClickLoginButton(isRegister: isRegister) }
		loginView.switchForgetView.addGestureRecognizer(UITapGestureRecognizer(target: self,
																			   action:
																			   		#selector(LoginViewController.didClickGotoForgetButton(_ :))))
		contentView.addSubview(loginView)
		loginView.setShowdowStyle(ShadowStyle.kButtonShadow)

		forgetView = ForgetView.createFromXib() as? ForgetView
		forgetView.backgroundColor = UIColor.clear
		forgetView.translatesAutoresizingMaskIntoConstraints = false
		forgetView.emailTextField.text = SCUser.tmpEmail
		forgetView.forgetHandler = { [weak self] in self?.didClickForgetButton() }
		forgetView.switchLoginButton.addGestureRecognizer(UITapGestureRecognizer(target: self,
																				 action:
																				 	#selector(LoginViewController.didClickGotoLoginButton(_:)))
																				 	)
		contentView.addSubview(forgetView)
		forgetView.setShowdowStyle(ShadowStyle.kButtonShadow)

		let views 	= ["loginView": loginView, "forgetView": forgetView] as [String : Any]
		let metrics = ["width": winSize.width]
		contentView.addConstraints(NSLayoutConstraint.constraints(withVisualFormat: "H:|-0-[loginView(width)]-0-[forgetView(width)]",
																  options: NSLayoutConstraint(),
																  metrics: metrics,
																  views: views))
		contentView.addConstraints(NSLayoutConstraint.constraints(withVisualFormat: "V:|-0-[loginView]-0-|",
																  options: NSLayoutConstraint(),
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

		forgetview.forgetButton.setButtonBackgroundColorStyle(ColorStyle.kBlueGradientColor)
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
	 		loginView.loginButton.setTitle(MTLocalizedString("REGISTER", comment: "注册"), for: .normal)
	 		loginView.triangleLeftConstraint.constant = loginView.switchSignButton.frame.midX - loginView.triangleView.bounds.width / 2
	 	case .login:
	 		loginView.emailTextField.text = SCUser.tmpEmail
	 	default:
	 		break
	 	}
	 }

	 override func didDismissViewController() {
	 	super.didDismissViewController()
	 	_ = navigationController?.popViewController(animated: true)
	 }

	 override func leftBarButtonClickedHandler() {
	 	didDiamissViewController()
	 }

	 
}



















