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

    var loginView: LoginView!
    var forgetView: ForgetView!
    var type = LoginViewType.login

    private var _isPosting = false
    private var _isInit = false
    
    override var isShowBackgroundLayer: Bool {
        return false
    }

    override func viewDidLoad() {
        super.viewDidLoad()
        view.backgroundColor = UIColor.white
        
        title = MTLocalizedString("LOGIN_REGISTER", comment: "登录/注册")
        setLeftBarButtonItem(image: Resource.Image.Navigation.back)
        bottomConstraint.constant -= baseWinHeight - winSize.height
        contentView.layer.masksToBounds = true

        loginView = LoginView.createFromXib() as? LoginView
        loginView.backgroundColor = UIColor.clear
        loginView.translatesAutoresizingMaskIntoConstraints = false
        loginView.loginHandler = { [weak self] isRegister in self?.didClickLoginButton(isRegister: isRegister) }
        loginView.switchForgetView.addGestureRecognizer(UITapGestureRecognizer(target: self,
                                                                               action: #selector(LoginViewController.didClickGotoForgetButton(_:))))
        contentView.addSubview(loginView)
        loginView.setShowdowStyle(ShadowStyle.kButtonShadow)

        forgetView = ForgetView.createFromXib() as? ForgetView
        forgetView.backgroundColor = UIColor.clear
        forgetView.translatesAutoresizingMaskIntoConstraints = false
        forgetView.emailTextField.text = SCUser.tmpEmail
        forgetView.forgetHandler = { [weak self] in self?.didClickFrogetButton() }
        forgetView.switchLoginButton.addGestureRecognizer(UITapGestureRecognizer(target: self,
                                                                                 action: #selector(LoginViewController.didClickGotoLoginButton(_:))))
        contentView.addSubview(forgetView)
        forgetView.setShowdowStyle(ShadowStyle.kButtonShadow)

        let views = ["loginView": loginView, "forgetView": forgetView] as [String : Any]
        let metrics = ["width": winSize.width]
        contentView.addConstraints(NSLayoutConstraint.constraints(withVisualFormat: "H:|-0-[loginView(width)]-0-[forgetView(width)]",
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
        // Dispose of any resources that can be recreated.
    }

    override func viewDidLayoutSubviews() {
        super.viewDidLayoutSubviews()
        if loginView == nil || forgetView == nil || _isInit {
            return
        }
        _isInit = true

        switch type {
        case .signUp:
            loginView.emailTextField.text = ""
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
        didDismissViewController()
    }

    func didClickGotoForgetButton(_ tapGestureRecognizer: UITapGestureRecognizer) {
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
                contentView.layoutIfNeeded()
            }
        }
    }

    func didClickLoginButton(isRegister: Bool) {
        if _isPosting {
            return
        }

        let email       = loginView.emailTextField.text?.trim()
        let username    = loginView.usernameTextField.text?.trim()
        let password    = loginView.passwordTextField.text?.trim()
        if email == "" || email?.isValidateEmail() == false {
            loginView.emailTextField.shake()
            MTToast.show(MTLocalizedString("EMAIL_FORMART_ERROR", comment: "邮件地址格式错误"))
            return
        }
        if isRegister {
            if username == "" {
                loginView.usernameTextField.shake()
                MTToast.show(MTLocalizedString("USER_NAME_EMPTY", comment: "用户名为空"))
                return
            }
        }
        if password == "" {
            loginView.passwordTextField.shake()
            MTToast.show(MTLocalizedString("PASSWORD_EMPTY", comment: "密码为空"))
            return
        }
        _isPosting = true
        if isRegister {
            User.register(email: email!, userName: username!, password: password!, success: { [weak self] (_) in
                self?._isPosting = false
                self?.loginSuccess()
            }) { [weak self] (_, msg) in
                self?._isPosting = false
                MTToast.show(msg)
            }
        } else {
            User.login(email: email!, password: password!, success: { [weak self] isLogin in
                self?._isPosting = false
                if isLogin {
                    //提示
                    let title                   = MTLocalizedString("LOGIN_VERIFY_TITLE", comment: "")
                    let message                 = MTLocalizedString("LOGIN_VERIFY_MESSAGE", comment: "")
                    let buttonString            = MTLocalizedString("LOGIN_VERIFY_OK", comment: "")
                    DialogManager.shared.show(title: title,
                                              message: message,
                                              buttonString: buttonString,
                                              clickOkHandler: { (_) in
                        // 登录成功，把uuid更新到服务器
                        User.conformLogin(success: { [weak self] in
                            self?.loginSuccess()
                        }) { _, message in
                            MTToast.show(message)
                        }
                    })
                } else {
                    self?.loginSuccess()
                }
            }) { [weak self] (_, msg) in
                self?._isPosting = false
                MTToast.show(msg)
            }
        }
    }

    func didClickFrogetButton() {
        if _isPosting {
            return
        }
        let email = forgetView.emailTextField.text?.trim()
        if email == "" || email?.isValidateEmail() == false {
            forgetView.emailTextField.shake()
            MTToast.show(MTLocalizedString("EMAIL_FORMART_ERROR", comment: "邮件地址格式错误"))
            retrun
        }
        _isPosting = true
        SCUser.forgetPassword(email: email!, success: { [weak self] in
            self?._isPosting = false
            MTToast.show(MTLocalizedString("CHECK_RESET_LINK", comment: "密码重置链接已发到您的邮箱。"))
        }) { [weak self] (_, msg) in
            self?._isPosting = false
            MToast.show(msg)
        }
    }

    func loginSuccess() {
        dismissNavigationController(animated: true, completion: nil)
    }

}


